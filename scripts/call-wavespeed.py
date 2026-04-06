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
    python call-wavespeed.py video --model seedance-pro --start URL --end URL --prompt "..." --duration 5
    python call-wavespeed.py video --model veo3-fast --start URL --prompt "..." --duration 8

NOTE on Gemini 3 Pro Image variant count (2026-04):
    Gemini 3 Pro returns exactly 1 image per call regardless of --n. For N
    variants, issue N separate calls with different --seed values. Other
    models (Nano Banana Pro, Gemini 2.5 Flash) do support true --n batching.

NOTE on lock-pair (2026-04):
    The lock-pair subcommand has been removed because the nano-banana-pro/
    edit-multi parameter schema drifted and the function returns HTTP 400.
    The lock_pair() Python function is still present but raises
    NotImplementedError. Skip lock-pair until the correct body shape is
    re-verified against Wavespeed docs.
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


# Image model shortcuts — maps friendly names to full endpoint paths
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


# Video model registry — each verified against Wavespeed during a 2026-04
# production run unless otherwise noted. Path is passed straight through
# to the Wavespeed POST endpoint under BASE_URL. end_param is the body
# key name the model expects for the end frame (differs between providers).
# duration_options is None if the model accepts arbitrary durations, else
# the tuple of valid values — callers outside the tuple get 400 errors.
VIDEO_MODELS = {
    "seedance-pro": {
        "path": "bytedance/seedance-v1-pro-i2v-480p",
        "label": "Seedance v1 Pro (image-to-video, 480p)",
        "supports_end_frame": True,
        "end_param": "last_image",  # Seedance uses "last_image", not "end_image"
        "duration_options": None,
        "cost_tier": "cheap",
        "verified": True,
    },
    "seedance-lite": {
        "path": "bytedance/seedance-v1-lite-i2v-480p",
        "label": "Seedance v1 Lite (image-to-video, 480p)",
        "supports_end_frame": True,
        "end_param": "last_image",
        "duration_options": None,
        "cost_tier": "cheap",
        "verified": True,  # model exists; production user hit insufficient-credits
    },
    "veo3-fast": {
        "path": "google/veo3-fast/image-to-video",
        "label": "Veo 3 Fast (image-to-video)",
        "supports_end_frame": False,  # Veo 3 i2v is single-frame input
        "end_param": None,
        "duration_options": (4, 6, 8),  # only 4, 6, or 8 seconds — verified
        "cost_tier": "mid",
        "verified": True,
    },
    # NOTE: kling on Wavespeed is NOT verified — production probes against
    # kwaivgi/kling-v2-1-master/image-to-video and kwaivgi/kling-v2-master/
    # image-to-video both returned 400 "model not found". Kling is currently
    # Kie-only, but Kie's video path is broken too (see call-kie.py). If you
    # find a working Wavespeed Kling path, add it here.
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
    """Accept either a shortcut key ('gemini-3-pro', 'seedance-pro') or a full path.
    Checks both the image MODELS dict and the VIDEO_MODELS registry."""
    if "/" in model:
        return model
    if model in MODELS:
        return MODELS[model]
    if model in VIDEO_MODELS:
        return VIDEO_MODELS[model]["path"]
    valid = list(MODELS.keys()) + list(VIDEO_MODELS.keys())
    raise ValueError(f"Unknown model '{model}'. Valid shortcuts: {', '.join(valid)}")


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


def lock_pair(*args, **kwargs) -> list[str]:
    """BROKEN as of 2026-04. The nano-banana-pro/edit-multi endpoint returns
    HTTP 400 with the previous body shape ({"prompt", "images": [...],
    "aspect_ratio", "num_images": 2}). The model exists but the parameter
    schema drifted — probable fixes include renaming `images` to
    `image_urls` or to individual `image_1`/`image_2` fields, dropping
    `aspect_ratio` (possibly inferred from inputs), or dropping
    `num_images: 2`. None have been verified.

    Until the correct body shape is confirmed against live Wavespeed docs,
    this function raises to prevent silently broken pipeline runs.
    Downstream callers should skip the lock-pair matching step when this
    raises — it's a quality polish, not a hard requirement."""
    raise NotImplementedError(
        "call-wavespeed.py lock_pair() is broken — the nano-banana-pro/"
        "edit-multi parameter schema drifted and the correct body shape "
        "has not been reverified against Wavespeed docs.\n"
        "\n"
        "Workaround: skip the lock-pair step. Generate start + end frames "
        "with consistent prompts and seeds via generate_image() and rely "
        "on the prompt to carry lighting/camera/palette coherence. The "
        "downstream Kling/Seedance transition will still work — it will "
        "just be slightly less visually locked between the two frames.\n"
    )


def generate_video(
    start_image_url: str,
    prompt: str,
    end_image_url: str | None = None,
    duration_seconds: int = 5,
    aspect_ratio: str = "16:9",
    model: str = "seedance-pro",
) -> str:
    """Generate an image-to-video clip via Wavespeed. Returns the output URL.

    Default model is Seedance v1 Pro (bytedance/seedance-v1-pro-i2v-480p),
    verified working in April 2026. Supports start+end frame interpolation
    (pass end_image_url for scroll-bound hero transitions). Veo 3 Fast is
    the other verified path but only accepts single-frame input and requires
    duration in (4, 6, 8).

    See VIDEO_MODELS for the full registry and per-model parameter quirks.
    """
    if model not in VIDEO_MODELS:
        raise ValueError(
            f"Unknown video model '{model}'. Valid options: "
            f"{', '.join(VIDEO_MODELS.keys())}"
        )
    info = VIDEO_MODELS[model]
    path = info["path"]

    # Duration validation — Veo 3 only accepts specific values, Seedance is open
    if info["duration_options"] is not None:
        if duration_seconds not in info["duration_options"]:
            raise ValueError(
                f"{info['label']} requires duration in "
                f"{info['duration_options']}, got {duration_seconds}"
            )

    body: dict = {
        "prompt": prompt,
        "image": start_image_url,
        "aspect_ratio": aspect_ratio,
        "duration": duration_seconds,
    }

    # End-frame support varies: Seedance uses "last_image", Veo has no end frame
    if info["supports_end_frame"] and end_image_url:
        body[info["end_param"]] = end_image_url

    resp = _post(path, body)
    data = resp.get("data", {})

    # If sync response, output is directly present
    if data.get("outputs"):
        outputs = data["outputs"]
        return outputs[0] if outputs else ""

    # Otherwise poll
    task_id = data.get("id")
    result_url = (data.get("urls") or {}).get("get")
    result = _poll(result_url or task_id, max_wait=1800)
    outputs = result.get("outputs", [])
    return outputs[0] if outputs else ""


def download(url: str, dest: Path) -> Path:
    """Download a file from a URL to a local path. Wavespeed URLs on cdn.wavespeed.ai are stable but download immediately to be safe."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as resp:
        dest.write_bytes(resp.read())
    return dest


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Wavespeed AI wrapper (Gemini 3 Pro Image + Nano Banana Pro + Seedance/Veo video)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    img = sub.add_parser("image", help="Generate images (default: Gemini 3 Pro Image, 4K). NOTE: Gemini 3 Pro returns exactly 1 variant per call — for N variants, issue N separate calls with different --seed.")
    img.add_argument("--prompt", required=True)
    img.add_argument("--model", default="gemini-3-pro", help=f"Shortcut or full path. Shortcuts: {', '.join(MODELS.keys())}")
    img.add_argument("--aspect", default="16:9")
    img.add_argument("--n", type=int, default=4, help="num_images param. Ignored by gemini-3-pro (always 1).")
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

    vid = sub.add_parser("video", help="Generate image-to-video clip (Seedance Pro by default, also supports Veo 3 Fast)")
    vid.add_argument("--start", required=True, help="Start frame URL")
    vid.add_argument("--end", default=None, help="End frame URL (Seedance only — Veo doesn't do end-frame i2v)")
    vid.add_argument("--prompt", required=True)
    vid.add_argument("--model", default="seedance-pro", choices=list(VIDEO_MODELS.keys()))
    vid.add_argument("--duration", type=int, default=5, help="Duration in seconds. Veo 3 Fast only accepts 4, 6, or 8.")
    vid.add_argument("--aspect", default="16:9")
    vid.add_argument("--out", default=".")

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
        # Print URLs FIRST so downstream pipeline steps can capture them
        # even if downloads fail. Print both the source URL and the local
        # path — downstream callers need the URL for chaining (video gen,
        # lock-pair, etc.), and the local path for local operations.
        for i, url in enumerate(urls):
            print(f"URL: {url}")
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
            print(f"URL: {url}")
        for i, url in enumerate(urls):
            dest = Path(args.out) / f"edit-{i+1}.webp"
            download(url, dest)
            print(f"Downloaded: {dest}")

    elif args.cmd == "video":
        url = generate_video(
            start_image_url=args.start,
            prompt=args.prompt,
            end_image_url=args.end,
            duration_seconds=args.duration,
            aspect_ratio=args.aspect,
            model=args.model,
        )
        print(f"URL: {url}")
        dest = Path(args.out) / "hero.mp4"
        download(url, dest)
        print(f"Downloaded: {dest}")


if __name__ == "__main__":
    try:
        _cli()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
