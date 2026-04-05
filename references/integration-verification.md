---
type: verification
dateVerified: "2026-04-04"
---

# Integration Verification Report

Researched 2026-04-04 for the `stride-website-builder-pipeline` skill.

## Summary

| Integration | Verdict | Env Var |
|---|---|---|
| Firecrawl `branding` format | WORKS | `FIRECRAWL_API_KEY` |
| 21st.dev Magic MCP | WORKS | `API_KEY` (passed as arg) |
| Google Stitch MCP | LIMITED (Claude Code auth bug) | `STITCH_API_KEY` |
| Paper.design MCP | WORKS (local, no auth) | none (local server) |

---

## 1. Firecrawl `branding` format — WORKS

Firecrawl v1 scrape API supports `formats: ["branding"]` as a first-class output format. **Branding Format v2** (shipped late 2025) reliably handles logos in background images, Wix/Framer sites, and unusual HTML.

**Response includes:** logo, favicon, color palette (primary/secondary/accent + text/background), typography (font families, sizes, weights), spacing scale, border radius, button styles, input styles, and brand personality.

### Install / Auth
- `pip install firecrawl-py`
- Env var: `FIRECRAWL_API_KEY` (format `fc-...`)
- Free tier: 500 one-time credits
- Hobby: 3,000/mo at $16/mo billed yearly

### curl example
```bash
curl -X POST https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://stripe.com","formats":["branding"]}'
```

### Python example
```python
from firecrawl import Firecrawl
fc = Firecrawl(api_key=os.environ["FIRECRAWL_API_KEY"])
result = fc.scrape(url="https://stripe.com", formats=["branding"])
print(result["branding"])
```

### Gotchas
- Per-branding credit cost not listed (assume ~1 credit/page)
- Can combine with other formats in one call: `formats=["branding","markdown","screenshot"]`
- JS-heavy sites may need `proxy: "stealth"`

**Sources:**
- https://docs.firecrawl.dev/features/scrape
- https://www.firecrawl.dev/blog/branding-format-v2
- https://www.firecrawl.dev/pricing

---

## 2. 21st.dev Magic MCP — WORKS

Real MCP server maintained by 21st-dev. "v0 in your IDE" — generates UI component files via the `/ui` slash command.

### Install (one-liner for Claude Code)
```bash
npx @21st-dev/cli@latest install claude --api-key <YOUR_KEY>
```

### Manual config at `~/.claude/mcp_config.json`
```json
{
  "mcpServers": {
    "@21st-dev/magic": {
      "command": "npx",
      "args": ["-y", "@21st-dev/magic@latest", "API_KEY=\"your-api-key\""]
    }
  }
}
```

### Env var
Literally `API_KEY` passed as an arg (NOT `TWENTY_FIRST_DEV_API_KEY` — common mistake). Get key at https://21st.dev/magic/console.

### Workflow
Type `/ui create a pricing section with three tiers` — Magic picks components from the 21st.dev library and writes TSX files into your project.

### Free Tier
All features free during public beta. Component selection + file writing both work on free tier. Upgrade prompt appears on overuse (no hard monthly quota documented).

### Gotchas
- Works best on small/medium components — break complex UIs apart
- Beta pricing will change
- `API_KEY` arg name can collide with other shell env vars

**Sources:**
- https://github.com/21st-dev/magic-mcp
- https://mcp.harishgarg.com/use/21stdev-magic/mcp-server/with/claude-code

---

## 3. Google Stitch MCP — LIMITED

Official remote MCP server exists at `https://stitch.googleapis.com/mcp`. Designed primarily for Google Antigravity IDE, but documented for Claude Code, Cursor, and Gemini CLI. **Known auth bug in Claude Code — use stdio proxy workaround.**

### Path A — Direct HTTP (currently BROKEN in Claude Code)
```bash
claude mcp add --transport http stitch https://stitch.googleapis.com/mcp \
  --header "X-Goog-Api-Key: $STITCH_API_KEY"
```
Fails with: *"Incompatible auth server: does not support dynamic client registration."*

### Path B — Stdio proxy (RECOMMENDED)
Local Node.js proxy handles OAuth + token refresh. Follow https://stitch.withgoogle.com/docs/mcp/setup for the proxy script.

