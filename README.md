# stride-website-builder-pipeline

**A Claude Code skill that takes you from a brand URL to a deployed, premium, animated website in under 30 minutes for $2 to $10 in total cost.**

One skill. One command. The entire 2026 AI website stack chained into a single guided workflow — brand extraction, cinematic image generation, scroll animation, multi-skill build, full SEO pass, visual verification, and deploy.

---

## What it does

- **Phase 0 — Preflight.** Checks your env vars, installed peer skills, and required tools before touching anything.
- **Phase 1 — Survey.** 15 adaptive questions (screenshot-friendly, so you can paste mockups instead of describing them).
- **Phase 2 — Brand extraction.** Pulls colors, fonts, logo, spacing, and personality from any URL via Firecrawl and saves it as `brand.json`.
- **Phase 3 — Guided peer skill installation.** Walks you through installing exactly the right three skills for your project — one rules skill (`taste-skill`, always), one aesthetic opinion skill (picked from the menu based on your vibe), and one image tool (`cc-nano-banana` if you have a Gemini key). Shows the install commands, asks you to confirm each one, never silently runs code on your machine. The "10 skills" in the video is the menu you pick from, not a stack you install all at once.
- **Phase 4 — Asset generation.** Generates start and end hero frames via Gemini 3 Pro Image (Wavespeed AI, 4K native, $0.025/img) or Nano Banana Pro (Kie.ai, 2K, as fallback — the skill picks automatically based on which API key you have set). Then animates the scroll transition via Kling 3.0 on Kie.ai. When Wavespeed is in play, also runs a lock-pair matching pass through Nano Banana Pro Edit Multi so start and end frames share identical light, color, and camera before Kling interpolates them.
- **Phase 5 — Scaffold.** Creates a clean project folder with the brand file, hero MP4, mobile still, and a locked prompt set.
- **Phase 6 — Build.** Claude Code builds the site in Plan Mode, then executes in Bypass Permissions mode for clean first-try quality.
- **Phase 6.5 — Verify.** Hands off to `agent-browser` (Vercel Labs) for automated desktop and mobile screenshots, accessibility tree checks, Lighthouse scoring, and a self-correcting fix loop.
- **Phase 7 — SEO pass.** Full 2026 playbook: JSON-LD (Organization, LocalBusiness, Service, FAQ, BreadcrumbList), Core Web Vitals tuning, passage-extraction rewriting for AI Overview citation, AVIF images, semantic HTML5.
- **Phase 7.5 — Re-verify.** Second `agent-browser` pass after SEO changes.
- **Phase 8 — Deploy.** One-command Vercel or Netlify deploy with custom domain handling.
- **Phase 9 — Self-improve.** Logs what worked and what did not, and updates the skill's own prompt library. Your personal copy gets better with every project.

---

## Install

```bash
npx skills add https://github.com/joshpocock/stride-website-builder-pipeline
```

Then in Claude Code:

```
build me a landing page for apple.com
```

Answer the survey. Wait about 15 minutes. Get a deployed site with full SEO.

---

## Requirements

**Required env vars:**

- `ANTHROPIC_API_KEY` — Claude Code itself (Pro or Max plan recommended)
- **One image provider** (either `WAVESPEED_API_KEY` *or* `KIE_AI_API_KEY`) — needed for hero asset generation. `KIE_AI_API_KEY` is also required if you want Kling video animation.

**Conditionally required (only if you pick that path in the survey):**

- `FIRECRAWL_API_KEY` — only needed if you choose **"Existing URL"** as your brand source in Q2. Free tier: 500 scrapes/mo. If you don't have it, the survey gives you four other brand paths (manual, screenshots, build from scratch, let AI decide) that need no API key.

**Strongly recommended (preferred image provider):**

- `WAVESPEED_API_KEY` — Gemini 3 Pro Image (4K native, $0.025/img) + Nano Banana Pro Edit Multi for locked-pair matching. If set, the skill prefers Wavespeed over Kie.ai for all hero image generation. Newest Gemini-family model, not yet available on Kie.ai.

**Optional env vars:**

- `GOOGLE_AI_STUDIO_KEY` — free Nano Banana 2 fallback
- `GEMINI_API_KEY` — for the `cc-nano-banana` peer skill
- `VERCEL_TOKEN` — automated Vercel deploy
- `NETLIFY_AUTH_TOKEN` — automated Netlify deploy

Full env template at `references/env-template.env`.

**Peer skills the pipeline walks you through installing** (one confirmation per skill, never silent):

*Always installed:*
- `taste-skill` (Leonxlnx) — rules + dials slot. Anti-slop patterns, MIT licensed, 2,900 GitHub stars
- `agent-browser` (Vercel Labs) — utility, critical for Phase 6.5 verification

