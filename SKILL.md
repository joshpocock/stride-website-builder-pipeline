---
name: stride-website-builder-pipeline
description: Use whenever the user says "build a site", "i wanna build a site", "make a landing page", "add a landing page", "throw up a site", "rebuild [url]", or similar. Builds a website or landing page in new OR existing projects — don't default to generic code help.
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

**Start Phase 0 immediately on activation.** Do not ask clarifying questions before running preflight — the Phase 1 survey collects every piece of information the skill needs (project type, tech stack, brand source, vibe, sections, deploy target, SEO tier, and more). Asking upfront questions like "what kind of site?" or "what do you want on it?" before loading this SKILL.md duplicates work the skill already does and wastes the user's turns. Load straight into the status audit below.

Before asking any questions, run a preflight audit. Show the user what is ready vs. what needs setup.

1. Check for required CLIs: `ffmpeg`, `node`, `python`, `gh`, `vercel`, `netlify`, `lighthouse`
2. **Check for environment variables across multiple sources** (see `references/env-template.env` for the full list). Load values in this order, with earlier sources winning:
   1. **Shell environment** (`process.env`) — primary source
   2. **`.env` in the current working directory** — if present, parse and merge any keys that weren't already set in the shell
   3. **`.env` in parent directories up to the project root** — walk upward from cwd until hitting a `.git/`, `package.json`, `pyproject.toml`, or 3 levels up; merge any `.env` files found along the way
   4. **`.env` in the skill's own root directory** — `~/.claude/skills/stride-website-builder-pipeline/.env` for user-scope installs, or `<project>/.claude/skills/stride-website-builder-pipeline/.env` for project-scope installs. Merge as the lowest-priority fallback.

   Why this matters: users commonly keep their keys in a `.env` file rather than exporting them to the shell every session. If Phase 0 only checks `process.env`, legitimate keys will look unset and the preflight will misreport. Always check files too. Shell values always win over file values so users can temporarily override a key without editing files.

   Implementation: run `cat ./.env 2>/dev/null`, `cat ../.env 2>/dev/null`, and `cat <skill-root>/.env 2>/dev/null`, parse each for `KEY=value` lines, and merge into a working env dict. Do NOT modify the user's shell. Only use the merged dict for this Phase 0 status check and for passing to the script subprocesses that need keys (e.g., `scripts/call-wavespeed.py`).
3. Check for installed peer skills: `taste-skill`, `front-end design`, `cc-nano-banana`, `mager/frontend-design`
4. Check for `brand.json` in current directory (if present, offer to reuse)
5. Check `~/.claude/website-builder/history.json` for prior runs (memory-aware)
6. **Detect registered MCPs.** Run `claude mcp list` and parse for three integrations:
   - **Stitch MCP** (tool names start with `mcp__stitch__`) — Google Stitch AI layout generator. If detected, enables Phase 2.5.
   - **Paper.design MCP** (tool names include `paper`) — then additionally HEAD-request `http://127.0.0.1:29979/mcp` with a 1-second timeout. Only counted as "available" if both the MCP is registered AND the endpoint responds (meaning Paper Desktop is actually running with a file open). If detected, enables Phase 4c.
   - **21st.dev Magic MCP** — premium component library. If detected, enables mid-Phase 6 component injection.
   For each detected MCP, ask the user explicitly via `AskUserQuestion` (do not just show it in the status table — present each as a yes/no question the user must actively answer): *"Stitch MCP detected — generate per-section layout scaffolds after brand extraction? [Y/n]"*. The user answers once; the skill remembers the choice for this run.
7. **Smoke-test provider scripts.** Script rot is real — a production run in April 2026 found `call-kie.py` completely broken because the Kie.ai API surface changed. Instead of trusting file-exists as "green," run one cheap read call per provider:
   - **Wavespeed:** `curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $WAVESPEED_API_KEY" $BASE_URL/models` or similar model-list endpoint. If 200 → ✓; if 4xx/5xx → ⚠ "Wavespeed API returned {code} — script may be stale"
   - **Kie.ai:** `curl -s -H "Authorization: Bearer $KIE_AI_API_KEY" https://api.kie.ai/api/v1/chat/credit`. If `{"code":200}` → ✓; else → ⚠ "Kie.ai credit check failed — script may be stale"
   - **Firecrawl:** `curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $FIRECRAWL_API_KEY" https://api.firecrawl.dev/v1/scrape -X POST -d '{}'`. If 400 (bad request but auth worked) → ✓; if 401/403 → ⚠ "Firecrawl auth failed"
   Total cost: $0 (read-only calls, no generation). Total time: <3 seconds. If any provider flags ⚠, tell the user which script is suspect and recommend checking the script's header comments for known issues before relying on that provider in later phases.

