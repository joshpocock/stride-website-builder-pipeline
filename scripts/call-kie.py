#!/usr/bin/env python3
"""
Kie.ai API wrapper — Nano Banana Pro + Nano Banana 2 + Nano Banana Edit.

Rewritten April 2026 against the current Kie.ai API docs:
- https://docs.kie.ai/market/google/nanobanana2
- https://docs.kie.ai/market/google/pro-image-to-image
- https://docs.kie.ai/market/google/nano-banana-edit

All models use:
  POST /api/v1/jobs/createTask  → returns {"data": {"taskId": "..."}}
  GET  /api/v1/playground/recordInfo?taskId={id}  → poll until complete

Video generation is NOT supported in this script — use call-wavespeed.py
(Seedance Pro or Veo 3 Fast) for all video needs.

Usage:
    from call_kie import generate_image, edit_image

    # Image generation (Nano Banana Pro — default)
    urls = generate_image(
        prompt="Professional studio-grade image of a blender...",
        aspect_ratio="16:9",
        resolution="2K",
    )

    # Image generation (Nano Banana standard — cheaper, no resolution control)
    urls = generate_image(
        prompt="...",
        model="nano-banana",
    )

    # Image editing (Nano Banana Edit)
    urls = edit_image(
        prompt="Change the background to a sunset...",
        image_urls=["https://example.com/photo.jpg"],
        image_size="16:9",
    )

CLI:
    python call-kie.py image --prompt "..." --aspect 16:9 --resolution 2K
    python call-kie.py image --prompt "..." --model nano-banana
    python call-kie.py edit --prompt "..." --image URL --image-size 16:9
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


# --------------------------------------------------------------------------
# Image model registry
# --------------------------------------------------------------------------

# Each model has different field names — Kie.ai is inconsistent across models.
# Field mappings verified against docs April 2026:
#   Pro:    https://docs.kie.ai/market/google/pro-image-to-image
#   Normal: https://docs.kie.ai/market/google/nanobanana2
#   Edit:   https://docs.kie.ai/market/google/nano-banana-edit
IMAGE_MODELS = {
    "nano-banana-pro": {
        "model_id": "nano-banana-pro",
        "label": "Nano Banana Pro (best quality, default)",
        "docs": "https://kie.ai/nano-banana-pro",
        "max_prompt": 10_000,
        "max_ref_images": 8,
        "aspect_field": "aspect_ratio",     # Pro uses aspect_ratio
        "image_field": "image_input",       # Pro uses image_input
        "has_resolution": True,             # 1K / 2K / 4K
        "output_formats": ("png", "jpg"),   # Pro uses "jpg" not "jpeg"
    },
    "nano-banana": {
        "model_id": "google/nano-banana",
        "label": "Nano Banana (standard, cheaper)",
        "docs": "https://docs.kie.ai/market/google/nanobanana2",
        "max_prompt": 5_000,
        "max_ref_images": 0,                # no image_input field
        "aspect_field": "image_size",       # Normal uses image_size, NOT aspect_ratio!
        "image_field": None,                # no reference image support
        "has_resolution": False,            # no resolution field
        "output_formats": ("png", "jpeg"),  # Normal uses "jpeg" not "jpg"!
    },
}

EDIT_MODEL = {
    "model_id": "google/nano-banana-edit",
    "label": "Nano Banana Edit",
    "docs": "https://docs.kie.ai/market/google/nano-banana-edit",
    "max_prompt": 5_000,
    "max_images": 10,
    "aspect_field": "image_size",       # Edit uses image_size like Normal
    "image_field": "image_urls",        # Edit uses image_urls (required!)
    "has_resolution": False,
    "output_formats": ("png", "jpeg"),  # Edit uses "jpeg" like Normal
}


# --------------------------------------------------------------------------
# Auth
# --------------------------------------------------------------------------

def _api_key() -> str:
    """Load Kie.ai API key from env, then walk upward for .env files,
    then fall back to the kie-ai skill's mcp-config.json."""
    key = os.environ.get("KIE_AI_API_KEY")
    if key:
        return key

    cwd = Path.cwd()
    for ancestor in [cwd, *cwd.parents]:
        env_file = ancestor / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("KIE_AI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    fallback = Path.home() / ".claude" / "skills" / "kie-ai" / "mcp-config.json"
    if not fallback.exists():
        for ancestor in [cwd, *cwd.parents]:
            candidate = ancestor / ".claude" / "skills" / "kie-ai" / "mcp-config.json"
            if candidate.exists():
                fallback = candidate
                break
    if fallback.exists():
        data = json.loads(fallback.read_text(encoding="utf-8"))
        try:
            return data["mcpServers"]["kie-ai"]["env"]["KIE_AI_API_KEY"]
        except (KeyError, TypeError):
            pass

    raise RuntimeError(
        "Kie.ai API key not found. Set KIE_AI_API_KEY env var, "
        "add it to a .env file in the project root, "
        "or ensure .claude/skills/kie-ai/mcp-config.json exists."
    )


# --------------------------------------------------------------------------
# HTTP helpers
# --------------------------------------------------------------------------

BASE_URL = "https://api.kie.ai/api/v1"


def _post(path: str, body: dict) -> dict:
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _get(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {_api_key()}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _poll(task_id: str, interval: int = 5, max_wait: int = 900) -> dict:
    """Poll GET /playground/recordInfo?taskId={id} until task completes.

    Verified working in April 2026 production run. The old /tasks/{id}
    endpoint is dead — do not use it.
    """
    url = f"{BASE_URL}/playground/recordInfo?taskId={task_id}"
    elapsed = 0
    while elapsed < max_wait:
        resp = _get(url)
        data = resp.get("data", {})
        state = data.get("status") or data.get("state", "")
        state_lower = state.lower() if isinstance(state, str) else ""

        if state_lower in ("completed", "succeeded", "success", "done"):
            return data
        if state_lower in ("failed", "error"):
            raise RuntimeError(f"Kie.ai task failed: {json.dumps(data, indent=2)}")

        # "waiting" or "processing" — keep polling
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f"Kie.ai task {task_id} did not complete within {max_wait}s")


# --------------------------------------------------------------------------
# Image generation
# --------------------------------------------------------------------------

def generate_image(
    prompt: str,
    model: str = "nano-banana-pro",
    aspect_ratio: str = "16:9",
    resolution: str = "2K",
    output_format: str = "png",
    reference_images: list[str] | None = None,
) -> list[str]:
    """Generate image(s) via Kie.ai. Returns list of output URLs.

    Default: Nano Banana Pro (https://kie.ai/nano-banana-pro)
    Alternative: 'nano-banana-2' (https://kie.ai/nano-banana-2) — cheaper

    resolution options: '1K', '2K', '4K' (default '2K')
    aspect_ratio options: '1:1', '16:9', '9:16', '3:2', '2:3', '3:4', '4:3',
        '4:5', '5:4', '21:9', 'auto'
    output_format: 'png' or 'jpg'
    """
    if model not in IMAGE_MODELS:
        raise ValueError(
            f"Unknown model '{model}'. Valid: {', '.join(IMAGE_MODELS.keys())}. "
            f"For editing, use edit_image() instead."
        )
    info = IMAGE_MODELS[model]

    input_body: dict = {
        "prompt": prompt,
        info["aspect_field"]: aspect_ratio,
        "output_format": output_format,
    }
    if info["has_resolution"] and resolution:
        input_body["resolution"] = resolution
    if reference_images and info["image_field"]:
        input_body[info["image_field"]] = reference_images

    body = {
        "model": info["model_id"],
        "input": input_body,
    }

    resp = _post("/jobs/createTask", body)
    task_id = (resp.get("data") or {}).get("taskId")
    if not task_id:
        raise RuntimeError(f"Kie.ai did not return a taskId: {json.dumps(resp, indent=2)}")

    result = _poll(task_id)
    # Extract output URLs from the result — Kie uses various field names
    urls = (
        result.get("output")
        or result.get("images")
        or result.get("outputUrls")
        or result.get("urls")
        or []
    )
    if isinstance(urls, str):
        urls = [urls]
    return [u if isinstance(u, str) else u.get("url", "") for u in urls]


# --------------------------------------------------------------------------
# Image editing
# --------------------------------------------------------------------------

def edit_image(
    prompt: str,
    image_urls: list[str],
    image_size: str = "16:9",
    output_format: str = "png",
) -> list[str]:
    """Edit image(s) via Nano Banana Edit. Returns list of output URLs.

    Docs: https://docs.kie.ai/market/google/nano-banana-edit

    Note: This model uses different field names than the generation models:
    - 'image_urls' not 'image_input'
    - 'image_size' not 'aspect_ratio'
    - output_format accepts 'png' or 'jpeg' (not 'jpg')
    """
    input_body: dict = {
        "prompt": prompt,
        "image_urls": image_urls,
        "image_size": image_size,
        "output_format": output_format,
    }

    body = {
        "model": EDIT_MODEL["model_id"],
        "input": input_body,
    }

    resp = _post("/jobs/createTask", body)
    task_id = (resp.get("data") or {}).get("taskId")
    if not task_id:
        raise RuntimeError(f"Kie.ai did not return a taskId: {json.dumps(resp, indent=2)}")

    result = _poll(task_id)
    urls = (
        result.get("output")
        or result.get("images")
        or result.get("outputUrls")
        or result.get("urls")
        or []
    )
    if isinstance(urls, str):
        urls = [urls]
    return [u if isinstance(u, str) else u.get("url", "") for u in urls]


# --------------------------------------------------------------------------
# Video — NOT supported, use call-wavespeed.py
# --------------------------------------------------------------------------

def generate_video(*args, **kwargs):
    """Use call-wavespeed.py video subcommand instead.

    Kie.ai video model IDs are not verified on the current API. Wavespeed
    has confirmed-working Seedance Pro and Veo 3 Fast paths.
    """
    raise NotImplementedError(
        "Video generation is not supported in call-kie.py.\n"
        "Use call-wavespeed.py instead:\n"
        "  python scripts/call-wavespeed.py video --model seedance-pro "
        "--start URL --end URL --prompt '...' --duration 5\n"
    )


# --------------------------------------------------------------------------
# Download
# --------------------------------------------------------------------------

def download(url: str, dest: Path) -> Path:
    """Download a file from a URL. Kie result URLs are temporary — download immediately."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as resp:
        dest.write_bytes(resp.read())
    return dest


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Kie.ai image generation — Nano Banana Pro / 2 / Edit"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Image generation
    img = sub.add_parser("image", help="Generate image(s) via Nano Banana Pro (default) or Nano Banana 2")
    img.add_argument("--prompt", required=True)
    img.add_argument("--model", default="nano-banana-pro", choices=list(IMAGE_MODELS.keys()))
    img.add_argument("--aspect", default="16:9")
    img.add_argument("--resolution", default="2K", choices=["1K", "2K", "4K"])
    img.add_argument("--format", default="png", choices=["png", "jpg"])
    img.add_argument("--ref-image", action="append", default=[], help="Reference image URL (can repeat)")
    img.add_argument("--out", default=".")

    # Image editing
    ed = sub.add_parser("edit", help="Edit image(s) via Nano Banana Edit")
    ed.add_argument("--prompt", required=True)
    ed.add_argument("--image", required=True, action="append", help="Input image URL (can repeat)")
    ed.add_argument("--image-size", default="16:9")
    ed.add_argument("--format", default="png", choices=["png", "jpeg"])
    ed.add_argument("--out", default=".")

    args = parser.parse_args()

    if args.cmd == "image":
        urls = generate_image(
            prompt=args.prompt,
            model=args.model,
            aspect_ratio=args.aspect,
            resolution=args.resolution,
            output_format=args.format,
            reference_images=args.ref_image or None,
        )
        for i, url in enumerate(urls):
            print(f"URL: {url}")
        for i, url in enumerate(urls):
            dest = Path(args.out) / f"image-{i+1}.{args.format}"
            download(url, dest)
            print(f"Downloaded: {dest}")

    elif args.cmd == "edit":
        urls = edit_image(
            prompt=args.prompt,
            image_urls=args.image,
            image_size=args.image_size,
            output_format=args.format,
        )
        for i, url in enumerate(urls):
            print(f"URL: {url}")
        for i, url in enumerate(urls):
            dest = Path(args.out) / f"edit-{i+1}.{args.format}"
            download(url, dest)
            print(f"Downloaded: {dest}")


if __name__ == "__main__":
    try:
        _cli()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