### Env Var
`STITCH_API_KEY` from Stitch settings, passed as `X-Goog-Api-Key` header. OAuth also supported via stdio proxy.

### Capabilities
Two-way sync — read Stitch designs (layers, components, auto-layout), generate React/Tailwind, push suggestions back to Stitch.

### Critical Gotcha
GitHub issue anthropics/claude-code#41664 — direct HTTP transport fails in Claude Code due to missing dynamic client registration support. Use stdio proxy until Anthropic adds DCR support.

### Alternatives that always work without MCP
- Stitch has a "Copy to Figma" button (preserves layers/auto-layout)
- Direct HTML+Tailwind export from the Stitch UI
- Community CLI: `github.com/davideast/stitch-mcp` for file-based workflow

**Sources:**
- https://stitch.withgoogle.com/docs/mcp/setup/
- https://codelabs.developers.google.com/design-to-code-with-antigravity-stitch
- https://github.com/anthropics/claude-code/issues/41664

---

---

## 4. Paper.design MCP — WORKS (local, no auth)

Paper is a modern design tool (macOS + Windows) with a local MCP server. The server is an authenticated API that lets LLMs read from and write to Paper design files — design token sync, content injection, design-to-code export.

### Install (one command)
```bash
claude mcp add paper --transport http http://127.0.0.1:29979/mcp --scope user
```

Verify with `/mcp` inside Claude Code — Paper should show in the list.

### Requirements
- Paper Desktop app installed and running
- A Paper file open (the MCP server only exposes the currently open file)
- No API key, no env var, no cloud account

### Capabilities (24 tools total)

**Read tools:**
- `get_basic_info`, `get_selection`, `get_node_info`, `get_children`, `get_tree_summary`
- `get_screenshot` — export a screenshot of any node
- `get_jsx` — export node as JSX/React
- `get_computed_styles` — full computed CSS
- `get_fill_image`, `get_font_family_info`, `get_guide`

**Write tools:**
- `create_artboard`, `write_html`, `set_text_content`
- `rename_nodes`, `duplicate_nodes`, `update_styles`, `delete_nodes`

**Status indicators:**
- `start_working_on_nodes`, `finish_working_on_nodes`

**Placement helper:** `find_placement`

### Use Cases for the Skill
- **Design-to-code**: user designs in Paper → skill calls `get_jsx` on the root artboard → injects into the build
- **Token sync**: extract design tokens from Paper and write to brand.json
- **Two-way iteration**: build in Claude Code → call `write_html` to push changes back into Paper
- **Alternative to Figma + Stitch** for designers who prefer Paper

### Gotchas
- Must have Paper Desktop running (not web)
- Works per-file (no multi-file support via MCP)
- macOS + Windows only
- Still early — expect some tool names/behaviors to change

**Source:** https://paper.design/docs/mcp

---

## Implementation Notes for stride-website-builder-pipeline

Based on this verification, the skill should:

1. **Firecrawl**: Use `pip install firecrawl-py` and the official `Firecrawl.scrape()` client with `formats=["branding"]` — NOT a custom extract schema. Simpler, better supported, and free tier is adequate for testing.

2. **21st.dev Magic MCP**: Update env template — the env var is `API_KEY` as a CLI arg, not `TWENTY_FIRST_DEV_API_KEY`. The install is a one-shot `npx @21st-dev/cli@latest install claude --api-key <KEY>`. Document the `/ui` slash command workflow.

3. **Google Stitch MCP**: Mark as LIMITED in the preflight check. Recommend the stdio proxy path by default (Path B) and the Antigravity direct-export fallback (Path C: "Copy to Figma" or HTML/Tailwind export) if the user doesn't want to set up the proxy. Do NOT use Path A (direct HTTP) in Claude Code until anthropics/claude-code#41664 is fixed.

4. **Paper.design MCP**: Add as an optional "Design Tool" integration. Preflight check: detect if the Paper Desktop app is running by attempting a HEAD request to `http://127.0.0.1:29979/mcp`. If found, offer the user the option to pull tokens/designs from Paper instead of (or alongside) Firecrawl brand extraction. Great for users who already use Paper as their design tool. No env var needed.
