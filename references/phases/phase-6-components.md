# Phase 6 Mid-Build — 21st.dev Magic Component Injection

**Loaded on demand.** Only read this file if 21st.dev Magic MCP was detected in Phase 0 preflight and the user opted in. If 21st.dev is not available, skip this sub-step — Claude builds every section from scratch (which it's already good at).

## What and why

21st.dev Magic is a premium component library exposed as an MCP. It returns production-ready React + Tailwind components for standardized landing-page patterns — pricing tables, testimonial carousels, feature grids, footers, nav bars. These are battle-tested, animated, accessible, and already aligned with premium design conventions.

We use it as a speedup for sections where a good premade exists. Claude can build these sections from scratch too, but for standardized patterns there's no upside to reinventing — and the premade components often look better than a from-scratch build under time pressure.

## Which sections benefit

**Eligible for 21st.dev injection:**
- Pricing tables
- Testimonials / reviews
- Features (only grid-heavy patterns — not brand-specific feature walls)
- FAQ accordions
- Footer
- Nav bar

**NOT eligible — always custom-built:**
- Hero — too brand-specific, and the cinematic scroll-animation path requires full control over the DOM structure
- About / Team — too custom, Team cards vary too much between brands
- Gallery / Portfolio — brand-specific layouts
- User-defined custom sections from Q11's "+ add your own" — definitionally not a premade

## Flow during Phase 6 build

### 1. Surface choices in Plan Mode

After Claude enters Plan Mode but before executing, the plan should list which sections will use 21st.dev components vs which will be custom-built. The user sees this in the plan and can override per-section if they want all-custom or all-21st.dev.

### 2. Query 21st.dev per eligible section

For each section on the eligible list that was selected in Q11, Claude calls the 21st.dev Magic MCP search/fetch tool with a prompt describing the section's needs:

- Brand colors from `brand.json`
- Vibe archetype from Q6
- Content from `brand.json` or survey answers

### 3. Pick + inject

21st.dev returns 1-3 component options. Claude picks the best fit based on vibe compatibility. If multiple options look equally good, present them to the user and ask which they prefer.

Insert the component into the build, then style it to match brand tokens (colors, fonts, spacing, roundness) from the design system.

### 4. Log the choice

Log every component choice in `build-log.md` for the Phase 9 learnings step. Format:

```
- Section: pricing
  Source: 21st.dev Magic
  Component: pricing-table-3-tier-highlight
  Reason: matched Brutalist vibe, 3-tier structure fits survey answers
  Brand tokens applied: customColor, headlineFont, ROUND_FOUR
```

## Conflict handling with Phase 2.5 Stitch scaffolds

If Phase 2.5 Stitch scaffolds exist for a section AND 21st.dev has a component for it, there's a conflict. Resolve with this rule:

- **21st.dev wins for standardized patterns** — Pricing, Testimonials, Footer, Nav. Components beat scaffolds for these because premade components are better-tested for standardized content.
- **Stitch scaffold wins for brand-specific sections** — Hero, Features (if brand-specific), About, custom sections. Scaffolds beat components here because the Stitch output is already themed to the brand.

Document the choice in the plan so the user can override before execution.

## See also

- `references/integration-verification.md` — 21st.dev Magic MCP setup and verification
- `references/phases/phase-2-5-stitch.md` — the Stitch scaffolding this interacts with
