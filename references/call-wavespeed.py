#!/usr/bin/env python3
"""
Wavespeed AI API wrapper for Gemini 3 Pro Image + Nano Banana Pro Edit.

Wavespeed is used when the pipeline wants state-of-the-art 4K hero pairs
(Gemini 3 Pro Image) and high-quality edit passes (Nano Banana Pro Edit Multi)
that are not yet available on Kie.ai.

Model menu for the website pipeline:
- `google/gemini-3-pro-image/text-to-image`  — 4K hero frames, $0.025/img
- `google/gemini-3-pro-image/edit`           — edit pass on Gemini 3 output
- `google/nano-banana-pro/edit-multi`        — lock-pair matching (accepts both frames)
- `google/nano-banana-pro/text-to-image`     — fallback T2I if Gemini 3 is down
- `google/gemini-2.5-flash-image/text-to-image` — cheap variants ($0.015/img)
- `google/gemini-2.5-flash-image/edit`       — cheap targeted edits ($0.015/img)

Usage:
    from call_wavespeed import generate_image, edit_image, lock_pair

    # 4K hero frame via Gemini 3 Pro Image
    urls = generate_image(
        prompt="A cinematic extreme close-up of a brushed titanium watch...",
        model="google/gemini-3-pro-image/text-to-image",
        aspect_ratio="16:9",
        num_images=4,
    )

    # Lock-pair matching pass — feeds both frames back in
    locked = lock_pair(
        start_url="https://.../start.webp",
        end_url="https://.../end.webp",
        prompt="Match lighting, color, and camera between these two frames...",
    )

CLI:
    python call-wavespeed.py image --model gemini-3-pro --prompt "..." --n 4
    python call-wavespeed.py edit --image URL --prompt "..."
    python call-wavespeed.py lock-pair --start URL --end URL --prompt "..."
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


BASE_URL = "https://api.wavespeed.ai/api/v3"


# Model shortcuts — maps friendly names to full endpoint paths
MODELS = {
    "gemini-3-pro": "google/gemini-3-pro-image/text-to-image",
    "gemini-3-pro-edit": "google/gemini-3-pro-image/edit",
    "nano-banana-pro": "google/nano-banana-pro/text-to-image",
    "nano-banana-pro-edit": "google/nano-banana-pro/edit",
    "nano-banana-pro-edit-multi": "google/nano-banana-pro/edit-multi",
    "nano-banana-pro-ultra": "google/nano-banana-pro/text-to-image-ultra",
    "nano-banana": "google/gemini-2.5-flash-image/text-to-image",
    "nano-banana-edit": "google/gemini-2.5-flash-image/edit",
}


def _api_key() -> str:
    """Load Wavespeed API key from env."""
    key = os.environ.get("WAVESPEED_API_KEY")
    if key:
        return key

    # Fallback: walk upward looking for a .env file with WAVESPEED_API_KEY
    cwd = Path.cwd()
    for ancestor in [cwd, *cwd.parents]:
        env_file = ancestor / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("WAVESPEED_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    raise RuntimeError(
        "Wavespeed API key not found. Set WAVESPEED_API_KEY env var "
        "or add it to a .env file in the project root."
    )


def _post(path: str, body: dict) -> dict:
    """POST to a Wavespeed model endpoint. Path is the model path, e.g. 'google/gemini-3-pro-image/text-to-image'."""
    url = f"{BASE_URL}/{path}"
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


def _poll(task_id_or_url: str, max_wait: int = 600) -> dict:
    """Poll a Wavespeed task until done. Accepts either a task id or a full result URL."""
    if task_id_or_url.startswith("http"):
        result_url = task_id_or_url
    else:
        result_url = f"{BASE_URL}/predictions/{task_id_or_url}/result"

    elapsed = 0
    interval = 3  # start at 3s per api-core.md
    while elapsed < max_wait:
        resp = _get(result_url)
        data = resp.get("data", {})
        state = data.get("status")
        if state == "completed":
            return data
        if state == "failed":
            raise RuntimeError(f"Wavespeed task failed: {data.get('error', 'unknown')}")
        time.sleep(interval)
        elapsed += interval
        if elapsed >= 30:
            interval = 10  # switch to 10s intervals after 30s per api-core.md
    raise TimeoutError(f"Wavespeed task did not complete within {max_wait}s")


def _resolve_model(model: str) -> str:
    """Accept either a shortcut key ('gemini-3-pro') or a full path ('google/gemini-3-pro-image/text-to-image')."""
    if "/" in model:
        return model
    if model in MODELS:
        return MODELS[model]
    raise ValueError(f"Unknown model '{model}'. Valid shortcuts: {', '.join(MODELS.keys())}")


def generate_image(
    prompt: str,
    model: str = "gemini-3-pro",
    aspect_ratio: str = "16:9",
    num_images: int = 4,
    negative_prompt: str | None = None,
    seed: int | None = None,
    enable_sync_mode: bool = False,
) -> list[str]:
    """Generate N image variants via Wavespeed. Returns list of output URLs.

    Default model is Gemini 3 Pro Image (4K, $0.025/img). For cheaper iteration,
    use 'nano-banana' ($0.015/img) or 'nano-banana-pro' ($0.030/img).
    """
    path = _resolve_model(model)
    body: dict = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "num_images": num_images,
    }
    if negative_prompt:
        body["negative_prompt"] = negative_prompt
    if seed is not None:
        body["seed"] = seed
    if enable_sync_mode:
        body["enable_sync_mode"] = True

    resp = _post(path, body)
    data = resp.get("data", {})

    # If sync mode, outputs come back directly
    if enable_sync_mode and data.get("outputs"):
        return data["outputs"]

    # Otherwise poll
    task_id = data.get("id")
    result_url = (data.get("urls") or {}).get("get")
    result = _poll(result_url or task_id)
    return result.get("outputs", [])


def edit_image(
    image_url: str,
    prompt: str,
    model: str = "nano-banana-pro-edit",
    aspect_ratio: str = "16:9",
    num_images: int = 1,
) -> list[str]:
    """Edit an existing image. Use 'nano-banana-pro-edit' for targeted edits.

    For Gemini 3 Pro Image edits (4K output), pass model='gemini-3-pro-edit'.
    """
    path = _resolve_model(model)
    body: dict = {
        "prompt": prompt,
        "image": image_url,
        "aspect_ratio": aspect_ratio,
        "num_images": num_images,
    }
    resp = _post(path, body)
    data = resp.get("data", {})
    task_id = data.get("id")
    result_url = (data.get("urls") or {}).get("get")
    result = _poll(result_url or task_id)
    return result.get("outputs", [])


def lock_pair(
    start_url: str,
    end_url: str,
    prompt: str,
    aspect_ratio: str = "16:9",
) -> list[str]:
    """Lock-pair matching pass: feed both frames into Nano Banana Pro Edit Multi,
    ask it to match lighting, color, and camera across the pair. Returns two
    output URLs (start and end), color-matched."""
    path = _resolve_model("nano-banana-pro-edit-multi")
    body = {
        "prompt": prompt,
        "images": [start_url, end_url],
        "aspect_ratio": aspect_ratio,
        "num_images": 2,
    }
    resp = _post(path, body)
    data = resp.get("data", {})
    task_id = data.get("id")
    result_url = (data.get("urls") or {}).get("get")
    result = _poll(result_url or task_id)
    return result.get("outputs", [])


def download(url: str, dest: Path) -> Path:
    """Download a file from a URL to a local path. Wavespeed URLs on cdn.wavespeed.ai are stable but download immediately to be safe."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as resp:
        dest.write_bytes(resp.read())
    return dest


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Wavespeed AI wrapper (Gemini 3 Pro Image + Nano Banana Pro)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    img = sub.add_parser("image", help="Generate images (default: Gemini 3 Pro Image, 4K)")
    img.add_argument("--prompt", required=True)
    img.add_argument("--model", default="gemini-3-pro", help=f"Shortcut or full path. Shortcuts: {', '.join(MODELS.keys())}")
    img.add_argument("--aspect", default="16:9")
    img.add_argument("--n", type=int, default=4)
    img.add_argument("--negative", default=None)
    img.add_argument("--seed", type=int, default=None)
    img.add_argument("--sync", action="store_true", help="Enable sync mode (blocks until done)")
    img.add_argument("--out", default=".")

    ed = sub.add_parser("edit", help="Edit an image (Nano Banana Pro Edit by default)")
    ed.add_argument("--image", required=True, help="Source image URL")
    ed.add_argument("--prompt", required=True)
    ed.add_argument("--model", default="nano-banana-pro-edit")
    ed.add_argument("--aspect", default="16:9")
    ed.add_argument("--n", type=int, default=1)
    ed.add_argument("--out", default=".")

    lp = sub.add_parser("lock-pair", help="Match lighting/color/camera across a start+end frame pair")
    lp.add_argument("--start", required=True, help="Start frame URL")
    lp.add_argument("--end", required=True, help="End frame URL")
    lp.add_argument("--prompt", required=True)
    lp.add_argument("--aspect", default="16:9")
    lp.add_argument("--out", default=".")

    args = parser.parse_args()

    if args.cmd == "image":
        urls = generate_image(
            prompt=args.prompt,
            model=args.model,
            aspect_ratio=args.aspect,
            num_images=args.n,
            negative_prompt=args.negative,
            seed=args.seed,
            enable_sync_mode=args.sync,
        )
        for i, url in enumerate(urls):
            dest = Path(args.out) / f"image-{i+1}.webp"
            download(url, dest)
            print(f"Downloaded: {dest}")

    elif args.cmd == "edit":
        urls = edit_image(
            image_url=args.image,
            prompt=args.prompt,
            model=args.model,
            aspect_ratio=args.aspect,
            num_images=args.n,
        )
        for i, url in enumerate(urls):
            dest = Path(args.out) / f"edit-{i+1}.webp"
            download(url, dest)
            print(f"Downloaded: {dest}")

    elif args.cmd == "lock-pair":
        urls = lock_pair(
            start_url=args.start,
            end_url=args.end,
            prompt=args.prompt,
            aspect_ratio=args.aspect,
        )
        for i, url in enumerate(urls):
            label = "start" if i == 0 else "end"
            dest = Path(args.out) / f"locked-{label}.webp"
            download(url, dest)
            print(f"Downloaded: {dest}")


if __name__ == "__main__":
    try:
        _cli()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
