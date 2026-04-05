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
- `{{framework_choice}}` (next/astro/remix/vanilla — inferred from complexity)

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

## Technical Requirements

- Framework: {{framework_choice}} (use Next.js App Router by default, Astro
  if marketing-heavy, vanilla HTML if simple single-page)
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
