#!/usr/bin/env python3
"""
Kie.ai API wrapper for NanoBanana 2 + Kling 3.0 + Veo 3 / Veo 3.1.

Known-good params (verified from memory):
- `size` (standard/high) for quality
- `aspect_ratio` (portrait/landscape/square/16:9/9:16/1:1)
- `n_frames` (10/15) is REQUIRED for video generation
- Do NOT use `quality` param — API rejects it with "size is invalid"
- High quality 15s portrait video renders take ~12-15 min
- Result URLs are temporary (tempfile.aiquickdraw.com) — download immediately

Supported video models (pass to generate_video via `model=`):
- `kling3`        — Kling 3.0 (default, fastest, cheapest, image-to-image)
- `veo3-fast`     — Veo 3 Fast (mid-tier quality, faster renders)
- `veo3`          — Veo 3 (high quality, slower)
- `veo3.1-fast`   — Veo 3.1 Fast (newest, balanced)
- `veo3.1`        — Veo 3.1 (newest, highest quality)
NOTE: Exact Kie.ai model identifiers should be cross-referenced against current
Kie docs — the names above follow Kie's public naming pattern but may need
tweaking as Kie renames endpoints. The API passes `model` through as a string
so overriding from the caller is always safe.

Usage:
    from call_kie import generate_image, generate_video

    # Image (NanoBanana 2)
    urls = generate_image(
        prompt="Professional studio-grade image of a blender...",
        aspect_ratio="16:9",
        size="high",
        n=4,  # generate 4 variants
    )

    # Video (Kling 3.0)
    video_url = generate_video(
        start_image_url="https://.../start.webp",
        end_image_url="https://.../end.webp",
        prompt="The lid lifts off, components separate...",
        duration_seconds=5,
        aspect_ratio="16:9",
    )

CLI:
    python call-kie.py image --prompt "..." --aspect 16:9 --n 4
    python call-kie.py video --start URL --end URL --prompt "..." --duration 5
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


def _api_key() -> str:
    """Load Kie.ai API key from env or from kie-ai skill's mcp-config.json."""
    key = os.environ.get("KIE_AI_API_KEY")
    if key:
        return key

    # Fallback: read from the kie-ai skill config (per memory)
    fallback = (
        Path.home()
        / ".claude"
        / "skills"
        / "kie-ai"
        / "mcp-config.json"
    )
    if not fallback.exists():
        # Also try project-level skill
        cwd = Path.cwd()
        for ancestor in [cwd, *cwd.parents]:
            candidate = ancestor / ".claude" / "skills" / "kie-ai" / "mcp-config.json"
            if candidate.exists():
                fallback = candidate
                break

    if fallback.exists():
        data = json.loads(fallback.read_text(encoding="utf-8"))
        # MCP config typically has { "mcpServers": { "kie-ai": { "env": { "KIE_AI_API_KEY": "..." } } } }
        try:
            return data["mcpServers"]["kie-ai"]["env"]["KIE_AI_API_KEY"]
        except (KeyError, TypeError):
            pass

    raise RuntimeError(
        "Kie.ai API key not found. Set KIE_AI_API_KEY env var, "
        "or ensure .claude/skills/kie-ai/mcp-config.json exists."
    )


BASE_URL = "https://api.kie.ai/v1"

# Video model registry — caller picks one, passed straight through to Kie.
# Verify exact model IDs against Kie.ai docs if a call returns a model-not-found error.
VIDEO_MODELS = {
    "kling3": {"label": "Kling 3.0", "supports_end_frame": True, "cost_tier": "cheap"},
    "veo3-fast": {"label": "Veo 3 Fast", "supports_end_frame": False, "cost_tier": "mid"},
    "veo3": {"label": "Veo 3", "supports_end_frame": False, "cost_tier": "high"},
    "veo3.1-fast": {"label": "Veo 3.1 Fast", "supports_end_frame": False, "cost_tier": "mid"},
    "veo3.1": {"label": "Veo 3.1", "supports_end_frame": False, "cost_tier": "high"},
}


