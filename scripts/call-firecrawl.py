#!/usr/bin/env python3
"""
Firecrawl brand extraction wrapper.

Uses Firecrawl's first-class `branding` format (verified 2026-04-04). No
custom schema needed — the branding format handles color palette, typography,
logo, favicon, spacing, button styles, and personality natively.

Docs: https://docs.firecrawl.dev/features/scrape
Branding Format v2 blog: https://www.firecrawl.dev/blog/branding-format-v2

Usage:
    from call_firecrawl import extract_brand
    brand = extract_brand("https://stripe.com")
    # → {"logo": "...", "colors": {...}, "typography": {...}, ...}

CLI:
    python call-firecrawl.py https://stripe.com --out brand.json

Install:
    pip install firecrawl-py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


API_KEY_ENV = "FIRECRAWL_API_KEY"


def _api_key() -> str:
    key = os.environ.get(API_KEY_ENV)
    if not key:
        raise RuntimeError(
            f"{API_KEY_ENV} not set in environment. "
            "Get a free key at https://firecrawl.dev (500 credits free tier)."
        )
    return key


def extract_brand(url: str) -> dict:
    """
    Extract brand identity from a URL using Firecrawl's branding format.

    Returns the `branding` sub-dict from the Firecrawl scrape response, which
    includes logo, favicon, colors (primary/secondary/accent + text/bg),
    typography (fonts + sizes + weights), spacing, border radius, button
    styles, input styles, and brand personality.
    """
    try:
        from firecrawl import Firecrawl  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            "firecrawl-py not installed. Run: pip install firecrawl-py"
        ) from e

    fc = Firecrawl(api_key=_api_key())
    result = fc.scrape(url=url, formats=["branding"])

    # Response shape (per Firecrawl docs):
    # { "success": true, "data": { "branding": {...}, "metadata": {...} } }
    # or directly { "branding": {...} } depending on SDK version
    if isinstance(result, dict):
        if "branding" in result:
            return result["branding"]
        if "data" in result and isinstance(result["data"], dict):
            return result["data"].get("branding", result["data"])

    # SDK may return an object with attribute access
    branding = getattr(result, "branding", None)
    if branding is not None:
        return branding if isinstance(branding, dict) else branding.__dict__

    raise RuntimeError(f"Unexpected Firecrawl response shape: {result}")


def extract_brand_with_fallback(url: str) -> dict:
    """
    Attempt the branding format, but fall back to markdown+screenshot if
    the site is JS-heavy or blocks standard scraping.
    """
    try:
        return extract_brand(url)
    except Exception as first_error:
        # Fallback: stealth proxy + markdown + screenshot, let Claude vision
        # extract the brand from the screenshot afterwards
        try:
            from firecrawl import Firecrawl  # type: ignore
        except ImportError:
            raise first_error

        fc = Firecrawl(api_key=_api_key())
        result = fc.scrape(
            url=url,
            formats=["branding", "markdown", "screenshot"],
            proxy="stealth",
        )
        if isinstance(result, dict):
            return result.get("branding") or result.get("data", {}).get("branding", {})
        return {}


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Firecrawl brand extraction")
    parser.add_argument("url", help="URL to extract brand from")
    parser.add_argument("--out", default="brand.json", help="Output JSON path")
    parser.add_argument(
        "--stealth",
        action="store_true",
        help="Use stealth proxy + fallback mode for JS-heavy sites",
    )
    args = parser.parse_args()

    brand = extract_brand_with_fallback(args.url) if args.stealth else extract_brand(args.url)
    Path(args.out).write_text(
        json.dumps(brand, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Saved: {args.out}")
    print(json.dumps(brand, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        _cli()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
