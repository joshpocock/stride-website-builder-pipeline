# Master Build Prompt — Minimal Stack

Used when the user wants a lightweight build: no peer skill dependencies, no Kling / Veo video, minimal framework footprint. Picked automatically when the user has no paid API keys set or explicitly opts out of the premium stack. Scaled-down version of `site-build-premium.md`.

---

## Variables (same as premium)

---

## The Prompt

```
You are building a clean, professional landing page for {{brand_name}}.
This is the free-tier version — no required peer skills beyond Claude Code's
built-in front-end design skill. Keep the stack minimal and the output shippable.

## Identity

- Name: {{brand_name}}
- Tagline: {{tagline}}
- Description: {{description}}
- Audience: {{audience}}

## Design System

Use Claude's built-in front-end design skill. No third-party skill dependencies.

### Fonts
- Heading: {{heading_font}} (default: Geist)
- Body: {{body_font}} (default: Inter)
Load via Google Fonts with font-display: swap.

### Colors
- Background: {{colors.bg}}
- Text: {{colors.text}}
- Accent (CTAs): {{colors.accent}}

Dark mode by default unless brand colors dictate otherwise. Avoid pure black.

### Patterns
- Avoid Inter as a heading font, Roboto, Arial
- No centered heroes unless the vibe is editorial
- No 3-column equal card rows
- No AI clichés: Elevate, Seamless, Unlock, Empower
- Use staggered reveal animations on scroll
- Use skeletal loaders, not spinners

## Assets

If `assets/hero.mp4` exists, use it for the hero scroll animation.
If not, use `assets/hero-mobile.jpg` or a single hero image as a static hero.
No Kling/NanoBanana dependencies required.

## Hero

Option A (with video): Apple-style scroll-driven frame animation via ffmpeg
frame extraction + scroll-bound playback.

Option B (without video): Static hero image with a subtle parallax or zoom
on scroll. Still image fallback on mobile.

## Sections

{{sections}}

Build in order. Staggered reveal on scroll. Semantic HTML5 landmarks.

## Project Mode

**If adding to an existing project:** detect the stack from the project root (Next.js / Nuxt / Astro / SvelteKit / Remix / Vite / plain HTML) and match its conventions. Drop `brand.json` and `assets/` into the project's static directory. Don't migrate or refactor unrelated code.

**If a new project:** default to vanilla HTML + CSS + minimal JS, or Astro if the user picked it in Q2. Avoid heavier frameworks in minimal mode — single `index.html` + `styles.css` + `main.js` is ideal when possible.

## Technical

- Styling: Tailwind CSS via CDN for simplicity, or hand-written CSS
- No build step if possible
- Images: convert to WebP, lazy-load below the fold
- Accessibility: WCAG 2.2 AA minimum

## Performance

- LCP under 2.5s
- Single hero image, preloaded
- Inline critical CSS if possible
- No heavy frameworks

## Workflow

1. Start in PLAN MODE. Show me the plan. Wait for approval.
2. On approval, switch to Bypass Permissions and execute.
3. End with a working file tree and instructions for how to open it locally
   (e.g., `npx serve .` or just open index.html in a browser).
4. Do NOT do the SEO pass yet.
```

---

## How the Skill Uses This

Same as the premium version — fill in variables, write to build-plan.md, invoke Claude Code.

The minimal prompt explicitly avoids:
- Third-party skill dependencies (taste-skill, mager, etc.)
- Kie.ai / Kling / Veo / NanoBanana API calls
- Heavy frameworks unless the user explicitly picked one in Q2
- Paid services

The goal: a beautiful landing page anyone can build with zero budget and no API keys.
