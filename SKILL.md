---
name: stride-website-builder-pipeline
description: >
  End-to-end premium website builder. Guided survey chains Firecrawl brand
  extraction, NanoBanana 2 image generation, Kling 3.0 video animation,
  Claude Code build with multiple skills, full SEO optimization, and one-click
  deploy to Vercel/Netlify. Use when the user wants to: (1) build a landing
  page or multi-page website with AI, (2) create a premium $10K-style animated
  site, (3) go from brand URL to deployed website in under 30 minutes,
  (4) rebuild a competitor or client site with modern design.
  Triggers on: "build me a website", "build a landing page", "create a site
  for [brand]", "$10K website", "premium landing page", "ai website pipeline",
  "website builder", "vibe code a website", "rebuild [url]", "landing page
  for [company]", "build a scroll animated site".
---

# Website Builder Pipeline

Guided, survey-driven workflow for building premium animated websites end-to-end. Chains every tool and skill from the 2026 creator playbook into one interactive experience with pre-built prompts under the hood.

**Philosophy:** Claude is a collaborator, not autopilot. Survey first, confirm before executing, checkpoint at every phase. The user stays in the driver's seat.

**Who this is for:** Anyone who wants to build a $5K-$10K quality landing page in 15-30 minutes for $2-10 total cost, without manually chaining 8 different tools.

---

## Pipeline Phases

```
Phase 0: PREFLIGHT (check env + installed skills/tools)
    ↓
Phase 1: SURVEY (15 adaptive questions)
    ↓ [user confirms plan]
Phase 2: BRAND EXTRACTION (Firecrawl API)
    ↓
Phase 3: SKILL INSTALLATION (auto-install peers)
    ↓
Phase 4: ASSET GENERATION (Kie.ai NanoBanana + Kling)
    ↓
Phase 5: PROJECT SCAFFOLD (create folder + .env + files)
    ↓
Phase 6: BUILD (Claude Code + skills + master prompt)
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
2. **Tech stack** — Next.js / Astro / SvelteKit / Remix / Vite+React / Plain HTML / AI decides. *Skipped if Q1 = "Add to existing project"; stack is auto-detected from the repo.*
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
- Plan Mode first (Nate Herk strategy)

**Critical: Use the Plan Mode → Bypass Permissions workflow.** The skill should instruct Claude Code to enter Plan Mode, show the plan, wait for user approval, then execute.

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
| `references/design-inspiration.md` | Curated Dribbble/Godly/Pinterest links |
| `references/integration-verification.md` | Verified integrations (Firecrawl, 21st.dev, Stitch MCP, Paper.design MCP) |

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
