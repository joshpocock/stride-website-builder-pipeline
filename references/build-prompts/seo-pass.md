# SEO Optimization Pass Prompt

Run AFTER the initial build is complete and user has approved the design.
This is Phase 7 of the stride-website-builder-pipeline skill.

Full 2026 SEO playbook lives at `references/seo-research-2026.md` (filled
by the SEO deep research agent). This prompt references that document.

---

## The Prompt

```
You are now running a full SEO optimization pass on the built site. Use the
2026 SEO playbook at `<skill-dir>/references/seo-research-2026.md` as your
authoritative reference. Do not make assumptions — follow the playbook.

## Brand Context (for generation)

- Name: {{brand_name}}
- Tagline: {{tagline}}
- Description: {{description}}
- Industry: {{industry}}
- Audience: {{audience}}
- Location: {{location}} (if local business)
- Service type: {{service_type}} (if LocalBusiness)
- Phone/address (if local): {{nap}}

## Tasks

### 1. Meta Tags (in <head>)

Inject or update:
- <title>{{brand_name}} — {{tagline}}</title> (max 60 chars)
- <meta name="description" content="..."> (150-160 chars, include 1 benefit + 1 proof point + CTA verb)
- <meta name="robots" content="index, follow">
- <link rel="canonical" href="https://{{domain}}/">
- <meta charset="utf-8">
- <meta name="viewport" content="width=device-width, initial-scale=1">

### 2. Open Graph + Twitter Cards

- <meta property="og:title" content="...">
- <meta property="og:description" content="...">
- <meta property="og:image" content="https://{{domain}}/og-image.jpg"> (1200x630)
- <meta property="og:url" content="https://{{domain}}/">
- <meta property="og:type" content="website">
- <meta property="og:site_name" content="{{brand_name}}">
- <meta name="twitter:card" content="summary_large_image">
- <meta name="twitter:title" content="...">
- <meta name="twitter:description" content="...">
- <meta name="twitter:image" content="https://{{domain}}/og-image.jpg">

Generate a dedicated og-image.jpg if one doesn't exist. Use brand colors,
name, and tagline in a 1200x630 composition.

### 3. JSON-LD Structured Data

Inject these schemas as <script type="application/ld+json"> in the <head>.
Only include schemas where the data actually exists on the page — don't
fabricate reviews or FAQs.

Always:
- Organization (or LocalBusiness if applicable)
- WebSite
- WebPage

Conditional:
- LocalBusiness — IF audience is local service business (strongly recommended)
- Service — for each service the page describes
- FAQ — if an FAQ section exists
- Review — if testimonials section exists with author names and ratings
- VideoObject — if hero animation or embedded videos exist
- Product — if selling a product
- BreadcrumbList — for multi-page sites
- HowTo — if the page describes a how-to
- Article — for blog/content pages
- Person — for team/about pages with individuals

Use the exact schema snippets from `seo-research-2026.md`. Do not invent
schema shapes.

### 4. Semantic HTML5 Landmarks

Audit the DOM and ensure:
- One <header> with primary nav
- One <main> containing the primary content
- <section> for each distinct content section with proper h2/h3 hierarchy
- <article> for self-contained content blocks
- <aside> for complementary content
- <nav> for primary and secondary navigation
- <footer> with legal, social, sitemap

Every image has alt text (descriptive, not keyword stuffed).
Every interactive element is keyboard accessible.

### 5. Generate Files at Site Root

- **robots.txt** — allow all reputable crawlers, disallow /admin, /api, link to sitemap
- **sitemap.xml** — auto-generate from all pages, include lastmod dates
- **llms.txt** — the emerging 2026 standard guiding LLM crawlers. Include:
  - Site name + brief description
  - Core content URLs with descriptions
  - What LLMs should prioritize
- **humans.txt** — optional, credits the team
- **manifest.json** — for PWA support (name, short_name, icons, theme_color)

Use the exact templates from `seo-research-2026.md`.

### 6. Image SEO

For every image on the site:
- Convert to AVIF (primary) and WebP (fallback) using ffmpeg or sharp
- Rename files descriptively (e.g., `red-sneakers-side-view.avif`, not `IMG_0423.avif`)
- Add meaningful alt text that describes the content (not keyword stuffed)
- Add loading="lazy" to below-the-fold images
- Add fetchpriority="high" to the hero image
- Add width + height attributes to prevent CLS
- Use <picture> with srcset for responsive images

### 7. Performance Optimization

- Inline critical CSS (above-the-fold styles)
- Preload the hero font and hero image
- Defer non-critical JS
- Minify CSS + JS
- Enable gzip/brotli compression
- Verify bundle size: initial JS under 100KB compressed
- Verify no layout shift from font loading (font-display: swap + size-adjust)

### 8. E-E-A-T Signals

If the site has any of:
- Author bylines → add Person schema + author bio
- Customer reviews → add Review + AggregateRating schema
- Credentials (licenses, certifications, years in business) → surface prominently
- Source citations → link out + use proper <cite> tags

### 9. Local SEO (if applicable)

If the target audience is a local service business:
- LocalBusiness schema with full NAP (Name, Address, Phone)
- Embed Google Maps iframe in contact section
- Hours of operation in schema
- Service area (geographic scope)
- Link to Google Business Profile
- Mention location/neighborhood in h1 and meta description
- "near me" oriented copy where appropriate

### 10. Analytics (if keys provided)

If GA4_MEASUREMENT_ID is set in .env:
- Inject the GA4 snippet in <head>
- Add basic event tracking for CTA clicks

If PLAUSIBLE_DOMAIN is set:
- Inject the Plausible script (privacy-first alternative)

### 11. Lighthouse Audit

Run `lighthouse <url> --output=json --output-path=./lighthouse-report.json`
via the CLI. Parse the report and show me:
- Performance score
- Accessibility score
- Best Practices score
- SEO score
- Core Web Vitals (LCP, CLS, INP)
- Any red-flag issues

If any score is under 90, identify the top 3 fixable issues and fix them.

### 12. Final Report

Print a summary:
- ✓ Meta tags: done
- ✓ JSON-LD schemas: [list what was added]
- ✓ Files generated: [list]
- ✓ Images optimized: [N images]
- ✓ Lighthouse scores: [4 numbers]
- ⚠ Manual steps needed: [list any human-required items]

## Rules

- NEVER fabricate data (no fake reviews, no fake FAQs, no fake authors)
- Only inject schemas for data that actually exists on the page
- Preserve the visual design — SEO changes should be invisible to human visitors
- Use data from brand.json + survey answers, not assumptions
- If any required data is missing (phone for LocalBusiness, author for Article),
  flag it to the user and skip that schema rather than inventing it
```

---

## Variables Filled by Skill

- `{{brand_name}}`, `{{tagline}}`, `{{description}}`, `{{industry}}`, `{{audience}}`
- `{{domain}}` (from deploy step or asked)
- `{{location}}`, `{{nap}}`, `{{service_type}}` (if LocalBusiness)

The skill asks for these in Phase 7 start if not already captured.