def _post(path: str, body: dict) -> dict:
    req = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _get(path: str) -> dict:
    req = urllib.request.Request(
        BASE_URL + path,
        headers={"Authorization": f"Bearer {_api_key()}"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _poll(task_id: str, interval: int = 5, max_wait: int = 900) -> dict:
    """Poll a Kie.ai task until done. Returns the final result dict."""
    elapsed = 0
    while elapsed < max_wait:
        status = _get(f"/tasks/{task_id}")
        state = status.get("status")
        if state in ("completed", "succeeded", "success"):
            return status
        if state in ("failed", "error"):
            raise RuntimeError(f"Kie.ai task failed: {status}")
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f"Kie.ai task {task_id} did not complete within {max_wait}s")


def generate_image(
    prompt: str,
    aspect_ratio: str = "16:9",
    size: str = "high",
    n: int = 4,
    reference_images: list[str] | None = None,
    model: str = "nanoBanana2",
) -> list[str]:
    """Generate N image variants and return a list of URLs."""
    body = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "size": size,  # NOT "quality" — memory note
        "n": n,
    }
    if reference_images:
        body["reference_images"] = reference_images

    result = _post("/images/generations", body)
    task_id = result.get("task_id") or result.get("id")
    if task_id:
        result = _poll(task_id)
    urls = result.get("images") or result.get("output") or []
    return [img if isinstance(img, str) else img.get("url") for img in urls]


def generate_video(
    start_image_url: str,
    prompt: str,
    end_image_url: str | None = None,
    duration_seconds: int = 5,
    aspect_ratio: str = "16:9",
    size: str = "high",
    model: str = "kling3",
) -> str:
    """Generate a video (Kling 3.0 or Veo 3/3.1) from a start frame.

    Kling supports an end_image_url for image-to-image interpolation (best
    for scroll-bound hero transitions). Veo models take a single start frame
    plus prompt and generate from there — pass end_image_url=None for Veo.
    """
    n_frames = 10 if duration_seconds <= 5 else 15
    model_info = VIDEO_MODELS.get(model, {})
    supports_end = model_info.get("supports_end_frame", False)

    body = {
        "model": model,
        "prompt": prompt,
        "start_image": start_image_url,
        "aspect_ratio": aspect_ratio,
        "size": size,
        "n_frames": n_frames,
        "duration": duration_seconds,
        "enhance": False,
    }
    if supports_end and end_image_url:
        body["end_image"] = end_image_url

    result = _post("/videos/generations", body)
    task_id = result.get("task_id") or result.get("id")
    if task_id:
        result = _poll(task_id, interval=15, max_wait=1800)
    return result.get("video_url") or result.get("output")


def download(url: str, dest: Path) -> Path:
    """Download a file from a URL to a local path. Result URLs are temporary per memory."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as resp:
        dest.write_bytes(resp.read())
    return dest


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Kie.ai NanoBanana + Kling wrapper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    img = sub.add_parser("image", help="Generate image(s) via NanoBanana 2")
    img.add_argument("--prompt", required=True)
    img.add_argument("--aspect", default="16:9")
    img.add_argument("--size", default="high", choices=["standard", "high"])
    img.add_argument("--n", type=int, default=4)
    img.add_argument("--out", default=".")

    vid = sub.add_parser("video", help="Generate video via Kling 3.0 / Veo 3 / Veo 3.1")
    vid.add_argument("--start", required=True, help="start image URL")
    vid.add_argument("--end", default=None, help="end image URL (Kling only; ignored for Veo)")
    vid.add_argument("--prompt", required=True)
    vid.add_argument("--duration", type=int, default=5)
    vid.add_argument("--aspect", default="16:9")
    vid.add_argument("--model", default="kling3", choices=list(VIDEO_MODELS.keys()))
    vid.add_argument("--out", default=".")

    args = parser.parse_args()

    if args.cmd == "image":
        urls = generate_image(
            prompt=args.prompt,
            aspect_ratio=args.aspect,
            size=args.size,
            n=args.n,
        )
        for i, url in enumerate(urls):
            dest = Path(args.out) / f"image-{i+1}.webp"
            download(url, dest)
            print(f"Downloaded: {dest}")

    elif args.cmd == "video":
        url = generate_video(
            start_image_url=args.start,
            end_image_url=args.end,
            prompt=args.prompt,
            duration_seconds=args.duration,
            aspect_ratio=args.aspect,
            model=args.model,
        )
        dest = Path(args.out) / "hero.mp4"
        download(url, dest)
        print(f"Downloaded: {dest}")


if __name__ == "__main__":
    try:
        _cli()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