**Env var tiers:**
- **Required for any run:** one image provider (`WAVESPEED_API_KEY` *or* `KIE_AI_API_KEY`) — pipeline cannot generate hero assets without one.
- **Required only if user picks Q2 = "Existing URL":** `FIRECRAWL_API_KEY`. If missing when URL path is chosen, tell the user and let them switch to manual / screenshot / AI-decide path instead of blocking.
- **Optional:** everything else (Vercel, Netlify, Gemini, Google AI Studio). Their absence just disables that specific feature, never blocks the run.

Present results as a color-coded table:
- ✓ Ready (green)
- ⚠ Needs key (yellow)
- ✗ Not installed (red)

Offer "install all recommended" or let the user cherry-pick. Always ask before installing anything — auto-installing skills or tools on someone's machine without consent is a trust violation that's hard to recover from, and a one-sentence confirmation is cheap.

If this is a repeat run, pre-fill the survey with the user's last answers from history.

---

## Phase 1: The Survey (13 Adaptive Questions)

Use `AskUserQuestion` for each step. Adapt — skip questions when answers from earlier questions make them unnecessary. Typical user answers 8–10 questions after adaptive skips.

See `references/survey-questions.md` for the full question spec with all options, adaptive rules, and escape hatches. Summary:

1. **Project type** — Landing / Multi-page / Full app / Portfolio / **Add to existing project**
   - **Q1b follow-up if "Add to existing project"**: pick a mode — **Add** (preserve code, extend), **Rebuild** (keep infrastructure, rewrite UI), or **Replace** (archive everything, start fresh in the same repo). Always ask — do not default. Rebuild and Replace delete/move files and must run inside Plan Mode with the file list surfaced before approval.
2. **Tech stack** — Next.js / Nuxt / Astro / SvelteKit / Remix / Vite+React / Plain HTML / AI decides. *Skipped if Q1 = "Add to existing project" (any mode); stack is auto-detected from the repo.*
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
2. Call `scripts/call-firecrawl.py` with the URL and a custom extract schema for brand fields
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

