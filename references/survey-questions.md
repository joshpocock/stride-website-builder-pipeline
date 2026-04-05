# Survey Questions Spec

Full question spec for the `stride-website-builder-pipeline` skill. Each question is invoked via `AskUserQuestion`. Questions are adaptive — skip or rewrite based on earlier answers.

**Target length:** 13 questions max, ~8–10 after adaptive skips. Every question does real work; no filler.

Every question supports "Skip" / "Let AI decide" / "Let me paste manually" as escape hatches.

---

## Q1: Project Type

**question:** "What are we building?"
**header:** "Project type"
**options:**
- Landing page (single scroll, conversion-focused) — *Recommended*
- Multi-page site (home + about + services + contact)
- Full app (auth, database, dashboard)
- Portfolio (personal or creative)
- Add to an existing project (I already have a codebase)

**adaptive:**
- If "Full app" → trigger Lovable/Bolt recommendation path instead of Claude Code from scratch
- If "Add to an existing project" → Q2 (tech stack) is skipped and we detect stack from the repo; Phase 5 scaffold is skipped; Phase 6 build respects existing code conventions. **Always ask Q1b next** to clarify the mode — do not default.

---

## Q1b: Existing Project Mode (only if Q1 = "Add to an existing project")

**question:** "I see this project already has code. What do you want me to do with it?"
**header:** "Existing code"
**options:**
- **Add** — Keep all existing code. Add new pages, components, or sections while respecting current conventions. Use this when the existing code is good and you want to extend it. — *Recommended when the current UI is working*
- **Rebuild** — Keep infrastructure (Next.js/Nuxt config, tsconfig, package.json, API routes, public assets, env files, AGENTS.md / CLAUDE.md) but delete and rewrite every UI component and page from scratch following the survey answers and any spec docs found in the repo. Use this when the current UI is bad and you want a do-over without losing the plumbing.
- **Replace** — Archive everything outside of `.git/`, `node_modules/`, and `.env*` files into `./archive-{timestamp}/`, then start fresh in the same repo as if it were greenfield. Use this when you want to keep the repo URL and git history but nothing else.

Why this exists: the previous version of Q1 had only "Add to existing project" which implicitly assumed the user wanted to preserve current code. That's wrong when the existing UI is low-quality and the user wants a rebuild — Claude would audit + gap-fill instead of tearing down, and the output stays bad. Surfacing the three modes lets the user say what they actually want in one question.

**adaptive:**
- All three modes skip Q2 tech stack (detected from the existing repo) and skip Phase 5 scaffold.
- **Add mode** → Phase 6 build respects existing components and conventions, reuses existing files where possible, never deletes or refactors unrelated code. This is the prior default behavior.
- **Rebuild mode** → Phase 6 build first enumerates every UI component / page file in the repo, shows the user the list in Plan Mode with a clear "these will be deleted" section, waits for approval, then deletes them and rebuilds from the survey answers + any spec docs found (look for files matching `*SPEC*.md`, `*-SPEC.md`, `AGENTS.md`, `PROJECT.md`, `README.md` with detailed requirements). Infrastructure files (configs, API routes, `public/`, env files) are preserved.
- **Replace mode** → Phase 5 scaffold runs, but in-place. Before creating new files, moves everything except `.git/`, `node_modules/`, and `.env*` into `./archive-{YYYY-MM-DD-HHMM}/`. Then runs the normal greenfield scaffold. After the build, remind the user the archive exists and they can delete it once they're happy.

**Safety:** Rebuild and Replace modes both delete or move files. Always run inside Plan Mode for these — the plan must list every file that will be deleted, moved, or overwritten. The user approves the plan before any destructive action runs. If the repo is not a git repo or has uncommitted changes, warn the user and recommend a commit before proceeding.

---

## Q2: Tech Stack (skipped if Q1 = "Add to existing project")

**question:** "Which tech stack?"
**header:** "Stack"
**options:**
- Next.js (React, SSR, best SEO) — *Recommended for most*
- Nuxt (Vue 3, SSR equivalent to Next)
- Astro (content-focused, fastest by default)
- SvelteKit (lightweight, performant)
- Remix (React, data-driven)
- Vite + React (SPA, no SSR)
- Plain HTML + CSS + JS (simplest, no build step)
- Let AI decide (picks based on Q1 + Q5 vibe)

**adaptive:** If Q1 = "Portfolio" → pre-select Astro. If "Landing page" → pre-select Next.js. If "Multi-page site" → pre-select Astro or Next.js based on vibe.

---

## Q3: Brand Source

