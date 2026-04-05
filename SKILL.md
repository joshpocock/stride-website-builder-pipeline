---
name: stride-website-builder-pipeline
description: >
  Build a website or landing page — new projects OR adding a page to an existing
  codebase. Works for any tech stack (Next.js, Nuxt, Astro, SvelteKit, Remix,
  Vite, plain HTML) and any project type (landing page, multi-page site,
  portfolio, full app). Runs a short adaptive survey, extracts or picks a
  brand, generates hero images and optional scroll animation, builds the
  site with taste-skill + peer skills, runs a full SEO pass, and optionally
  deploys to Vercel/Netlify/Cloudflare. All phases have "let AI decide"
  escape hatches — user can go fast or stay in control.
  USE THIS SKILL WHENEVER the user asks to build, create, make, rebuild,
  scaffold, design, or add a website, landing page, marketing site, product
  page, portfolio, or similar — even if the phrasing is informal ("build me
  a site", "i wanna build a site", "make a landing page", "add a landing
  page to this repo", "design a site for [X]", "rebuild [url]", "help me
  build a website", "launch a site for [brand]", "put together a landing
  page", "throw up a site", "website for my business"). USE THIS SKILL EVEN
  IF THE PROJECT ALREADY EXISTS — Q1 has an "add to existing project" path
  that detects the stack and respects conventions. Do NOT default to
  generic "help with this existing project" mode when the user says
  anything about building, creating, or launching a website or landing
  page — activate this skill instead and let Phase 0 preflight handle the
  new-vs-existing decision.
---

# Website Builder Pipeline

Guided, survey-driven workflow for building premium animated websites end-to-end. Chains every tool and skill from the 2026 creator playbook into one interactive experience with pre-built prompts under the hood.

**Philosophy:** Claude is a collaborator, not autopilot. Survey first, confirm before executing, checkpoint at every phase. The user stays in the driver's seat.

**Who this is for:** Anyone who wants to build a $5K-$10K quality landing page in 15-30 minutes for $2-10 total cost, without manually chaining 8 different tools.

---

## Pipeline Phases

```
Phase 0: PREFLIGHT (env + skills + tools + MCP detection)
    ↓
Phase 1: SURVEY (13 adaptive questions)
    ↓ [user confirms plan]
Phase 2: BRAND EXTRACTION (Firecrawl / manual / screenshots / AI decides)
    ↓
Phase 2.5: STITCH LAYOUT GEN (optional — only if Stitch MCP detected)
    ↓
Phase 3: SKILL INSTALLATION (guided peer install)
    ↓
Phase 4: ASSET GENERATION (Wavespeed / Kie — images + Kling/Veo video)
    ↓   ↳ Phase 4c: PAPER GRAPHIC EXPORTS (optional — only if Paper MCP running)
Phase 5: PROJECT SCAFFOLD (skipped if Q1 = add-to-existing)
    ↓
Phase 6: BUILD (Claude Code + peer skills + Stitch scaffolds + 21st.dev components)
    ↓
Phase 6.5: VERIFY (agent-browser screenshots + a11y tree + fix loop)
    ↓
Phase 7: SEO PASS (JSON-LD, meta, sitemap, llms.txt, Lighthouse)
    ↓
Phase 7.5: VERIFY AGAIN (agent-browser re-check after SEO changes)
    ↓
Phase 8: DEPLOY (Vercel/Netlify CLI)
    ↓
Phase 8.5: PROD VERIFY (agent-browser against live URL)
    ↓
Phase 9: LEARNINGS LOG (self-improving)
```

---

## Phase 0: Preflight Check

Before asking any questions, run a preflight audit. Show the user what is ready vs. what needs setup.

1. Check for required CLIs: `ffmpeg`, `node`, `python`, `gh`, `vercel`, `netlify`, `lighthouse`
2. Check for environment variables (see `references/env-template.env`)
3. Check for installed peer skills: `taste-skill`, `front-end design`, `cc-nano-banana`, `mager/frontend-design`
4. Check for `brand.json` in current directory (if present, offer to reuse)
5. Check `~/.claude/website-builder/history.json` for prior runs (memory-aware)
6. **Detect registered MCPs.** Run `claude mcp list` and parse for three integrations:
   - **Stitch MCP** (tool names start with `mcp__stitch__`) — Google Stitch AI layout generator. If detected, enables Phase 2.5.
   - **Paper.design MCP** (tool names include `paper`) — then additionally HEAD-request `http://127.0.0.1:29979/mcp` with a 1-second timeout. Only counted as "available" if both the MCP is registered AND the endpoint responds (meaning Paper Desktop is actually running with a file open). If detected, enables Phase 4c.
   - **21st.dev Magic MCP** — premium component library. If detected, enables mid-Phase 6 component injection.
   For each detected MCP, present a one-line opt-in during the preflight confirmation: *"Stitch MCP detected — generate per-section layout scaffolds after brand extraction? [Y/n]"*. The user answers once; the skill remembers the choice for this run.

**Env var tiers:**
- **Required for any run:** one image provider (`WAVESPEED_API_KEY` *or* `KIE_AI_API_KEY`) — pipeline cannot generate hero assets without one.
- **Required only if user picks Q2 = "Existing URL":** `FIRECRAWL_API_KEY`. If missing when URL path is chosen, tell the user and let them switch to manual / screenshot / AI-decide path instead of blocking.
- **Optional:** everything else (Vercel, Netlify, Gemini, Google AI Studio). Their absence just disables that specific feature, never blocks the run.

Present results as a color-coded table:
- ✓ Ready (green)
- ⚠ Needs key (yellow)
- ✗ Not installed (red)

Offer "install all recommended" or let user cherry-pick. NEVER install automatically — always ask first.

If this is a repeat run, pre-fill the survey with the user's last answers from history.

---

## Phase 1: The Survey (13 Adaptive Questions)

Use `AskUserQuestion` for each step. Adapt — skip questions when answers from earlier questions make them unnecessary. Typical user answers 8–10 questions after adaptive skips.

See `references/survey-questions.md` for the full question spec with all options, adaptive rules, and escape hatches. Summary:

1. **Project type** — Landing / Multi-page / Full app / Portfolio / **Add to existing project**
2. **Tech stack** — Next.js / Nuxt / Astro / SvelteKit / Remix / Vite+React / Plain HTML / AI decides. *Skipped if Q1 = "Add to existing project"; stack is auto-detected from the repo.*
3. **Brand source** — URL (Firecrawl) / Manual / Screenshots / Build from scratch / Let AI decide
4. **Business info** — Company name, tagline, one-sentence description (pre-filled from Firecrawl if available)
5. **Target audience** — Free text
6. **Vibe archetype** — 6 presets + Custom + Let AI decide
7. **Color palette** — *Skipped if Q3 already provided colors*
8. **Font pairing** — *Skipped if Q3 already provided fonts*
9. **Hero images** — three sub-axes: **source** (AI generates / upload as-is / upload + AI edits / AI decides), **prompt** (AI writes from 6-stage Cinematic Frame Method / user writes / AI decides), **model** (auto-picked from env: Wavespeed Gemini 3 Pro → Kie Nano Banana Pro)
10. **Hero animation** — three sub-axes: **style** (exploded / orbit / dolly / pan / static / own MP4 / AI decides), **model** (Kling 3.0 / Veo 3.1 Fast / Veo 3.1 / Veo 3 Fast / Veo 3 / AI picks), **prompt** (AI writes / user writes / AI decides). *Q10b + Q10c skipped if style = static or own MP4*
11. **Sections** — multi-select with smart pre-selection from Q1 + Q6, plus a free-text "+ add your own" field for custom sections
12. **Deploy target** — Vercel / Netlify / Cloudflare / Manual / Skip
13. **SEO tier** — Full audit / Basic / Skip. **Never forced** — user's answer always wins, even for local service businesses (we only recommend).

After Q13, present the generated plan and wait for explicit confirmation before any execution.

**Adaptive rules (examples):**
- If Q1 = "Add to existing project" → skip Q2 tech stack, detect from repo; skip Phase 5 scaffold; Phase 6 build respects existing code conventions
- If Q3 = "Build from scratch" or "Let AI decide" → skip Q7 + Q8
- If Q10a = "Static" or "Own MP4" → skip Q10b + Q10c
- If Q9a = "Upload as-is" → skip Q9b prompt source
- If user provides a Figma file → skip Q7, Q8 entirely
- If Stitch MCP not detected → skip Phase 2.5 entirely; no mention to user
- If Paper MCP not running → skip Phase 4c entirely; no mention to user
- If 21st.dev Magic MCP not detected → skip mid-Phase 6 component injection; Claude builds all sections from scratch

**Removed from prior spec:** old Q12 budget tier (overlapped with provider-key detection), old Q13 integrations list (now auto-detected from env vars in Phase 0), old Q14 separate inspiration question (merged with Q4b above Q5).

**Escape hatches:** every question supports "skip this / paste manually / let me show you / let AI decide".

---

## Phase 2: Brand Extraction

Four possible paths based on Q2. `brand.json` is the single output format regardless of path — it IS the brand guidelines doc the rest of the pipeline reads from. Do not create a separate markdown brand guide; `brand.json` is canonical.

**Path A — Existing URL (requires `FIRECRAWL_API_KEY`):**

1. Read the URL
2. Call `references/call-firecrawl.py` with the URL and a custom extract schema for brand fields
3. Parse response into `brand.json`:
   ```json
   {
     "name": "...",
     "tagline": "...",
     "colors": {"primary": "#...", "secondary": "#...", "accent": "#...", "bg": "#..."},
     "fonts": {"heading": "...", "body": "..."},
     "logo_url": "...",
     "personality": ["..."]
   }
   ```
4. Show extracted brand to user, ask "any corrections?"

**Path B — Screenshots (no API key needed):** use Claude vision to extract the same fields from user-uploaded images and write `brand.json`. Uses the prompt in `references/build-prompts/brand-extract.md`.

**Path C — Manual (no API key needed):** ask the user for each field directly via `AskUserQuestion` — name, tagline, primary/secondary/accent/bg colors (hex), heading + body font, 3 personality adjectives. Write `brand.json` from their answers.

**Path D — Let AI decide (no API key needed):** user provides only company name + one-sentence description + target audience (already collected in Q3/Q4). Claude picks vibe, palette, and fonts from the vibe archetype that best matches the business, then writes `brand.json`. Show the AI-picked brand to user and let them tweak any field before proceeding. This is the "just do what it wants" escape hatch — useful when the user has no brand yet or doesn't care about design specifics.

**Firecrawl is NOT required for Paths B/C/D.** If `FIRECRAWL_API_KEY` is missing and the user picked Path A, surface the missing key and offer to switch to Path B, C, or D instead of blocking.

---

## Phase 2.5: Stitch Layout Generation (optional)

**Skip this phase entirely** if Stitch MCP was not detected in Phase 0 OR if the user declined the Stitch opt-in during preflight.

Stitch is Google's free AI-native UI design tool (powered by Gemini 3.1 Pro / Gemini 3 Flash). It generates themed HTML + Tailwind scaffolds per section. We use it as **structural scaffolding** for Phase 6 — not as finished code. Claude ports the Stitch output to the chosen tech stack and layers in animations, real images, taste-skill rules, and SEO.

**Flow:**

1. **Create a Stitch project.** Call `mcp__stitch__create_project` with `title = {{brand_name}}`. Capture the returned `projectId`.

2. **Map `brand.json` → Stitch design system.** Call `mcp__stitch__create_design_system` with `projectId` and a `DesignTheme` built from:
   - `customColor` ← `brand.colors.primary`
   - `overrideSecondaryColor` ← `brand.colors.secondary`
   - `overrideTertiaryColor` ← `brand.colors.accent`
   - `headlineFont` ← closest enum match to `brand.fonts.heading`. Supported enum: `GEIST`, `SPACE_GROTESK`, `INTER`, `MANROPE`, `PLUS_JAKARTA_SANS`, `DM_SANS`, `IBM_PLEX_SANS`, `SORA`, `MONTSERRAT`, `EB_GARAMOND`, `NEWSREADER`, `LITERATA`, `DOMINE`, `LIBRE_CASLON_TEXT`, `SOURCE_SERIF_FOUR`, `RUBIK`, `NUNITO_SANS`, `WORK_SANS`, `LEXEND`, `EPILOGUE`, `BE_VIETNAM_PRO`, `PUBLIC_SANS`, `METROPOLIS`, `SOURCE_SANS_THREE`, `HANKEN_GROTESK`, `ARIMO`, `SPLINE_SANS`, `NOTO_SERIF`. If the brand font isn't in the enum, pick the visually-closest match and record the real font name in `designMd`.
   - `bodyFont` ← same logic
   - `colorMode` ← `DARK` if `brand.colors.bg` has luminance < 0.3, else `LIGHT`
   - `colorVariant` ← mapped from Q6 vibe: Brutalist → `MONOCHROME`, Minimalist → `NEUTRAL`, Ethereal Glass → `TONAL_SPOT`, Soft Structuralism → `EXPRESSIVE`, Editorial Luxury → `FIDELITY`, Custom → `VIBRANT`
   - `roundness` ← mapped from vibe: Brutalist → `ROUND_FOUR`, Editorial Luxury → `ROUND_EIGHT`, Minimalist/Soft → `ROUND_TWELVE`, Ethereal Glass → `ROUND_FULL`
   - `designMd` ← free-form markdown describing the vibe archetype, the taste-skill dial tuning (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY), the banned patterns (no AI clichés, no Inter-as-heading, no 3-column equal rows), and the real brand font names if any had to fall back
3. Immediately call `mcp__stitch__update_design_system` to activate it on the project.

4. **Generate one screen per selected Q11 section.** For each section, call `mcp__stitch__generate_screen_from_text`:
   - `projectId` ← the one from step 1
   - `deviceType` ← `DESKTOP` (we generate mobile responsiveness in Phase 6)
   - `modelId` ← `GEMINI_3_1_PRO` (higher quality) or `GEMINI_3_FLASH` (faster) — default to Pro, fall back to Flash if the user hits rate limits
   - `prompt` ← templated string: *"{section_name} section for {brand_name}, a {brand.description}. Vibe: {vibe_archetype}. Audience: {target_audience}. {section-specific instructions from `references/build-prompts/stitch-section-prompts.md`}. Must include: {section_required_elements}. Avoid: centered hero unless Editorial Luxury, 3-column equal card rows, AI clichés like Elevate/Seamless/Unlock/Empower."*
   - Important: this call is async and "can take a few minutes." Run section generations **in parallel** where possible (multiple `generate_screen_from_text` tool calls in one assistant message) to keep total wall time under ~3 minutes for a 6-section landing page.

5. **Optional variants.** If the user opted in to "show me alternatives for key sections" during preflight, call `mcp__stitch__generate_variants` on the hero + pricing + CTA screens with `variantOptions = {variantCount: 3, creativeRange: EXPLORE, aspects: [LAYOUT, COLOR_SCHEME]}`. Skip variants by default — they triple generation time.

6. **User selection.** Call `mcp__stitch__list_screens` to enumerate everything generated. For each section, present the screen(s) to the user with a brief description pulled from `get_screen`, and ask them to pick one per section. Support "keep all" and "regenerate this one with feedback" via `edit_screens`.

7. **Extract HTML + Tailwind.** For each selected screen, call `mcp__stitch__get_screen` and pull the HTML + Tailwind output. Save to `{project_dir}/stitch-scaffold/{section_name}.html`.

8. **Hand off to Phase 6.** The Phase 6 build prompt is augmented with a new instruction block: *"Structural scaffolding is available in `./stitch-scaffold/`. For each section, the corresponding `.html` file is a Stitch-generated Tailwind layout themed to the brand. Port these to {{tech_stack}} components — preserve layout structure, spacing, and hierarchy — but ADD: scroll-bound hero animation (use `assets/hero.mp4`), real Nano Banana / Gemini hero images (replace any placeholder images), taste-skill anti-slop overrides, framework idioms (e.g., Next.js `<Image>` instead of `<img>`, Astro `.astro` components instead of raw HTML), semantic HTML5 landmarks, and responsive breakpoints Stitch didn't cover."*

**Cost:** $0 (Stitch is free, Google hosts the Gemini inference).

**Time:** 2-5 min without variants, 5-12 min with variants. Skill should tell the user the estimate before starting.

**Failure handling:** If any `generate_screen_from_text` call fails or times out, try once with `modelId = GEMINI_3_FLASH` as a fallback. If that also fails, skip that section — Phase 6 build will generate the layout from scratch for sections without a scaffold. Never block the whole pipeline on a Stitch failure.

**Reference:** See `references/build-prompts/stitch-section-prompts.md` for the per-section prompt templates.

---

## Phase 3: Skill Installation

Based on Q13 integrations + vibe archetype, determine which peer skills to install. See `references/recommended-skills.json`.

**The stacking rule: one skill per job, cap at three.** Each peer skill belongs to one of three functional slots:

1. **Rules + dials slot** — always `taste-skill`. Not an aesthetic opinion; it bans generic AI patterns and enforces premium ones via three tunable dials (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY).
2. **Aesthetic opinion slot** — pick exactly ONE based on the vibe archetype from Q11:
   - `mager/frontend-design` → dark neon SaaS, brutalist, minimalist
   - Anthropic official `front-end design` (modified) → polished animated product landing pages
   - `UIUX Pro Max` (nextlevelbuilder) → industry-specific UX refinement (medical, legal, fintech)
3. **Image generation tool slot** — `cc-nano-banana` if `GEMINI_API_KEY` is set, otherwise skip (pipeline still works; image gen happens via `call-kie.py` or `call-wavespeed.py`).

**NEVER stack multiple aesthetic-opinion skills.** Installing mager + front-end design + UIUX Pro Max at the same time gives Claude contradictory signals about type hierarchy, grid style, and motion intensity, and the build quality drops. The "10 skills not just taste" video narrative is about having the MENU to swap between projects, not about installing all of them at once.

**Always install (utility, non-opinion):**
- `agent-browser` (Vercel Labs) — critical for Phase 6.5 verification loop

**Optional opt-in (user must explicitly confirm):**
- Owl-Listener `designer-skills` bundle — only if the project needs research/strategy/design-ops depth beyond taste-skill; NEVER co-install with another aesthetic-opinion skill
- `TypeUI.sh` themes — design-file downloads, not a skill in the traditional sense
- `AccessLint` — WCAG compliance, safe to co-install (utility, not opinion), required if SEO tier is "Full Audit"
- `paper-design-mcp` — only if user is actively designing in Paper

**Skool-gated skills** (Nate Herk Video-to-Website, Jack Roberts 3D Builder) — flag as "manual install" with a link. Do not attempt automated install.

**Process:**
1. Check what's already installed (`.claude/skills/` in user home + project)
2. For each skill in the three slots above, if missing, show the exact install command to the user
3. Ask the user to confirm each install individually
4. Run the confirmed installs one at a time, verify each succeeded before moving on
5. NEVER silently auto-execute installs. NEVER batch-install without per-skill confirmation.

---

## Phase 4: Asset Generation

### 4a. Hero Start + End Frames

Generate two image prompts from the survey answers (product, vibe, brand colors) using `references/build-prompts/image-gen-nanobanana.md` as the fill-in template and `references/build-prompts/cinematic-frame-method.md` as the underlying framework for non-standard projects.

**Provider selection (check env vars in order):**

1. **If `WAVESPEED_API_KEY` is set → PREFERRED.** Use Gemini 3 Pro Image via `references/call-wavespeed.py`:
   - Model: `gemini-3-pro` (shortcut for `google/gemini-3-pro-image/text-to-image`)
   - Aspect ratio: `16:9`
   - Native 4K output (no upscale needed for retina desktop heroes)
   - Cost: ~$0.025/img
   - Batch: 4 variants per prompt
   - Why preferred: newest Gemini family model, genuine 4K native, cheaper than Nano Banana Pro on Wavespeed

2. **Else if `KIE_AI_API_KEY` is set → FALLBACK.** Use Nano Banana Pro via `references/call-kie.py`:
   - Model: `nanoBanana2` (or `nanoBananaPro` if the survey picked a premium tier)
   - Aspect ratio: `16:9`
   - Resolution: 2K
   - n_frames: N/A (image mode)
   - Batch: 4 variants per prompt
   - Safety rules from memory: do NOT use `quality` param on Kie.ai (breaks the request); use `size` (standard/high), `aspect_ratio`, `n_frames` (required for video)

3. **Else → ERROR.** Tell the user to set one of the two keys in `.env` before rerunning. Do not try to proceed without image generation.

Show all 8 generated images (4 start + 4 end) to user, ask them to pick one of each. Download picked ones to `project/assets/`.

### 4a.5 Lock-Pair Matching Pass (Wavespeed only)

**If Wavespeed was used for 4a**, run an additional pass through Nano Banana Pro Edit Multi via `call-wavespeed.py` to guarantee the picked start + end frames share identical lighting, color, and camera — this is critical for the Kling transition in 4b to look seamless.

```
python references/call-wavespeed.py lock-pair \
  --start <picked_start_url> \
  --end <picked_end_url> \
  --prompt "Match lighting, color temperature, and camera angle across these two frames exactly. Preserve the subject state in each (assembled in the first, exploded in the second). Keep the background and framing identical." \
  --out project/assets/
```

This writes `locked-start.webp` and `locked-end.webp` into the project assets folder. Use those as the inputs to Phase 4b instead of the raw picks.

**Skip this step if Kie.ai was used in 4a** — Kie.ai Nano Banana already includes internal coherence between variants in the same batch, so the locked-pair pass is redundant.

### 4b. Video Animation (Kling 3.0 / Veo 3 / Veo 3.1)

Pick the video model from Q10b. Kie.ai hosts all supported video models via `references/call-kie.py` (see its `VIDEO_MODELS` registry). Quick reference:

| Model (Q10b) | `--model` flag | Takes end frame? | Cost tier | Best for |
|---|---|---|---|---|
| Kling 3.0 | `kling3` | ✅ Yes | cheap | Scroll-bound hero with locked start/end (default) |
| Veo 3.1 Fast | `veo3.1-fast` | ❌ No | mid | Freeform hero motion, fast turnaround |
| Veo 3.1 | `veo3.1` | ❌ No | high | Premium freeform hero, slower render |
| Veo 3 Fast | `veo3-fast` | ❌ No | mid | Older Veo, mid quality |
| Veo 3 | `veo3` | ❌ No | high | Older Veo, high quality |

**Prompt generation (Q10c):**
- If user chose "AI writes" → fill `references/build-prompts/video-gen-kling.md` with survey answers
- If user chose "I'll write my own" → ask them for the prompt directly via `AskUserQuestion`
- If user chose "Let AI decide" → same as AI writes, but also auto-pick Q10b based on Q10a (exploded/orbit → Kling since those need locked start+end; dolly/pan → Veo 3.1 Fast)

**Call `call-kie.py video`:**
- `--start` → picked start frame URL (always)
- `--end` → picked end frame URL (only if model is Kling; ignored for Veo)
- `--prompt` → from the prompt step above
- `--duration` → 5
- `--aspect` → `16:9`
- `--model` → from Q10b

Download the MP4 to `project/assets/hero.mp4`. Run ffmpeg to extract a mobile still: `hero-mobile.jpg`.

**Cost budget:** Kling ~$0.50, Veo Fast ~$1.50, Veo full ~$4 per 5s clip. Full run budget: $2-10. Alert user if they hit $10.

### 4c. Paper.design Graphic Exports (optional)

**Skip this sub-phase entirely** if Paper.design MCP was not detected in Phase 0 (MCP not registered OR HEAD check to `http://127.0.0.1:29979/mcp` failed OR user declined the Paper opt-in during preflight).

Paper.design is a code-native design tool with a local MCP server. While its primary job is UI layout → code (which overlaps with Stitch and is NOT how we use it here), its `get_screenshot` tool lets us export composed graphics from any node on the canvas as PNGs — useful for decorative section art, typographic compositions, or custom brand graphics that the user has already designed in Paper but wants baked into the built site.

**Flow:**

1. **Enumerate artboards.** Call the Paper MCP's `get_tree_summary` (or `get_basic_info` + `get_children` on the root) to list top-level artboards in the currently-open Paper file. Paper's MCP only exposes the currently-open file, so tell the user: *"I see Paper is running with `{filename}` open. It contains these artboards: {list}. Want to use any of them as section graphics in the built site?"*

2. **User selection.** For each artboard the user wants to use:
   - Ask which section of the built site it should live in (dropdown of Q11 sections + "hero background" + "section divider" + "footer graphic" + "other")
   - Ask the desired output size (default: 2x the target display size for retina)

3. **Export via screenshot.** For each selected artboard, call Paper MCP `get_screenshot` with the node ID and size. Save the returned PNG to `{project_dir}/assets/graphics/{section_name}-{artboard_name}.png`.

4. **Update the build prompt.** Phase 6 build prompt is augmented: *"Additional graphics from Paper.design are available in `./assets/graphics/`. Each file is named `{section}-{description}.png` — place it in that section as a decorative element, section background, or accent graphic per the user's intent. These are pre-composed static images — do NOT regenerate or replace them with AI-generated alternatives."*

**Cost:** $0 (local MCP, no network calls beyond localhost).

**Time:** ~1 second per artboard export.

**Failure handling:** If Paper stops responding mid-export (user closed the app, file was closed), stop cleanly — save whatever was exported so far, tell the user, and continue to Phase 5. Do not block the pipeline.

**Why this is complementary, not competing, with Nano Banana / Gemini:** Paper exports are for things the user *designed themselves* — composed typography, layered shapes, branded patterns, custom iconography. Nano Banana / Gemini generate photorealistic imagery from prompts. Different jobs, no overlap.

---

## Phase 5: Project Scaffold

**Skip this entire phase if Q1 = "Add to existing project".** Instead: `cd` to the user-provided project root, detect the existing tech stack (look for `package.json`, `astro.config.*`, `svelte.config.*`, `next.config.*`, `remix.config.*`, `vite.config.*`, plain `index.html`), read existing conventions (component folder structure, CSS approach, routing pattern), and drop `brand.json` + `assets/` into a sensible location inside the existing repo (typically `public/brand.json` and `public/assets/` or `src/assets/`). Do NOT overwrite existing files without explicit confirmation.

For new projects, run `references/scaffold-project.py` to create:

```
project-name/
├── .env                    # Populated from survey + user's existing keys
├── brand.json              # From Phase 2
├── inspiration/            # Any competitor URLs/screenshots from Q14
│   ├── source-1.html       # From view-page-source.com
│   └── screenshot-1.png
├── assets/
│   ├── hero.mp4            # From Kling
│   ├── hero-mobile.jpg     # ffmpeg still
│   ├── start-frame.webp    # From NanoBanana
│   └── end-frame.webp
├── README.md               # Survey summary + next steps
└── build-plan.md           # The master prompt that will drive the build
```

Pre-populate `.env` with:
- User's existing keys (from environment or prior runs)
- Placeholders for missing keys
- Comments explaining which keys are required vs optional

### Install script fallback

Scaffolders (`create-next-app`, `nuxi init`, `npm create astro`, `npm create svelte`, `npm create vite`, `create-remix`) sometimes prompt interactively or hang waiting for input when Claude Code runs them. **Always pass non-interactive flags** so the scaffold runs clean:

- Next.js: `npx create-next-app@latest {name} --ts --tailwind --app --src-dir --import-alias "@/*" --no-eslint --use-npm --yes`
- Nuxt: `npx nuxi@latest init {name} --packageManager npm --gitInit false --force`
- Astro: `npm create astro@latest {name} -- --template minimal --typescript strict --install --no-git --yes`
- SvelteKit: `npm create svelte@latest {name} -- --template skeleton --types ts --no-prettier --no-eslint --no-playwright --no-vitest`
- Vite: `npm create vite@latest {name} -- --template react-ts`
- Remix: `npx create-remix@latest {name} --template remix-run/remix/templates/remix --install --no-git-init --yes`

**If the scaffolder still fails** (network error, prompt can't be bypassed, version mismatch), do NOT keep retrying. Stop and print the exact command for the user to run manually in their own terminal, then wait for them to confirm it finished before continuing to Phase 6. Tell them: "I couldn't run `<command>` non-interactively. Please run it yourself and reply 'done' when the folder is created." This keeps the skill unblocked without making the user debug a subprocess failure.

---

## Phase 6: Build

**If Q1 = "Add to existing project":** use `site-build-premium.md` as a guide but adapt to the existing codebase — match the detected stack's patterns, reuse existing components where possible, and stay inside the user's folder conventions. Never refactor unrelated code.

Otherwise, read `references/build-prompts/site-build-premium.md` (for premium tier) or `site-build-minimal.md` (for simpler runs) and fill in template variables from the survey:
- `{{brand_name}}`, `{{tagline}}`, `{{colors}}`, `{{fonts}}`
- `{{vibe}}`, `{{motion_intensity}}`, `{{design_variance}}`, `{{visual_density}}`
- `{{sections}}`, `{{animation_type}}`
- `{{inspiration_refs}}`

The filled prompt invokes Claude Code with:
- taste-skill active with tuned dials
- front-end design skill active
- Reference to brand.json, assets/, inspiration/
- Stitch scaffold folder (`./stitch-scaffold/`) if Phase 2.5 ran
- Paper graphic exports (`./assets/graphics/`) if Phase 4c ran
- Plan Mode first (Nate Herk strategy)

**Critical: Use the Plan Mode → Bypass Permissions workflow.** The skill should instruct Claude Code to enter Plan Mode, show the plan, wait for user approval, then execute.

### Mid-build: 21st.dev Magic MCP component injection (optional)

**Only applies if 21st.dev Magic MCP was detected in Phase 0 and the user opted in during preflight.**

21st.dev Magic is a premium component library exposed as an MCP — it returns production-ready React/Tailwind components for common landing-page patterns (pricing tables, testimonial carousels, feature grids, footers, nav bars). Instead of having Claude build these from scratch, the skill can inject 21st.dev components into sections where a good premade exists.

**Which sections benefit:** Pricing, Testimonials, Features (only for grid-heavy patterns), FAQ, Footer, Nav. Do NOT use 21st.dev for Hero — hero is too brand-specific and the cinematic animation path makes premades wrong-fit.

**Flow during Phase 6 build:**

1. After Claude enters Plan Mode but before executing, the plan should list which sections will use 21st.dev components vs which will be custom-built.
2. For each 21st.dev-eligible section, Claude calls the 21st.dev Magic MCP search/fetch tool with a prompt describing the section's needs (brand colors from `brand.json`, vibe from Q6, content from `brand.json` or survey).
3. 21st.dev returns 1-3 component options. Claude picks the best fit or asks the user if preference is ambiguous.
4. The component is inserted into the build, then styled to match brand tokens (colors, fonts, spacing from the design system).
5. Claude logs which sections used 21st.dev vs custom in `build-log.md` for the Phase 9 learnings step.

**Conflict handling:** If Phase 2.5 Stitch scaffolds exist for a section AND 21st.dev has a component for it, 21st.dev wins for Pricing/Testimonials/Footer/Nav (components beat scaffolds for standardized patterns) and Stitch wins for Hero/Features/About/Custom sections (scaffolds beat components for brand-specific layouts). Document the choice in the plan so the user can override.

Dev server spins up when done. User verifies, gives feedback, skill iterates.

---

## Phase 7: SEO Optimization Pass

Read `references/build-prompts/seo-pass.md` and invoke it on the built site.

The SEO pass does:

1. **Meta tags** — title, description, OG, Twitter Card, canonical
2. **JSON-LD schemas** — Organization, LocalBusiness, Service, FAQ, Review (conditional on survey)
3. **Files** — generate `robots.txt`, `sitemap.xml`, `llms.txt`
4. **Images** — convert to AVIF/WebP, rename descriptively, add alt text, `loading="lazy"`, `fetchpriority="high"` on hero
5. **Semantic HTML5** — ensure `<main>`, `<article>`, `<section>`, `<nav>`, `<header>`, `<footer>` landmarks
6. **Core Web Vitals** — verify LCP <2.5s, CLS <0.1, INP <200ms
7. **Lighthouse audit** — run `lighthouse --output=json` via CLI, report scores
8. **Analytics injection (conditional on env vars, silent if unset):**
   - If `GA4_MEASUREMENT_ID` is set → inject the GA4 gtag snippet into `<head>`:
     ```html
     <script async src="https://www.googletagmanager.com/gtag/js?id={{GA4_MEASUREMENT_ID}}"></script>
     <script>
       window.dataLayer = window.dataLayer || [];
       function gtag(){dataLayer.push(arguments);}
       gtag('js', new Date());
       gtag('config', '{{GA4_MEASUREMENT_ID}}');
     </script>
     ```
   - If `PLAUSIBLE_DOMAIN` is set → inject the Plausible snippet into `<head>`:
     ```html
     <script defer data-domain="{{PLAUSIBLE_DOMAIN}}" src="https://plausible.io/js/script.js"></script>
     ```
   - Both can be set simultaneously — inject both. If neither is set, skip this step silently (no user-facing message, no error). Log which were injected in `build-log.md` for Phase 9.

Full 2026 SEO reference lives at `references/seo-research-2026.md`.

User sees the Lighthouse scores and any issues before deploy.

---

## Phase 8: Deploy

Based on Q11:

- **Vercel:** `vercel --prod` (after `gh repo create` + git push)
- **Netlify:** `netlify deploy --prod`
- **Cloudflare Pages:** `wrangler pages deploy`
- **Manual:** skip deploy, show build output dir

Confirm URL works, show final metrics, celebrate.

---

## Phase 9: Learnings Log

After successful deploy, ask:

```
What worked well? What would you change? Anything to tune for next time?
```

Append the user's answers + the survey answers + final metrics to `~/.claude/website-builder/history.json`. Next run pre-fills the survey with these preferences.

Also offer to update specific `build-prompts/*.md` files with learnings (Nate Herk self-improving pattern).

---

## Key Files

| File | Purpose |
|---|---|
| `references/survey-questions.md` | Full survey spec with adaptive rules |
| `references/vibe-archetypes.md` | 6 preset aesthetics with dials + sample references |
| `references/env-template.env` | All env vars the skill can use |
| `references/recommended-skills.json` | Peer skills + install commands |
| `references/call-kie.py` | Kie.ai API wrapper (Nano Banana + Kling) — fallback image provider, always used for video |
| `references/call-wavespeed.py` | Wavespeed API wrapper (Gemini 3 Pro Image + Nano Banana Pro Edit Multi) — preferred image provider when `WAVESPEED_API_KEY` is set |
| `references/call-firecrawl.py` | Firecrawl brand extraction |
| `references/scaffold-project.py` | Project folder creator |
| `references/seo-research-2026.md` | Deep SEO 2026 playbook |
| `references/build-prompts/brand-extract.md` | Vision extraction prompt (screenshots → brand.json) |
| `references/build-prompts/image-gen-nanobanana.md` | NanoBanana prompt template (fill-in) |
| `references/build-prompts/cinematic-frame-method.md` | 6-layer cinematic prompt framework (ANCHOR/WORLD/LUMINANCE/AIR/OPTICS/EXCLUSIONS) + locked-pair workflow |
| `references/build-prompts/video-gen-kling.md` | Kling prompt template |
| `references/build-prompts/site-build-premium.md` | Master build prompt (full stack) |
| `references/build-prompts/site-build-minimal.md` | Master build prompt (free tier) |
| `references/build-prompts/seo-pass.md` | Full SEO audit + fix prompt |
| `references/build-prompts/verify-build.md` | agent-browser visual verification + fix loop |
| `references/build-prompts/deploy-vercel.md` | Deploy orchestration prompt |
| `references/build-prompts/stitch-section-prompts.md` | Per-section Stitch prompt templates for Phase 2.5 |
| `references/design-inspiration.md` | Curated Dribbble/Godly/Pinterest links |
| `references/integration-verification.md` | Verified integrations (Firecrawl, 21st.dev Magic MCP, Stitch MCP, Paper.design MCP) |

---

## Quick Commands

Instead of running the full pipeline, invoke individual phases:

| Command | What it does |
|---|---|
| "preflight" | Phase 0 only — check env/skills/tools |
| "extract brand from [url]" | Phase 2 only |
| "generate hero animation for [brand]" | Phase 4 only |
| "seo pass on [dir]" | Phase 7 only |
| "deploy [dir] to vercel" | Phase 8 only |
| "rebuild [competitor url]" | Full pipeline w/ HTML scaffolding |

---

## Safety & Cost Guardrails

- **Always confirm before:** API calls that cost money, installing skills, running deploy, overwriting files
- **Budget cap:** alert if a single run exceeds $10 in API costs
- **Never:** skip the Plan Mode checkpoint, auto-commit to git, push to prod without user approval
- **Always:** persist `.env` at project root (never to skill folder), keep `brand.json` as backup, log everything for self-improvement

---

## Differentiators (What This Does That Competitors Don't)

1. **One-shot execution** — competitors describe the process in videos; this skill executes it
2. **Pre-built battle-tested prompts** — distilled from 13 creator videos, no prompt engineering required
3. **Auto brand extraction** — no manual JSON writing from Firecrawl dashboard
4. **Auto API calls** — no browser-hopping between Higgsfield, Kie.ai, Google AI Studio
5. **Full SEO baked in** — most creators skip SEO entirely
6. **Memory-aware** — learns your preferences across runs
7. **Self-improving** — prompts get better with every project
8. **Screenshot-driven** — answer any question with an image via Claude vision
9. **Competitor scaffolding** — view-page-source.com integration for structural copying
10. **Vibe archetypes** — 6 premium presets that bundle font/color/motion/dial tuning

Ship version 1.0 with the Stride AI Academy video. Iterate publicly based on community feedback.
