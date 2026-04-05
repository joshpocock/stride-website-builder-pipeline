# Phase 4c — Paper.design Graphic Exports

**Loaded on demand.** Only read this file if Paper.design MCP was detected in Phase 0 preflight, the HEAD check against `http://127.0.0.1:29979/mcp` confirmed Paper Desktop is running with a file open, and the user opted in. If Paper is not available, skip this sub-phase entirely.

## What and why

Paper.design is a code-native design tool with a local MCP server. Its primary positioning is UI layout → code, which overlaps with Stitch — and is *not* how we use it here. Instead, we use Paper's `get_screenshot` tool to export **composed graphics** from any node on the canvas as PNGs. This is useful for decorative section art, typographic compositions, custom brand patterns, or layered graphics the user has already designed in Paper and wants baked into the built site.

This is **complementary to Nano Banana / Gemini 3 Pro Image**, not competing. Paper exports are for things the user designed themselves (composed typography, layered shapes, branded patterns, custom iconography). Nano Banana / Gemini generate photorealistic imagery from prompts. Different jobs.

## Flow

### 1. Enumerate artboards

Paper's MCP only exposes the currently-open Paper file. Call `get_tree_summary` (or `get_basic_info` + `get_children` on the root) to list top-level artboards. Present them to the user:

> I see Paper is running with `{filename}` open. It contains these artboards: {list}. Want to use any of them as section graphics in the built site?

### 2. User selection with placement

For each artboard the user wants to use, ask two follow-up questions:

1. **Where should it go?** Dropdown of Q11 sections + "hero background" + "section divider" + "footer graphic" + "other" (free text)
2. **What size?** Default to 2x the target display size for retina sharpness

### 3. Export via screenshot

For each selected artboard, call Paper MCP `get_screenshot` with the node ID and requested size. Paper returns a PNG. Save to `{project_dir}/assets/graphics/{section_name}-{artboard_name}.png`.

Use a consistent naming convention so Phase 6 knows where each graphic belongs. Example:
- `hero-pattern-background.png`
- `about-section-divider.png`
- `footer-lockup.png`

### 4. Update the build prompt

Augment Phase 6's build prompt with:

> Additional graphics from Paper.design are available in `./assets/graphics/`. Each file is named `{section}-{description}.png` — place it in that section as a decorative element, section background, or accent graphic per the naming hint. These are pre-composed static images — do NOT regenerate or replace them with AI-generated alternatives.

## Cost and time

- **Cost:** $0. Local MCP, no network calls beyond localhost.
- **Time:** ~1 second per artboard export.

## Failure handling

If Paper stops responding mid-export (user closed the app, file was closed, or the MCP endpoint went away):

1. Stop cleanly — save whatever was exported so far
2. Tell the user: *"Paper stopped responding after exporting X of Y artboards. The exported ones are in assets/graphics/. Continuing to Phase 5."*
3. Continue to the next phase — do not block the pipeline

## See also

- `references/integration-verification.md` — Paper MCP setup, tool list, and gotchas