**question:** "Where does the brand come from?"
**header:** "Brand source"
**options:**
- Existing website URL (Firecrawl extracts everything — requires `FIRECRAWL_API_KEY`)
- Upload logo + colors + fonts manually (no API key needed)
- Screenshots (Claude vision extracts from images — no API key needed)
- Build from scratch (I'll define it with you, no API key needed)
- Let AI decide (skip brand questions, Claude picks from business info — no API key needed)

**adaptive:**
- "Existing URL" → ask for URL, skip Q7 colors, Q8 fonts. If `FIRECRAWL_API_KEY` missing, offer to switch to another path.
- "Screenshots" → request uploads, use vision extraction, skip Q7 + Q8
- "Manual" → parse inputs into `brand.json`, skip Q7 + Q8
- "Build from scratch" → keep Q7 + Q8
- "Let AI decide" → skip Q7 + Q8; Claude auto-generates `brand.json` from Q4 + Q5 + Q6 after the survey

---

## Q4: Business Info (free text, multi-part)

- Company name
- Tagline (10–15 words)
- One-sentence description

If Q3 = "Existing URL", pre-fill from Firecrawl extract and ask "does this look right?".

---

## Q5: Target Audience (free text)

"Who is this for? (industry, age range, what they care about)"

Used to tune copy tone, imagery style, section emphasis, and AI-suggested vibe.

---

## Q6: Vibe Archetype

**question:** "Pick a vibe (or let me pick one for you)"
**header:** "Vibe"
**options with previews (ASCII mockups — see `vibe-archetypes.md`):**
- Ethereal Glass — frosted, translucent, layered
- Editorial Luxury — magazine-grade, high contrast, serif
- Soft Structuralism — organic geometry, warm tones
- Brutalist — raw mechanical, monospace, grid
- Minimalist — warm monochrome, bento grids, serif + sans
- Custom — paste a URL and 3 adjectives, I generate a new archetype
- **Let AI decide** — I'll pick based on your business info and target audience

**adaptive:** If Q5 mentions "law firm / medical / finance" → default to Editorial Luxury or Minimalist. If "creative agency / art" → default to Ethereal Glass or Custom. If "tech startup / SaaS" → default to Brutalist or Minimalist.

---

## Q7: Color Palette (skipped if Q3 already provided colors)

**question:** "How do you want colors handled?"
**header:** "Colors"
**options:**
- Pick from preset palettes (per vibe archetype)
- Custom hex codes (I'll enter 4)
- AI suggests based on vibe + target audience

---

## Q8: Font Pairing (skipped if Q3 already provided fonts)

**question:** "Font pairing?"
**header:** "Fonts"
**options:**
- Geist + Satoshi (modern, taste-skill default)
- Cabinet Grotesk + Inter (editorial)
- JetBrains Mono + Space Grotesk (mager's stack)
- Playfair + Inter (luxury)
- Custom — I'll name them
- Let AI decide

**adaptive:** Pre-select based on vibe archetype.

---

## Q9: Hero Images

This question handles **all generated imagery for the site** — hero images, product shots, section accents. Three sub-axes.

### Q9a: Image Source

**question:** "How do you want the hero images?"
**header:** "Image source"
**options:**
- AI generates from scratch (I give Claude the prompt framework, it creates them) — *Recommended*
- I upload my own images (used as-is, no AI editing)
- I upload my own + AI edits them (Nano Banana / Gemini edits uploaded images to match brand colors, add elements, fix framing — your image becomes the starting point)
- Let AI decide

### Q9b: Prompt Source (only if Q9a ≠ "upload as-is")

**question:** "Where should the image prompts come from?"
**header:** "Image prompts"
**options:**
- AI writes them using the 6-stage Cinematic Frame Method (ANCHOR / WORLD / LUMINANCE / AIR / OPTICS / EXCLUSIONS) — *Recommended*
- I'll write my own prompts
- Let AI decide

### Q9c: Image Model (auto, not a user question unless override requested)

Model is auto-picked from env vars:
1. `WAVESPEED_API_KEY` set → Gemini 3 Pro Image (4K native, $0.025/img) — *preferred*
2. else `KIE_AI_API_KEY` set → Nano Banana Pro (2K)
3. else → error, prompt user to set a key

User can override via "let me pick the image model" escape hatch if they want to force one.

**Reference:** `build-prompts/cinematic-frame-method.md`, `build-prompts/image-gen-nanobanana.md`

---

## Q10: Hero Animation

### Q10a: Animation Style

**question:** "What hero animation style?"
**header:** "Animation style"
**options:**
- Exploded view (product decomposes into layers) — *Recommended for products*
- Cinematic orbit (camera rotates around product)
- Dolly zoom (camera pushes toward / away)
- Environment pan (camera travels through a 3D scene)
- Static image (no animation)
- I have my own MP4 to use
- Let AI decide

**adaptive:** If "Static" or "Own MP4" → skip Q10b and Q10c entirely.

### Q10b: Video Model

**question:** "Which video model?"
**header:** "Video model"
**options:**
- Kling 3.0 (image-to-image with start + end frames, cheapest, best for scroll animations) — *Recommended*
- Veo 3.1 Fast (newest, balanced speed/quality, single frame input)
- Veo 3.1 (newest, highest quality, slower)
- Veo 3 Fast (mid quality, faster)
- Veo 3 (high quality, slower)
- Let AI decide (picks based on Q10a + cost budget)

**note:** Kling is the only model that takes both start + end frames for precise interpolation. Veo models take a single start frame plus prompt — better for freeform motion, worse for locked scroll pairs.

### Q10c: Prompt Source

**question:** "Where should the video prompt come from?"
**header:** "Video prompt"
**options:**
- AI writes it from your animation style choice — *Recommended*
- I'll write my own prompt
- Let AI decide

**Reference:** `build-prompts/video-gen-kling.md`

---

## Q11: Sections (multi-select with free-text addition)

**question:** "Which sections does the site need? (pre-selected based on your project type and vibe — edit as you like)"
**header:** "Sections"
**multiSelect:** true
**options:**
- Hero (always required)
- Features / Benefits
- Pricing
- Testimonials / Reviews
- Team / About
- FAQ
- CTA / Contact Form
- Gallery / Portfolio
- Blog preview
- **+ Add your own** (free-text field — type any custom section name, comma-separated for multiple)
- Let AI decide everything

**adaptive pre-selection:**
- Landing page + SaaS vibe → Hero, Features, Pricing, Testimonials, FAQ, CTA
- Portfolio → Hero, Gallery, About, Contact
- Multi-page service business → Hero, Services, About, Testimonials, Contact
- Full app → Hero, Features, Pricing, CTA

---

## Q12: Deploy Target

**question:** "Where should we deploy?"
**header:** "Deploy"
**options:**
- Vercel + GitHub (auto-deploys on push) — *Recommended*
- Netlify (free forever, simple)
- Cloudflare Pages
- Manual (I'll handle it myself)
- Skip deploy for now

---

## Q13: SEO Tier

**question:** "SEO optimization level?"
**header:** "SEO"
**options:**
- Full audit — JSON-LD schemas, meta, sitemap, llms.txt, Lighthouse check — *Recommended*
- Basic — meta tags + OG + sitemap only
- Skip — no SEO pass

**adaptive:** If Q5 audience = "local service business", include a one-line note recommending Full with LocalBusiness schema. **Never force** — user's answer always wins.

---

## Q14 (Confirmation): Plan Summary

Generate a summary of everything and ask:

```
Here's what I'll do:

1. Stack: [tech stack] ([new project | add to existing at <path>])
2. Brand: [name] from [source]
3. Vibe: [archetype] with colors [hex list] and fonts [heading + body]
4. Hero images: [source] via [model], prompts [written by AI / user / mix]
5. Hero animation: [style] via [video model], prompt [source]
6. Sections: [list, including any user-added custom ones]
7. SEO: [tier]
8. Deploy: [target]
9. Estimated cost: $[X]
10. Estimated time: [X] minutes

Proceed?
```

**Options:**
- Looks good, run it
- Let me change [X]
- Cancel

---

## Removed Questions (historical)

- **Old Q12 Budget tier** — deleted. Overlapped with provider key detection in Phase 0 and added no real signal. Cost is bounded $2–$10 per run regardless; finer control comes from a cost ceiling set in preflight, not a tier.
- **Old Q13 Integrations** — deleted. Integrations are auto-detected from env vars in Phase 0 preflight and shown in the status table. Asking the user to re-select what they already have keys for is redundant.
- **Old Q14 Inspiration** — merged into the pre-survey Q4b (inspiration sources). Single question, no duplication.

---

## Adaptive Rules Summary

| If user says... | Then skip or rewrite... |
|---|---|
| Add to existing project | Skip Q2 tech stack; detect from repo. Skip Phase 5 scaffold entirely. |
| Existing URL brand | Skip Q7, Q8 (use extracted) |
| Screenshots / Manual / AI decide brand | Skip Q7, Q8 |
| Static hero or own MP4 | Skip Q10b + Q10c |
| Upload images as-is | Skip Q9b prompt source |
| Local service business target | Recommend Full SEO (never force) |
| Creative / portfolio site | Default Ethereal Glass or Custom vibe |
| Tech SaaS | Default Brutalist or Minimalist vibe |
| First-time user (no history) | Explain each tool before asking |
| Repeat user | Pre-fill from `history.json` |

---

## Escape Hatches

Every question supports these as implicit sub-options via "Other":
- "Skip this question"
- "Let me paste this manually"
- "Show me a screenshot of what you mean"
- "Use the default"
- "Let AI decide"

The skill never blocks on a question. If the user skips, use sensible defaults from vibe archetype + project type.
