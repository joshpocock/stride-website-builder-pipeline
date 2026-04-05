---
name: website-builder-pipeline
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

Present results as a color-coded table:
- ✓ Ready (green)
- ⚠ Needs key (yellow)
- ✗ Not installed (red)

Offer "install all recommended" or let user cherry-pick. NEVER install automatically — always ask first.

If this is a repeat run, pre-fill the survey with the user's last answers from history.

---

## Phase 1: The Survey (15 Adaptive Questions)

Use `AskUserQuestion` for each step. Adapt — skip questions when answers from earlier questions make them unnecessary.

See `references/survey-questions.md` for the full question spec, adaptive rules, and answer options.

**Core questions:**

1. **Project type** — Landing page / Multi-page / Full app / Portfolio
2. **Brand source** — Existing URL (→ Firecrawl) / Upload logo+colors / Build from scratch / Screenshots
3. **Business info** — Company name, tagline, one-sentence description
4. **Target audience** — Who is this for?
5. **Vibe archetype** — 6 presets with ASCII previews (see `references/vibe-archetypes.md`)
6. **Color palette** — Use extracted brand / Pick preset / Custom hex
7. **Font pairing** — Geist+Satoshi / Cabinet Grotesk+Inter / Custom
8. **Hero animation** — Exploded view / Cinematic orbit / Dolly / Pan / None / Upload MP4
9. **Product images** — AI-generate / Upload existing / Mix
10. **Sections needed** — Hero / Features / Pricing / Testimonials / Team / FAQ / CTA (multi)
11. **Deploy target** — Vercel / Netlify / Cloudflare / Manual / Skip
12. **Budget tier** — Free / Budget ($5, Kie.ai) / Pro ($20, Higgsfield+skills)
13. **Integrations** — Firecrawl / Kie.ai / GitHub / Vercel / 21st.dev / Stitch MCP (multi)
14. **Inspiration** — Paste URLs or drop screenshots
15. **SEO tier** — Skip / Basic / Full Audit

After Q15, present the generated plan and wait for explicit confirmation before any execution.

**Adaptive rules (examples):**
- If Q2 = "Build from scratch" → skip Q6 brand extraction questions
- If Q12 = "Free" → force Q13 to Google AI Studio, skip Kie.ai
- If Q8 = "None" → skip Q9 product images
- If user provides a Figma file → skip Q6, Q7 entirely

**Escape hatches:** every question supports "skip this / paste manually / let me show you".

---

## Phase 2: Brand Extraction

If user chose "Existing URL" in Q2:

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

If user provided screenshots instead: use Claude vision to extract the same fields and write `brand.json`.

If user chose "Build from scratch": ask for the fields directly via `AskUserQuestion`.

**Reference:** `references/build-prompts/brand-extract.md` for the vision extraction prompt.

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

### 4b. Kling 3.0 Video Animation

Generate the Kling transition prompt from `references/build-prompts/video-gen-kling.md` using the picked start+end frames.

Call `references/call-kie.py` with:
- Model: `kling3`
- Start image: picked start frame URL
- End image: picked end frame URL
- Duration: 5s
- Quality: 1080p
- Enhance: off

Download the MP4 to `project/assets/hero.mp4`. Run ffmpeg to extract a mobile still: `hero-mobile.jpg`.

Cost budget: ~$3-5 per full run. Alert user if they hit $10.

---

## Phase 5: Project Scaffold

Run `references/scaffold-project.py` to create:

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

Read `references/build-prompts/site-build-premium.md` (or `site-build-minimal.md` if budget tier is Free) and fill in template variables from the survey:
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
