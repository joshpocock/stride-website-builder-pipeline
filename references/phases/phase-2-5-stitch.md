# Phase 2.5 — Stitch Layout Generation

**Loaded on demand.** Only read this file if Stitch MCP was detected in Phase 0 preflight and the user opted in. If Stitch is not available, skip this phase entirely — Phase 6 will generate layouts from scratch.

## What and why

Stitch is Google's free AI-native UI design tool, powered by Gemini 3.1 Pro or Gemini 3 Flash. It generates themed HTML + Tailwind scaffolds per section. We use it as **structural scaffolding** for Phase 6 — not as finished code. Claude's job in Phase 6 is to port the Stitch output to the chosen tech stack and layer in animations, real images, taste-skill rules, and SEO. This gives you the speed of AI layout generation with the quality of Claude's framework-native build.

## Flow

### 1. Create a Stitch project

Call `mcp__stitch__create_project` with `title = {{brand_name}}`. Capture the returned `projectId` — it's needed for every subsequent call.

### 2. Map brand.json → Stitch design system

Call `mcp__stitch__create_design_system` with `projectId` and a `DesignTheme` built from the following mapping.

**Colors:**
- `customColor` ← `brand.colors.primary`
- `overrideSecondaryColor` ← `brand.colors.secondary`
- `overrideTertiaryColor` ← `brand.colors.accent`
- `colorMode` ← `DARK` if `brand.colors.bg` has luminance < 0.3, else `LIGHT`

**Fonts:** Stitch has a fixed 29-font enum. Pick the closest match to `brand.fonts.heading` and `brand.fonts.body`. Supported fonts:

```
GEIST, SPACE_GROTESK, INTER, MANROPE, PLUS_JAKARTA_SANS, DM_SANS,
IBM_PLEX_SANS, SORA, MONTSERRAT, EB_GARAMOND, NEWSREADER, LITERATA,
DOMINE, LIBRE_CASLON_TEXT, SOURCE_SERIF_FOUR, RUBIK, NUNITO_SANS,
WORK_SANS, LEXEND, EPILOGUE, BE_VIETNAM_PRO, PUBLIC_SANS, METROPOLIS,
SOURCE_SANS_THREE, HANKEN_GROTESK, ARIMO, SPLINE_SANS, NOTO_SERIF
```

If the brand font isn't in the enum (e.g., Satoshi, Cabinet Grotesk), pick the visually-closest match (Geist for modern sans, EB Garamond for elegant serif) and record the real font name in `designMd` so Gemini can honor it in the output.

**Color variant** — mapped from Q6 vibe:
- Brutalist → `MONOCHROME`
- Minimalist → `NEUTRAL`
- Ethereal Glass → `TONAL_SPOT`
- Soft Structuralism → `EXPRESSIVE`
- Editorial Luxury → `FIDELITY`
- Custom → `VIBRANT`

**Roundness** — mapped from vibe:
- Brutalist → `ROUND_FOUR`
- Editorial Luxury → `ROUND_EIGHT`
- Minimalist / Soft Structuralism → `ROUND_TWELVE`
- Ethereal Glass → `ROUND_FULL`

**designMd** — free-form markdown. Write a brief description of the vibe archetype, the taste-skill dial tuning (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY), the banned patterns (no AI clichés, no Inter-as-heading, no 3-column equal rows), and the real brand font names if any had to fall back. This is where you get to add nuance the enum can't capture.

### 3. Activate the design system

Call `mcp__stitch__update_design_system` on the project. This is required — creating the design system alone doesn't apply it.

### 4. Generate one screen per selected Q11 section

For each section the user picked in Q11, call `mcp__stitch__generate_screen_from_text`:

- `projectId` ← the one from step 1
- `deviceType` ← `DESKTOP` (mobile responsiveness happens in Phase 6)
- `modelId` ← `GEMINI_3_1_PRO` by default, fall back to `GEMINI_3_FLASH` on rate limits
- `prompt` ← filled from `references/build-prompts/stitch-section-prompts.md` using `{brand_name}`, `{brand.description}`, `{vibe_archetype}`, `{target_audience}`, and section-specific instructions. **Keep each prompt under ~1500 tokens** — Stitch times out on large monolithic prompts.

**Always generate per-section, never monolithic.** A production run in April 2026 confirmed that passing a single prompt describing an entire multi-section landing page (all copy + all design system + all section instructions) causes the Stitch MCP HTTP call to time out client-side, and `list_screens` confirms nothing was generated server-side either. The monolithic approach seems like it would produce more coherent results, but in practice it just fails. Split every landing page into one `generate_screen_from_text` call per section — the design system handles cross-section consistency.

**Parallelize 2-3 calls at a time.** `generate_screen_from_text` is async and each call can take a few minutes. Running them sequentially for a 6-section landing page means 15-20 minutes of wall time. Issuing 2-3 parallel calls per turn drops that to ~3-5 minutes. Avoid issuing all 6+ at once — too many simultaneous MCP calls can hit rate limits or connection pool exhaustion.

### 5. Optional variants

If the user opted in during preflight to "show alternatives for key sections," call `mcp__stitch__generate_variants` on the hero + pricing + CTA screens:

```
variantOptions = {
  variantCount: 3,
  creativeRange: EXPLORE,
  aspects: [LAYOUT, COLOR_SCHEME]
}
```

**Variants are off by default** because they triple total generation time. Only run when the user explicitly asks for exploration.

### 6. User selection

Call `mcp__stitch__list_screens` to enumerate everything generated. For each section, present the screen(s) to the user with a brief description pulled from `get_screen`, and ask them to pick one per section. Support two refinement paths:

- **"Keep all"** — move on with every variant selected
- **"Regenerate this one with feedback"** — use `mcp__stitch__edit_screens` with the user's feedback as the prompt

### 7. Extract HTML + Tailwind

For each selected screen, call `mcp__stitch__get_screen` and pull the HTML + Tailwind output. Save to `{project_dir}/stitch-scaffold/{section_name}.html`.

### 8. Hand off to Phase 6

Augment the Phase 6 build prompt with this instruction block:

> Structural scaffolding is available in `./stitch-scaffold/`. For each section, the corresponding `.html` file is a Stitch-generated Tailwind layout themed to the brand. Port these to `{{tech_stack}}` components — preserve layout structure, spacing, and hierarchy — but ADD: scroll-bound hero animation (use `assets/hero.mp4`), real Nano Banana / Gemini hero images (replace any placeholder images), taste-skill anti-slop overrides, framework idioms (e.g., Next.js `<Image>` instead of `<img>`, Astro `.astro` components instead of raw HTML), semantic HTML5 landmarks, and responsive breakpoints Stitch didn't cover.

## Cost and time

- **Cost:** $0. Stitch is free, Google hosts the Gemini inference.
- **Time:** 2-5 min without variants, 5-12 min with variants. Tell the user the estimate upfront so the wait doesn't feel broken.

## Failure handling

If `generate_screen_from_text` fails or times out on a specific section:

1. Retry once with `modelId = GEMINI_3_FLASH` (faster, looser rate limits)
2. If that also fails, skip that section — Phase 6 will generate the layout from scratch for sections without a scaffold
3. Never block the whole pipeline on a Stitch failure — the rest of the pipeline works without it

## See also

- `references/build-prompts/stitch-section-prompts.md` — per-section prompt templates with anti-slop rules
- `references/vibe-archetypes.md` — vibe → color variant / roundness mappings originate here