**Skip this phase if Stitch MCP was not detected in Phase 0 or the user declined.** If active, Stitch (Google's free AI UI design tool, Gemini 3.1 Pro) generates themed HTML + Tailwind scaffolds per section. We use them as structural scaffolding for Phase 6 — Claude ports the output to the chosen tech stack and layers in animations, real images, and taste-skill rules. $0 cost, 2-5 min typical (5-12 with optional variants).

**Read `references/phases/phase-2-5-stitch.md` for the full flow** — brand.json → Stitch `DesignTheme` mapping (font enum, color variant, roundness), per-section `generate_screen_from_text` calls, parallelization, variants, user selection, and Phase 6 handoff.

---

## Phase 3: Skill Installation

**Do not skip this phase.** Even if the user didn't mention skills, check what's installed and ask about anything missing. This phase runs every time — it's not gated on a survey question.

**Installation scope: project-only.** All skill installs go into the current project's `.claude/skills/` or `.agents/skills/` directory — never into the user-scope `~/.claude/skills/`. The pipeline should not pollute other projects with skills that are only relevant to this build. If a skill is already installed at user scope, that's fine (it'll be detected in the scan), but new installs always target project scope.

**Step 1 — Scan what's already installed.** List the contents of `~/.claude/skills/`, `<project>/.claude/skills/`, and `<project>/.agents/skills/`. Note which of the slot skills are present in any of these locations.

**Step 2 — Check each slot and ask via `AskUserQuestion` for any missing critical skill.** See `references/recommended-skills.json` for install commands and details.

**Slot 1 — Rules + dials (always `taste-skill`):**
If `taste-skill` is not in the installed list, ask explicitly:
> taste-skill is not installed. It's the anti-slop ruleset that prevents generic AI patterns and gives you 3 tunable dials (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY). Every build is better with it.
> Install into this project? `git clone https://github.com/Leonxlnx/taste-skill .claude/skills/taste-skill` [Y/n]

**Slot 2 — Aesthetic opinion (pick ONE based on vibe):**
Check if any of these are already installed: `frontend-design`, `mager/frontend-design`, `uiux-pro-max`. If one is present, confirm it's the right pick for this project's vibe. If none are present, recommend one based on vibe and ask:
- Trustworthy / service / local business → recommend Anthropic `frontend-design` (`git clone` from `https://github.com/anthropics/skills` → copy `skills/frontend-design` into `.claude/skills/frontend-design`) or `UIUX Pro Max`
- Dark neon / SaaS / brutalist / minimalist → recommend `mager/frontend-design` (`git clone https://github.com/mager/frontend-design .claude/skills/frontend-design`)
- Animated product landing → recommend Anthropic `frontend-design`

Don't stack multiple aesthetic-opinion skills — they give contradictory signals about type hierarchy and the output gets muddy. One per project.

**Slot 3 — Utility:**
If `agent-browser` is not installed, ask:
> agent-browser (Vercel Labs) is not installed. It's used in Phase 6.5 for automated visual verification — desktop/mobile screenshots, accessibility tree checks, and a self-correcting fix loop.
> Install into this project? `git clone https://github.com/vercel-labs/agent-browser .claude/skills/agent-browser` [Y/n]

**Step 3 — Run confirmed installs one at a time.** After each install, verify it succeeded (check the skills directory for the new folder) before moving to the next. If an install fails, tell the user the error and offer to skip that skill — don't block the pipeline.

**Skills NOT to auto-install (mention as "manual install" only if the user asks):**
- Skool-gated skills (Nate Herk Video-to-Website, Jack Roberts 3D Builder) — community-only, require manual download
- Owl-Listener `designer-skills` bundle — heavy (63 skills), only if the user specifically wants research/strategy/design-ops depth
- `TypeUI.sh` themes — design-file downloads from typeui.sh, not a git-installable skill
- `AccessLint` — WCAG compliance, safe to co-install, mention only if SEO tier = "Full Audit"

---

## Phase 4: Asset Generation

### 4a. Hero Start + End Frames

Generate two image prompts from the survey answers (product, vibe, brand colors) using `references/build-prompts/image-gen-nanobanana.md` as the fill-in template and `references/build-prompts/cinematic-frame-method.md` as the underlying framework for non-standard projects.

**Provider selection (check env vars in order):**

1. **If `WAVESPEED_API_KEY` is set → PREFERRED.** Use Gemini 3 Pro Image via `scripts/call-wavespeed.py`:
   - Model: `gemini-3-pro` (shortcut for `google/gemini-3-pro-image/text-to-image`)
   - Aspect ratio: `16:9`
   - Native 4K output (no upscale needed for retina desktop heroes)
   - Cost: ~$0.025/img
   - **Gemini 3 Pro returns exactly 1 variant per call** regardless of `--n`. For N variants, issue N separate `generate_image()` calls with different `--seed` values (costs N × $0.025). This is a Gemini 3 Pro limitation — other Wavespeed models (Nano Banana Pro, Gemini 2.5 Flash) do support true --n batching.
   - Why preferred: newest Gemini family model, genuine 4K native

2. **Else if `KIE_AI_API_KEY` is set → FALLBACK.** Use Nano Banana Pro via `scripts/call-kie.py`:
   - Model: `nanoBanana2` (or `nanoBananaPro` if the survey picked a premium tier)
   - Aspect ratio: `16:9`
   - Resolution: 2K
   - Batch: up to 4 variants per call (true batching works here)
   - **Note:** `call-kie.py` is partially broken as of April 2026 (the Kie.ai API surface changed). Image generation may work with the corrected BASE_URL but is unverified. See the warning block at the top of the file. If it fails, fall back to Wavespeed even for non-preferred paths.
   - Safety rules: do NOT use `quality` param on Kie.ai (breaks the request); use `size` (standard/high), `aspect_ratio`

3. **Else → ERROR.** Tell the user to set one of the two keys in `.env` before rerunning. Do not try to proceed without image generation.

Show generated images to the user (4 start variants + 4 end variants if using true batching, or 1 of each if Gemini 3 Pro), ask them to pick one of each. Offer to regenerate with feedback if none are satisfactory. Download picked ones to `project/assets/`.

### 4a.5 Lock-Pair Matching Pass — CURRENTLY BROKEN (skip)

**⚠️ The `lock_pair()` function in `call-wavespeed.py` returns HTTP 400 as of April 2026.** The nano-banana-pro/edit-multi parameter schema drifted (suspected: `images` field name, `num_images`, or `aspect_ratio` changed). The function is deprecated with a clear `NotImplementedError` until the correct body shape is re-verified.

**Workaround:** skip the lock-pair step entirely. Generate start + end frames with consistent prompts (same scene, same lighting, same camera angle described in text) and different subject states. Rely on prompt consistency to carry coherence across the pair. The downstream video transition (Seedance / Kling) will still work — the transition will just be slightly less visually locked between the two frames than with a verified lock-pair pass. For most landing pages, the quality difference is negligible.

### 4b. Video Animation (Seedance / Veo 3 via Wavespeed)

Pick the video model from Q10b. **Use `scripts/call-wavespeed.py video`** for all video generation — the Kie.ai video path is broken as of April 2026. See `VIDEO_MODELS` registry in `call-wavespeed.py` for the full list.

**Verified working models on Wavespeed (April 2026):**

| Model (Q10b) | `--model` flag | Takes end frame? | Duration | Best for |
|---|---|---|---|---|
| Seedance v1 Pro | `seedance-pro` | ✅ Yes (via `last_image`) | any | Scroll-bound hero with start+end frames (**default**) |
| Seedance v1 Lite | `seedance-lite` | ✅ Yes | any | Same as Pro, cheaper, lighter quality |
| Veo 3 Fast | `veo3-fast` | ❌ No | 4, 6, or 8s only | Freeform hero motion from single frame |

**Not available on Wavespeed:** Kling models returned "model not found" on all tested path patterns (`kwaivgi/kling-v2-1-master/image-to-video`, `kwaivgi/kling-v2-master/image-to-video`). Kling is currently only on Kie.ai, and Kie.ai's video endpoint is broken. If start+end frame interpolation is needed, use Seedance Pro — it supports both frames.

**Prompt generation (Q10c):**
- If user chose "AI writes" → fill `references/build-prompts/video-gen-kling.md` with survey answers (the prompt template works for any i2v model, not just Kling)
- If user chose "I'll write my own" → ask them for the prompt directly via `AskUserQuestion`
- If user chose "Let AI decide" → auto-pick model based on Q10a (exploded/orbit → Seedance Pro since those need locked start+end; dolly/pan → Veo 3 Fast for freeform)

**Call `call-wavespeed.py video`:**
- `--start` → picked start frame URL (always — use the `URL:` line printed by the image subcommand, not the local path)
- `--end` → picked end frame URL (only for Seedance models; Veo doesn't support end frames)
- `--prompt` → from the prompt step above
- `--duration` → 5 (Seedance) or 4/6/8 (Veo 3 Fast — other values rejected)
- `--aspect` → `16:9`
- `--model` → from Q10b

Download the MP4 to `project/assets/hero.mp4`. Run ffmpeg to extract a mobile still: `hero-mobile.jpg`.

**Cost budget:** Seedance Pro ~$0.50, Veo Fast ~$1.50 per clip. Full run budget: $2-10. Alert user if they hit $10.

### 4c. Paper.design Graphic Exports (optional)

**Skip this sub-phase if Paper.design MCP was not detected, not running, or the user declined.** If active, Paper's `get_screenshot` tool exports composed graphics from the currently-open Paper file as PNGs — useful for decorative section art, typographic compositions, and custom brand graphics the user already designed. Complementary to Nano Banana / Gemini, not competing (those generate photorealistic imagery from prompts; Paper exports user-composed visuals). $0 cost, ~1 sec per export.

**Read `references/phases/phase-4c-paper.md` for the full flow** — artboard enumeration, user placement selection, `get_screenshot` export, build prompt augmentation, and failure handling.

---

## Phase 5: Project Scaffold

Behavior depends on Q1 + Q1b:

- **Q1 = new project** (Landing / Multi-page / Full app / Portfolio) → run the normal scaffold flow below using `scripts/scaffold-project.py`.
- **Q1 = "Add to existing project", Q1b = Add** → skip scaffold. `cd` to the user-provided project root, detect the existing tech stack (`package.json`, `astro.config.*`, `svelte.config.*`, `next.config.*`, `nuxt.config.*`, `remix.config.*`, `vite.config.*`, plain `index.html`), read existing conventions (component folder layout, CSS approach, routing pattern), and drop `brand.json` + `assets/` into a sensible location inside the existing repo (typically `public/brand.json` and `public/assets/` or `src/assets/`). Never overwrite existing files without explicit confirmation.
- **Q1 = "Add to existing project", Q1b = Rebuild** → skip scaffold creation, but do the detection work (stack, conventions, preserved infrastructure). Phase 6 handles the tear-down-and-rewrite step with a file deletion list in Plan Mode. Drop `brand.json` + `assets/` in the same location as Add mode.
- **Q1 = "Add to existing project", Q1b = Replace** → run the in-place archive-then-scaffold flow. First move everything except `.git/`, `node_modules/`, and `.env*` files into `./archive-{YYYY-MM-DD-HHMM}/` (use the current timestamp, UTC). Then run `scripts/scaffold-project.py` in the now-empty repo directory. Tell the user the archive path and that they can delete it once they're satisfied with the rebuild.

For new projects, run `scripts/scaffold-project.py` to create:

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

Build behavior depends on Q1 + Q1b:

**Q1b = Add** (existing project, preserve): use `site-build-premium.md` as a guide but adapt to the existing codebase — match the detected stack's patterns, reuse existing components where possible, stay inside the user's folder conventions, never refactor unrelated code. This is the "extend, don't disrupt" mode.

**Q1b = Rebuild** (existing project, rewrite UI): this is the destructive mode and requires extra care. Before writing or deleting anything:

1. Enumerate every UI component and page file in the repo. Look in `src/app/`, `src/components/`, `src/pages/`, `app/`, `components/`, `pages/`, `src/routes/` — wherever the detected stack puts them. Also include `app/globals.css` or equivalent root stylesheet.
2. Look for spec docs in the repo: `*SPEC*.md`, `*-SPEC.md`, `AGENTS.md`, `PROJECT.md`, `CLAUDE.md`, and any README with detailed requirements. Read them — they carry user intent the survey doesn't capture.
3. Enter Plan Mode. The plan must have three clearly-labeled sections:
   - **Files to delete** (full list of UI components and pages, with paths)
   - **Files to preserve** (configs, API routes, `public/*`, env files, spec docs, `node_modules/`, `.git/`)
   - **Files to create** (new component/page layout per survey + spec)
4. Wait for user approval. If the user says "skip the delete of X", respect it — remove X from the delete list but keep the rest.
5. After approval, execute: delete the files in the delete list, then build the new UI following the survey answers + spec docs + existing infrastructure conventions (import aliases, TypeScript/JavaScript choice, CSS approach).
6. If the repo is not a git repo or has uncommitted changes, warn the user in the plan and recommend a commit before proceeding. Do not hard-block — some users work without git.

**Q1b = Replace** (existing project, archive and restart): Phase 5 already archived everything into `./archive-{timestamp}/`. Phase 6 runs as a greenfield build in the now-empty repo. No special handling beyond a one-line reminder at the end: *"Your original files are in ./archive-{timestamp}/ — delete the archive folder once you're happy with the rebuild."*

**New project** (Q1 = Landing / Multi-page / Full app / Portfolio): read `references/build-prompts/site-build-premium.md` (for premium tier) or `site-build-minimal.md` (for simpler runs) and fill in template variables from the survey:
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

**Use the Plan Mode → Bypass Permissions workflow** for the build. Plan Mode surfaces Claude's plan so the user can catch wrong assumptions before any files get written, and switching to Bypass Permissions only after approval means the actual build doesn't get interrupted by per-tool confirmations (which would pull the user out of the flow every few seconds during a 10-20 minute build). The checkpoint is upfront, the execution is smooth.

### Mid-build: 21st.dev Magic MCP component injection (optional)

**Skip if 21st.dev Magic MCP was not detected or the user declined.** If active, 21st.dev injects premium pre-built React/Tailwind components into standardized sections (Pricing, Testimonials, grid Features, FAQ, Footer, Nav) instead of having Claude build them from scratch. Never eligible for Hero, About, or custom sections — those stay custom-built.

**Read `references/phases/phase-6-components.md` for the full flow** — eligibility rules, per-section query pattern, brand-token styling, and conflict handling with Phase 2.5 Stitch scaffolds.

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
| `references/phases/phase-2-5-stitch.md` | Full Stitch flow — load only when Stitch MCP is detected and user opted in |
| `references/phases/phase-4c-paper.md` | Full Paper.design export flow — load only when Paper MCP is running and user opted in |
| `references/phases/phase-6-components.md` | Full 21st.dev mid-build injection flow — load only when 21st.dev MCP is detected |
| `references/survey-questions.md` | Full survey spec with adaptive rules |
| `references/vibe-archetypes.md` | 6 preset aesthetics with dials + sample references |
| `references/env-template.env` | All env vars the skill can use |
| `references/recommended-skills.json` | Peer skills + install commands |
| `scripts/call-kie.py` | Kie.ai API wrapper — Nano Banana image fallback + Kling 3.0 / Veo 3 / Veo 3.1 video |
| `scripts/call-wavespeed.py` | Wavespeed wrapper — Gemini 3 Pro Image (preferred) + Nano Banana Pro Edit Multi |
| `scripts/call-firecrawl.py` | Firecrawl brand extraction |
| `scripts/scaffold-project.py` | Project folder creator |
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
