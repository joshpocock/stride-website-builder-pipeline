# Master Build Prompt — Premium Stack

This is the main prompt that drives the Claude Code build when the user picks
Budget or Pro tier. Filled from survey answers + brand.json + vibe archetype.

The skill writes the filled-in version to `{project}/build-plan.md` and then
invokes Claude Code with `@build-plan.md`.

---

## Variables

- `{{brand_name}}`, `{{tagline}}`, `{{description}}`
- `{{colors}}` (primary/secondary/accent/bg/text hex)
- `{{heading_font}}`, `{{body_font}}`
- `{{vibe}}`, `{{design_variance}}`, `{{motion_intensity}}`, `{{visual_density}}`
- `{{sections}}` (list)
- `{{animation_type}}`
- `{{inspiration_refs}}` (list of URLs or files)
- `{{deploy_target}}`
- `{{framework_choice}}` (next/nuxt/astro/sveltekit/remix/vite/vanilla — from Q2, or `existing` if Q1 = add-to-existing-project)
- `{{project_mode}}` (`new` or `existing`) — controls whether Phase 5 scaffold ran
- `{{existing_project_path}}` (absolute path, only set when `project_mode = existing`)

---

## The Prompt

```
You are building a premium landing page for {{brand_name}}. Follow this spec
exactly and resist the urge to add anything not specified.

## Identity

- Name: {{brand_name}}
- Tagline: {{tagline}}
- Description: {{description}}
- Industry: {{industry}}
- Audience: {{audience}}

## Design System (apply via taste-skill)

Activate the taste-skill with these dial settings:
- DESIGN_VARIANCE: {{design_variance}} (layout experimentation level)
- MOTION_INTENSITY: {{motion_intensity}} (animation level)
- VISUAL_DENSITY: {{visual_density}} (content per viewport)

Also activate the front-end design skill and (if installed) mager/frontend-design.

### Fonts
- Heading: {{heading_font}}
- Body: {{body_font}}
Load via Google Fonts or self-hosted WOFF2. Add font-display: swap. Preload
the heading font.

### Colors
- Background: {{colors.bg}}
- Text: {{colors.text}}
- Primary: {{colors.primary}}
- Secondary: {{colors.secondary}}
- Accent (CTAs): {{colors.accent}}

Do NOT use pure black (#000000) — use {{colors.bg}} which is dark but not absolute.

### Vibe: {{vibe}}
Reference the taste-skill's {{vibe}} archetype. Key rules:
- BANNED fonts: Inter (as heading), Roboto, Arial, Open Sans
- BANNED patterns: 3-column equal card rows, centered hero (unless Editorial
  Luxury), purple/neon AI aesthetic, spinners (use skeletal loaders), AI
  clichés (Elevate, Seamless, Unlock, Empower)
- REQUIRED: spring physics animations, staggered reveals, GPU-safe transforms
  only, asymmetric or Bento grid layouts, loading/empty/error states for
  every interactive element

### Layout Reinvention Rule (REBUILD mode critical)

When `{{project_mode}} = existing` and the user chose Rebuild mode, this
is the single most important thing to get right: **preserving copy is NOT
the same as preserving layouts.** A "visual refresh" that keeps the same
section skeletons with nicer CSS is a polish pass, not a rebuild — and the
user will experience it as "looks exactly the same."

**Pre-write self-check for every component:** Before writing any component
file, ask yourself: "Is this layout structurally different from what
existed, or am I just restyling the old skeleton?" If a stranger comparing
before-and-after screenshots would squint to find differences, start over
with a different layout approach.

**Layout alternatives menu — use these instead of the common defaults:**

| Section | Instead of this (generic) | Do this (premium/distinctive) |
|---|---|---|
| 3-step process / How It Works | 3-column icon card grid | Vertical timeline with massive step numbers (8rem), alternating-side rows, or horizontal scroll-snap on mobile |
| 3 value props | Equal 3-column cards | Asymmetric bento with one hero card (2/3 width) + two stacked support cards (1/3), or 12-col grid with 7/5 split |
| Testimonials | Equal 3-column review cards | One massive featured quote (full-width, display-scale type) + 2-3 supporting quotes orbiting below at smaller scale |
| FAQ | Standard accordion | Numbered editorial list with inline answers visible, or two-column Q-left A-right layout, or progressive disclosure with search |
| Comparison / Why Us | 3-column HTML table | Visual versus layout (side-by-side stacked columns with icons), or animated toggle between options |
| Final CTA | Gradient background block | Full-bleed cinematic image background with text overlay, or split-screen (image left, CTA right), or floating card over section transition |
| Stats / Social Proof | Inline number row | Massive counter typography (10rem numbers) with small labels, staggered fade-in on scroll |
| Pricing | Equal-width tier columns | Asymmetric — spotlight the recommended tier at 1.5x scale, slide others back |

**Typography push for premium builds:**
- Display-scale headlines at 4rem minimum, 6rem–10rem for hero and section
  headers. Tight tracking (-0.03em to -0.06em). Line height 0.9–1.1 for
  display sizes.
- Editorial two-column body layouts for long-form sections (About, How It
  Works narrative).
- Massive pull-quotes for testimonials — 3rem minimum, serif or display font,
  max-width 65ch.
- Numbers rendered at display scale (e.g., "500+" at 6rem) with a small
  label underneath ("installations completed") — never inline.

## Assets

All assets are in `./assets/`:
- `hero.mp4` — the scroll animation video (use ffmpeg to extract frames)
- `hero-mobile.jpg` — still fallback for mobile (do NOT load MP4 on mobile)
- `start-frame.webp`, `end-frame.webp` — if you need them for feature sections
- Logo (if any) — from brand.json logo_url

## Hero Section

Create an Apple-style scroll-driven animation:
1. Use ffmpeg to extract 100+ frames from `assets/hero.mp4` as WebP images at
   1920x1080 or the MP4's native resolution
2. Preload the first 10 frames for instant render
3. Lazy-load the remaining frames as the user scrolls
4. Bind frame index to scroll position using requestAnimationFrame
5. Scroll down = play forward, scroll up = play backward
6. On mobile (<768px viewport): replace with `hero-mobile.jpg` as a static
   hero — do NOT load the video

Overlay the hero headline and CTA on top of the animation using the fonts
and colors above.

## Sections (build in this order)

{{sections}}

For each section:
- Use staggered reveal animations on scroll (IntersectionObserver)
- Respect the vibe archetype layout patterns
- Add loading, empty, and error states where applicable
- Use semantic HTML5 landmarks (section, article, header, nav, main, footer)

## Inspiration

Reference these inspiration sources for layout rhythm and structure only
(NOT visual copying):
{{inspiration_refs}}

Any HTML sources in `inspiration/` are for structural scaffolding only. Any
screenshots are for visual mood reference only.

## Project Mode: {{project_mode}}

**If `{{project_mode}} = new`:** you are working in a fresh scaffolded project at the current working directory. Build freely.

**If `{{project_mode}} = existing`:** you are adding this landing page to an existing codebase at `{{existing_project_path}}`. Rules:
- Detect the stack by reading the project root (`package.json`, `next.config.*`, `nuxt.config.*`, `astro.config.*`, `svelte.config.*`, `remix.config.*`, `vite.config.*`, or plain `index.html`). Use what's there — do NOT try to migrate it.
- Match the project's existing conventions: component folder layout, CSS approach (Tailwind / CSS modules / styled-components / plain CSS), import aliases, TypeScript or JavaScript, routing pattern.
- Reuse existing components, utilities, and design tokens where they fit. Only create new files when no existing equivalent covers the need.
- Drop `brand.json` into `public/` or the project's static directory. Drop `assets/` into `public/assets/` or `src/assets/` — match whichever the existing project uses.
- Never refactor, rename, or delete unrelated files. If you see a code-quality issue outside the landing page's scope, leave it alone.
- If the landing page needs a new route, create it following the project's existing routing pattern (e.g., `app/landing/page.tsx` for Next App Router, `pages/landing.vue` for Nuxt, `src/routes/landing/+page.svelte` for SvelteKit, `src/pages/landing.astro` for Astro).
- Before writing any file, check if a similar file already exists and show the user a one-line diff plan.

## Technical Requirements

- Framework: {{framework_choice}} — Next.js App Router is the default for new projects; Nuxt 3 if Vue is requested; Astro for content-heavy marketing sites; SvelteKit / Remix / Vite+React for niche preferences; plain HTML only for the simplest single-page cases. When `{{project_mode}} = existing`, ignore this and use whatever the existing project uses.
- Build tool: whatever the framework uses
- Styling: Tailwind CSS with the theme tokens configured to match the color
  palette and fonts above
- Animation: Framer Motion or native CSS transitions (GPU-safe only —
  transform + opacity)
- Icons: Lucide or Phosphor (never emoji in UI)
- Images: Optimize to AVIF/WebP, lazy-load below the fold
- Accessibility: WCAG 2.2 AA minimum, semantic HTML, alt text, keyboard nav,
  focus styles

## Performance Targets

- LCP under 2.5s
- CLS under 0.1
- INP under 200ms
- Initial JS bundle under 100KB compressed
- No layout shift on font load (use font-display: swap + size-adjust)

## What NOT to Do

- Do NOT do the SEO pass yet — that's a separate step
- Do NOT commit or push to git
- Do NOT deploy
- Do NOT add analytics
- Do NOT add tracking pixels
- Do NOT add a cookie banner (that comes later if legally required)
- Do NOT add placeholder content if real content is in brand.json
- Do NOT use Lorem Ipsum anywhere

## Workflow

1. Start in PLAN MODE. Read every file in the project. Create a detailed plan.
2. Show me the plan. Wait for my approval before executing.
3. When I approve, switch to Bypass Permissions mode and execute.
4. End by spinning up a dev server at localhost.
5. Tell me the URL and what to click to verify the hero animation works.
```

---

## How the Skill Uses This

1. Reads the template
2. Substitutes all `{{variable}}` placeholders from survey answers + brand.json
3. Writes the result to `{project_dir}/build-plan.md`
4. Tells Claude Code: "@build-plan.md — enter plan mode and follow this exactly"
5. Checkpoints after plan approval before letting Claude execute