*Aesthetic opinion slot — pick exactly ONE per project based on the vibe:*
- `mager/frontend-design` → dark neon SaaS, brutalist, minimalist
- Anthropic official `front-end design` (modified) → polished animated product pages
- `UIUX Pro Max` (nextlevelbuilder) → industry-specific UX (medical, legal, fintech)

*Image tool slot:*
- `cc-nano-banana` (kkoppenhaver) — only if `GEMINI_API_KEY` is set

The pipeline never stacks multiple aesthetic-opinion skills at once. Stacking mager + front-end design + UIUX Pro Max gives Claude contradictory signals about type hierarchy and the build quality drops. Three skills is the sweet spot.

---

## Quick Start

```bash
# 1. Install the skill
npx skills add https://github.com/joshpocock/stride-website-builder-pipeline

# 2. Set your env vars (at minimum: Firecrawl + one image provider)
export FIRECRAWL_API_KEY=fc-...
export WAVESPEED_API_KEY=ws-...      # Preferred (Gemini 3 Pro Image, 4K)
export KIE_AI_API_KEY=kie-...        # Required for Kling video + image fallback

# 3. In Claude Code
build me a landing page for nike.com

# 4. Answer the 15-question survey (2-3 minutes)

# 5. Watch the pipeline run (~15-25 minutes)

# 6. Your site is live at https://your-project.vercel.app
```

---

## What you get

- A production-ready Next.js or Astro site (your choice during survey)
- Scroll-bound hero animation using 100+ WebP frames extracted from the Kling MP4
- Full 2026 SEO: JSON-LD schemas, Core Web Vitals in the green, AI Overview citation-ready copy
- Lighthouse scores: targeting 95+ on Performance, Accessibility, Best Practices, and SEO
- Automated visual verification at desktop and mobile breakpoints
- Deployed URL with custom domain support

---

## The philosophy

Claude is a collaborator, not autopilot. The pipeline surveys first, confirms before executing, and checkpoints at every phase. You stay in the driver's seat. No prompts are hidden, no phases run without your acceptance, and every decision the skill makes is surfaced to you so you can override it.

---

## The Cinematic Frame Method

For hero images that actually look like they cost $10K to shoot, this skill ships with a six-layer prompt framework: **ANCHOR, WORLD, LUMINANCE, AIR, OPTICS, EXCLUSIONS**. It includes a locked-pair workflow specifically designed so start frame and end frame share identical light, camera, and palette — which is how premium scroll animations actually work.

Full framework at `references/build-prompts/cinematic-frame-method.md`.

---

## Links

- **Full video walkthrough:** *Build Beautiful $10K Websites with AI. The Complete 2026 Guide*
- **YouTube channel (@joshfpocock):** https://www.youtube.com/@joshfpocock
- **Stride AI Academy — Free tier:** `<REPLACE: Stride AI Academy free URL>`
- **Stride AI Academy — Pro tier:** `<REPLACE: Stride AI Academy pro URL>`
- **Work with Josh 1:1:** https://executivestride.com/apply

---

## Credits

Built by [Josh Pocock](https://www.youtube.com/@joshfpocock). Distilled from 13+ creator tutorials, hundreds of build hours, and the full 2026 Claude Code skills ecosystem. Ships with every tool, prompt, and SEO technique from the companion video.

Open source. MIT licensed. Run it, break it, send PRs.

---

## Structure

```
stride-website-builder-pipeline/
├── SKILL.md                        # Main skill instructions for Claude
├── README.md                       # This file
├── references/
│   ├── env-template.env
│   ├── survey-questions.md
│   ├── vibe-archetypes.md
│   ├── recommended-skills.json
│   ├── call-firecrawl.py           # Firecrawl API wrapper
│   ├── call-kie.py                 # Kie.ai API wrapper (Nano Banana + Kling video)
│   ├── call-wavespeed.py           # Wavespeed API wrapper (Gemini 3 Pro Image + lock-pair)
│   ├── scaffold-project.py         # Project folder creator
│   ├── seo-research-2026.md        # Deep SEO playbook
│   ├── design-inspiration.md       # Curated design references
│   ├── integration-verification.md # Verified tool integrations
│   └── build-prompts/
│       ├── brand-extract.md
│       ├── image-gen-nanobanana.md        # Fill-in templates
│       ├── cinematic-frame-method.md      # 6-layer prompt framework
│       ├── video-gen-kling.md
│       ├── site-build-premium.md
│       ├── site-build-minimal.md
│       ├── seo-pass.md
│       ├── verify-build.md                # agent-browser loop
│       └── deploy-vercel.md
└── assets/
```

---

## Reporting issues

Open an issue on the GitHub repo. Include which phase failed, the full Claude Code log, your env var status (redact the keys — just say which are set), and the survey answers you gave.

---

*If this skill saved you a week of work, star the repo and share the video. That is the whole economy.*
