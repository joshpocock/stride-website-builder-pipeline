---
type: research
topic: SEO best practices 2026 for AI-generated premium landing pages (local service businesses)
dateGenerated: 2026-04-04
audience: Claude Code skill that auto-optimizes Next.js/React sites on Vercel/Netlify
stack: Next.js 15 App Router, React, Vercel/Netlify
---

# SEO Research 2026 — Reference for the Website Builder Pipeline Skill

This document is the canonical SEO reference loaded by the `stride-stride-website-builder-pipeline` skill during Phase 7. Every landing page the skill ships for a local service business (dental, restaurant, barber, real estate, fitness) should satisfy the Automated Audit Checklist at the bottom of this file — that checklist is the minimum bar for local-SEO quality, and skipping items there tends to show up as lost AI Overview citations and weaker local pack rankings. Nothing here is generic — every item is directly actionable in code.

## Table of Contents

1. [Google AI Overviews / AI Mode Optimization](#1-google-ai-overviews--ai-mode-optimization)
2. [E-E-A-T Post-2024](#2-e-e-a-t-post-2024)
3. [Core Web Vitals 2026](#3-core-web-vitals-2026)
4. [JSON-LD Structured Data](#4-json-ld-structured-data)
5. [llms.txt / ai.txt](#5-llmstxt--aitxt)
6. [Semantic HTML5 + WCAG 2.2](#6-semantic-html5--wcag-22)
7. [Image SEO 2026](#7-image-seo-2026)
8. [Open Graph + Twitter Cards + oEmbed](#8-open-graph--twitter-cards--oembed)
9. [robots.txt, sitemap.xml, Canonicals, hreflang](#9-robotstxt-sitemapxml-canonicals-hreflang)
10. [Page Speed Budgets](#10-page-speed-budgets)
11. [Mobile-First Indexing](#11-mobile-first-indexing)
12. [Local SEO for Service Businesses](#12-local-seo-for-service-businesses)
13. [Content SEO for Landing Pages](#13-content-seo-for-landing-pages)
14. [Technical SEO Checklist](#14-technical-seo-checklist)
15. [Automated Audit Checklist](#15-automated-audit-checklist)

---

## 1. Google AI Overviews / AI Mode Optimization

### Key findings

- AI Overviews (AIO) now appear on 50–60% of U.S. Google searches. Organic CTR drops up to 61% on queries where AIO shows, **but cited brands earn ~35% higher CTR** and AI-referred visitors convert at roughly **23× traditional organic rates** ([Averi, Mar 2026](https://www.averi.ai/blog/google-ai-overviews-optimization-how-to-get-featured-in-2026)).
- Google upgraded AIO to **Gemini 3** as the global default on **Jan 27, 2026**. Citation behavior has decoupled from classical rankings: only **38% of cited pages** also rank in the top 10 (down from 76% seven months earlier). YouTube is now the single most-cited domain (18.2% of out-of-top-100 citations) ([ALM Corp, Mar 2026](https://almcorp.com/blog/google-ai-overview-citations-drop-top-ranking-pages-2026/)).
- Google's retrieval uses a **"query fan-out"** process — the query is split into sub-queries — so topical depth + multi-format content beats single-keyword optimization ([Digital Applied](https://www.digitalapplied.com/blog/seo-after-ai-overviews-complete-strategy-guide-2026)).
- Pages > 20,000 characters average **~10.18 AIO citations**; short pages average 2.39. Extracted passages favor **134–167 word windows** (62% land in the 100–300 word range).
- **#1 ranking factor for AIO selection: semantic completeness** (r = 0.87) — each paragraph must answer standalone. Apply the **"Island Test"**: if the paragraph were orphaned from the rest of the page, would it still answer the question? ([Wellows, Feb 2026](https://wellows.com/blog/google-ai-overviews-ranking-factors/)).
- Other leading factors: multi-modal integration (+156% selection), verifiable citations (+89%), **entity density ≥ 15 connected entities** in the Knowledge Graph (4.8× boost), explicit schema markup (+73%).
- **Freshness matters**: 65% of AI bot hits target content published in the past year, 89% within 3 years ([The Digital Bloom, Mar 2026](https://thedigitalbloom.com/learn/ai-citation-position-revenue-report-2026/)).

### 2026-specific changes

- AIO is no longer a "SERP feature" — it is the SERP for informational/commercial queries.
- Citations follow **trust graph + semantic density**, not blue-link ranking. You can be cited without ranking, and vice versa.
- AI Mode reads JSON-LD as a **verification signal** even when no rich result shows.

### Actionable checklist (inject every build)

- [ ] Every H2 section answers a complete question in 130–170 words (passes Island Test).
- [ ] Page has `WebPage` + `Organization` + `LocalBusiness` schema wired with `sameAs` pointing to Wikidata, LinkedIn, Crunchbase, GBP, Yelp, Facebook, Instagram.
- [ ] `knowsAbout` array on Organization listing 8–15 relevant services/entities.
- [ ] Each major claim paired with a source the model can verify (link, review, data).
- [ ] `dateModified` updated on every deploy (not just `datePublished`).
- [ ] Mix of text + images + embedded video + structured data on a single URL.

---

## 2. E-E-A-T Post-2024

### Key findings

- E-E-A-T (Experience, Expertise, Authoritativeness, Trust) is a **practical quality filter** for both classical rankings and AI citations, especially on YMYL (dental, finance, legal, health) ([ClickRank](https://www.clickrank.ai/e-e-a-t-and-ai/)).
- Google rewards **hands-on, lived-in content**: real case studies with outcomes, first-party photos, usage duration, behind-the-scenes footage, insider operational detail, experience-based opinions — not abstract summaries ([Keywords Everywhere](https://keywordseverywhere.com/blog/google-e-e-a-t-guidelines-an-overview/)).
- For local service pages the highest-impact experience signals are: **staff bios with real photos and credentials**, **location-specific testimonials with names and dates**, **original photos of the physical location/interior/team**, and **verifiable license numbers** (state dental board, bar, contractor license).
- Author/Article schema is not strictly required but converts trust signals into machine-readable data and improves eligibility for enhanced features.

### Actionable checklist

- [ ] `/about` page exists with named founder/owner + Person schema + real photo.
- [ ] Every staff member has `Person` schema with `jobTitle`, `hasCredential`, `sameAs` (LinkedIn).
- [ ] Reviews displayed on page with schema: `Review` + `aggregateRating` (real ratings only — fake review schema violates Google policy).
- [ ] `Organization.foundingDate`, `Organization.numberOfEmployees` where applicable.
- [ ] `hasCredential` / license number visible and marked up for regulated businesses.
- [ ] At least one first-party photo per major section (no stock photography on hero).

### Person schema snippet

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Dr. Jane Doe",
  "jobTitle": "DDS, Owner",
  "image": "https://example.com/team/jane.jpg",
  "worksFor": { "@type": "Dentist", "name": "Bright Smile Dental" },
  "hasCredential": {
    "@type": "EducationalOccupationalCredential",
    "credentialCategory": "license",
    "recognizedBy": { "@type": "Organization", "name": "Texas State Board of Dental Examiners" },
    "identifier": "12345"
  },
  "alumniOf": "University of Texas Dental Branch",
  "sameAs": [
    "https://www.linkedin.com/in/janedoe-dds",
    "https://www.healthgrades.com/dentist/dr-jane-doe"
  ]
}
```

---

## 3. Core Web Vitals 2026

### Thresholds (75th percentile, field data via CrUX)

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | ≤ **2.5s** | ≤ 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | ≤ **200ms** | ≤ 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ **0.1** | ≤ 0.25 | > 0.25 |
| **FCP** (informational) | ≤ 1.8s | | |
| **TTFB** (informational) | ≤ 800ms | | |

Sources: [web.dev Core Web Vitals](https://web.dev/articles/vitals), [DebugBear](https://www.debugbear.com/docs/core-web-vitals-metrics), [Senorit](https://senorit.de/en/blog/core-web-vitals-2026), [Rivulet IQ](https://www.rivuletiq.com/core-web-vitals-2026-whats-changed-and-how-to-pass/).

### 2026-specific changes

- **INP replaced FID** as the primary interactivity metric in March 2024 — FID is fully retired.
- **Aspirational 2026 targets** (one source reports Google's March 2026 core update tightened internal thresholds to LCP 2.0s / INP 150ms; others still cite 2.5s/200ms). Build for **LCP < 2.0s, INP < 150ms, CLS < 0.05** as stretch targets and you're safe either way.
- Page Experience report in Search Console was retired; CWV + HTTPS reports remain.
- Search Console **groups similar URLs** and applies the worst metric to the whole group — template-level issues poison entire page sets. Fix at the layout level.

### Actionable checklist

- [ ] Hero image is AVIF, preloaded, has `fetchpriority="high"`, explicit `width`/`height`.
- [ ] No layout shifts from web fonts (use `font-display: optional` or `size-adjust`).
- [ ] No CLS from lazy-loaded images (reserve space via aspect-ratio CSS).
- [ ] JS hydration deferred; event handlers attached in `requestIdleCallback` where possible.
- [ ] `content-visibility: auto` on below-the-fold sections.
- [ ] TTFB ≤ 200ms via Vercel/Netlify edge caching.

---

## 4. JSON-LD Structured Data

### Key findings (2026)

- Google's **March 12, 2026 core update** was the biggest structured-data shift since rich snippets launched. Rich-result eligibility narrowed for abused types: **FAQ and HowTo rich results dropped ~47%** on non-primary content pages ([Digital Applied](https://www.digitalapplied.com/blog/schema-markup-after-march-2026-structured-data-strategies)). (Note: Google had already restricted FAQ/HowTo rich results to authoritative government/health sites in August 2023; 2026 narrowed further.)
- AI Mode reads schema as a **trust/verification signal**. Accurate schema lifts AI citation probability **3.2×** even when no rich result shows.
- Highest-leverage schema in 2026 = **entity disambiguation** via `Organization.sameAs` (Wikidata, LinkedIn, Crunchbase, GBP) + `knowsAbout`.
- JSON-LD in `<head>` remains Google's preferred format. Microdata/RDFa offer no benefit.
- Schema must describe the **primary** content of the page, not peripheral content.

### Priority schemas for local service landing pages

1. **Organization** + **LocalBusiness subtype** (Dentist, Restaurant, BarberShop, RealEstateAgent, HealthClub) — required on every page.
2. **WebSite** with `potentialAction` SearchAction — once per domain.
3. **WebPage** — per page.
4. **BreadcrumbList** — per page (even single-level, for knowledge graph).
5. **Service** — one per service offered.
6. **Person** — for each staff member shown.
7. **Review** + `aggregateRating` — only with real, verifiable reviews.
8. **VideoObject** — any embedded video.
9. **FAQPage** — still markup it (helps AIO) even though rich result is gated.
10. **Product** — physical goods only.
11. **Article** — blog/news only, not landing pages.

### Example: Dentist LocalBusiness (complete)

```json
{
  "@context": "https://schema.org",
  "@type": "Dentist",
  "@id": "https://brightsmile.com/#business",
  "name": "Bright Smile Dental",
  "image": [
    "https://brightsmile.com/photos/exterior-1x1.jpg",
    "https://brightsmile.com/photos/interior-4x3.jpg",
    "https://brightsmile.com/photos/team-16x9.jpg"
  ],
  "logo": "https://brightsmile.com/logo.png",
  "url": "https://brightsmile.com",
  "telephone": "+1-512-555-0123",
  "email": "hello@brightsmile.com",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street, Suite 200",
    "addressLocality": "Austin",
    "addressRegion": "TX",
    "postalCode": "78701",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 30.2672,
    "longitude": -97.7431
  },
  "hasMap": "https://www.google.com/maps/place/?q=place_id:ChIJ...",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
      "opens": "08:00",
      "closes": "17:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "09:00",
      "closes": "13:00"
    }
  ],
  "areaServed": [
    { "@type": "City", "name": "Austin" },
    { "@type": "City", "name": "Round Rock" },
    { "@type": "City", "name": "Cedar Park" }
  ],
  "knowsAbout": [
    "Cosmetic dentistry",
    "Dental implants",
    "Invisalign",
    "Teeth whitening",
    "Pediatric dentistry"
  ],
  "medicalSpecialty": "Dentistry",
  "currenciesAccepted": "USD",
  "paymentAccepted": "Cash, Credit Card, Insurance, CareCredit",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "287",
    "bestRating": "5"
  },
  "review": [{
    "@type": "Review",
    "reviewRating": { "@type": "Rating", "ratingValue": "5" },
    "author": { "@type": "Person", "name": "Sarah M." },
    "datePublished": "2026-03-12",
    "reviewBody": "Dr. Doe and the team made my Invisalign experience easy..."
  }],
  "sameAs": [
    "https://www.facebook.com/brightsmiledental",
    "https://www.instagram.com/brightsmiledental",
    "https://www.yelp.com/biz/bright-smile-dental-austin",
    "https://www.google.com/maps/place/?q=place_id:ChIJ...",
    "https://www.healthgrades.com/group-directory/bright-smile-dental"
  ]
}
```

### WebSite + SearchAction

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "url": "https://brightsmile.com",
  "name": "Bright Smile Dental",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://brightsmile.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

### BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://brightsmile.com" },
    { "@type": "ListItem", "position": 2, "name": "Services", "item": "https://brightsmile.com/services" },
    { "@type": "ListItem", "position": 3, "name": "Invisalign" }
  ]
}
```

### Service

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "Invisalign Treatment",
  "provider": { "@id": "https://brightsmile.com/#business" },
  "areaServed": { "@type": "City", "name": "Austin" },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "3500",
    "priceValidUntil": "2026-12-31"
  }
}
```

### FAQPage (still mark it up for AIO even without rich result)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How much does Invisalign cost in Austin?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Invisalign treatment at Bright Smile Dental in Austin ranges from $3,500 to $6,500..."
    }
  }]
}
```

### VideoObject

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Tour of Bright Smile Dental",
  "description": "Take a 60-second tour of our Austin office.",
  "thumbnailUrl": "https://brightsmile.com/video/tour-thumb.jpg",
  "uploadDate": "2026-03-01",
  "duration": "PT1M",
  "contentUrl": "https://brightsmile.com/video/tour.mp4",
  "embedUrl": "https://www.youtube.com/embed/XXXX"
}
```

---

## 5. llms.txt / ai.txt

### Key findings

- **llms.txt adoption is very low and effectiveness is unproven.** SE Ranking's survey of 300k domains found a **10.13% adoption rate**, skewed toward low/medium-traffic sites ([LinkBuildingHQ, Feb 2026](https://www.linkbuildinghq.com/blog/should-websites-implement-llms-txt-in-2026/)).
- A Search Engine Land study of 9 sites found 8 saw **no measurable traffic change**. Google's John Mueller confirmed no AI crawler has verified using it. One analyst calls it **"a dud"** ([Medium / Kai Priestersbach](https://medium.com/@kaispriestersbach/the-llms-txt-is-dead-more-precisely-a-dud-ab7bee4f469c)).
- No major LLM (ChatGPT, Claude, Perplexity, Gemini) has committed to reading `llms.txt`.

### Recommendation

- **Ship it anyway, but spend zero optimization effort on it.** It costs ~2 minutes to generate, signals professionalism, and may become canonical. Treat it as a static artifact.
- Control AI crawlers via `robots.txt` user-agent directives (see §9) — that is where the real control exists today.

### Minimal llms.txt template

```
# Bright Smile Dental
> Family and cosmetic dentistry in Austin, Texas. Invisalign, implants, whitening.

## Core pages
- [Home](https://brightsmile.com): Services overview and booking
- [Services](https://brightsmile.com/services): Full list of dental services
- [About](https://brightsmile.com/about): Meet Dr. Jane Doe and the team
- [Contact](https://brightsmile.com/contact): Address, hours, phone

## Policies
- [Privacy](https://brightsmile.com/privacy)
```

---

## 6. Semantic HTML5 + WCAG 2.2

### Key findings

- **WCAG 2.2 was republished 2024-12-12** and is backwards-compatible with 2.1. It adds **nine new success criteria** and **removes 4.1.1 Parsing** ([W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/)).
- WCAG 2.2 is not a direct ranking factor, but failures produce lawsuits (ADA), worse INP scores, and worse screen-reader crawl behavior by Google.

### New WCAG 2.2 criteria

| # | Criterion | Level | Build impact |
|---|---|---|---|
| 2.4.11 | Focus Not Obscured (Minimum) | AA | Sticky headers must not cover focused elements |
| 2.4.12 | Focus Not Obscured (Enhanced) | AAA | |
| 2.4.13 | Focus Appearance | AAA | Focus ring ≥ 2px, 3:1 contrast |
| 2.5.7 | Dragging Movements | AA | Provide single-pointer alternative (e.g., buttons next to drag handle) |
| **2.5.8** | **Target Size (Minimum)** | **AA** | **Tap targets ≥ 24×24 CSS px** (Google recommends 48×48 for mobile UX) |
| 3.2.6 | Consistent Help | A | Help links in same order on every page |
| 3.3.7 | Redundant Entry | A | Don't re-ask for data in the same flow |
| 3.3.8 | Accessible Authentication (Min) | AA | No cognitive puzzle tests |
| 3.3.9 | Accessible Authentication (Enh) | AAA | |

### Semantic HTML5 checklist

- [ ] One `<h1>` per page, matching primary keyword + intent.
- [ ] `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>` used correctly.
- [ ] Skip-to-content link as first focusable element.
- [ ] `<img alt="...">` on every decorative image uses `alt=""` explicitly.
- [ ] `<button>` for actions, `<a>` for navigation — never the reverse.
- [ ] Forms have `<label for>` on every input.
- [ ] `lang="en"` on `<html>`.
- [ ] Color contrast ≥ 4.5:1 for body text, ≥ 3:1 for large text.
- [ ] Focus visible (don't `outline: none` without replacement).
- [ ] Tap targets ≥ 24×24 CSS px (prefer 48×48).

---

## 7. Image SEO 2026

### Format hierarchy

1. **AVIF** (best): ~50% smaller than JPEG at equal quality, 10/12-bit HDR/wide-color, baseline widely available as of 2026 (Chrome 85+, Firefox 93+, Safari 16+, Edge 93+) ([DEV Baseline 2026](https://dev.to/marianocodes/baseline-web-features-you-can-safely-use-today-to-boost-performance-4bnb)).
2. **WebP**: ~25–35% smaller than JPEG, universal support.
3. **JPEG/PNG fallback**.

### LCP image pattern (copy/paste)

```html
<link rel="preload" as="image" fetchpriority="high"
      href="/hero.avif" type="image/avif"
      imagesrcset="/hero-800.avif 800w, /hero-1600.avif 1600w"
      imagesizes="100vw">

<picture>
  <source type="image/avif" srcset="/hero-800.avif 800w, /hero-1600.avif 1600w" sizes="100vw">
  <source type="image/webp" srcset="/hero-800.webp 800w, /hero-1600.webp 1600w" sizes="100vw">
  <img src="/hero-1600.jpg"
       alt="Dr. Jane Doe greeting a patient at Bright Smile Dental in Austin"
       width="1600" height="900"
       fetchpriority="high"
       decoding="async">
</picture>
```

Sources: [MDN: Fix LCP by optimizing image loading](https://developer.mozilla.org/en-US/blog/fix-image-lcp/), [web.dev LCP](https://web.dev/articles/lcp).

### Key rules

- **`fetchpriority="high"`** — exactly one image per page (the LCP hero). Don't spray it.
- **`loading="lazy"`** on every image below the fold.
- **Never lazy-load the LCP image** — it blocks LCP.
- **Explicit `width` + `height`** on every image (prevents CLS).
- **`decoding="async"`** on all non-critical images.
- **Preload pitfall**: when using `<picture>` with multiple sources, preload only the highest-priority source type (AVIF), not the `<img src>`.
- A 1MB JPEG → AVIF@80 can yield ~95% savings (~46KB).

### Alt text rules

- Describe the image in context of the surrounding content, not literal pixels.
- Include subject + action + location for local SEO: *"Dental hygienist cleaning teeth at Bright Smile Dental in Austin"*.
- 125 characters max. Screen readers truncate beyond that.
- `alt=""` for purely decorative images (icons with adjacent text labels).
- Never keyword-stuff.

### File naming

- `kebab-case-descriptive.avif` — e.g., `invisalign-treatment-austin.avif`.
- Include the primary keyword, location, and business name where natural.
- Avoid `IMG_2394.jpg`, `hero-1.png`, or `final-final-v2.jpg`.

### Next.js 15

Use `<Image>` from `next/image` with `priority` (sets `fetchpriority="high"` and disables lazy) for the LCP image. `next/image` emits AVIF + WebP automatically if `formats: ['image/avif', 'image/webp']` is set in `next.config.js`.

---

## 8. Open Graph + Twitter Cards + oEmbed

### Complete tag set (copy/paste)

```html
<!-- Primary -->
<title>Bright Smile Dental — Cosmetic Dentistry in Austin, TX</title>
<meta name="description" content="Cosmetic dentistry, Invisalign, and dental implants in Austin, TX. 4.9★ (287 reviews). Book online 24/7.">
<link rel="canonical" href="https://brightsmile.com/">

<!-- Open Graph -->
<meta property="og:title" content="Bright Smile Dental — Cosmetic Dentistry in Austin, TX">
<meta property="og:description" content="Cosmetic dentistry, Invisalign, and dental implants in Austin, TX.">
<meta property="og:url" content="https://brightsmile.com/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bright Smile Dental">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="https://brightsmile.com/og.png">
<meta property="og:image:secure_url" content="https://brightsmile.com/og.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Bright Smile Dental exterior with logo">

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@brightsmile">
<meta name="twitter:creator" content="@brightsmile">
<meta name="twitter:title" content="Bright Smile Dental — Cosmetic Dentistry in Austin, TX">
<meta name="twitter:description" content="Cosmetic dentistry, Invisalign, and dental implants in Austin, TX.">
<meta name="twitter:image" content="https://brightsmile.com/og.png">
<meta name="twitter:image:alt" content="Bright Smile Dental exterior with logo">
```

Sources: [imgsrc OG guide](https://imgsrc.io/guides/open-graph-meta-tags), [ogmatic.io](https://medium.com/ogmatic-io/open-graph-images-everything-you-need-to-know-6bbf34cf2da2), [X developers](https://devcommunity.x.com/t/twitter-card-summary-large-image-not-rendering-in-tweet-composer-despite-correct-meta-tags/257497).

### Rules

- **Image: 1200×630 PNG or JPG, < 5 MB, absolute URL with HTTPS**. 2:1 aspect ratio is superseded.
- Use absolute URLs, never relative.
- X caches aggressively — append `?v=2` to force recrawl (the Card Validator no longer shows previews as of 2026).
- `og:locale` for every non-English build; add `og:locale:alternate` for translations.
- Don't omit `og:image:width/height` — some clients (Slack, Discord) refuse to render without them.

### Next.js 15 Metadata API

```ts
// app/layout.tsx
export const metadata = {
  metadataBase: new URL('https://brightsmile.com'),
  title: { default: 'Bright Smile Dental', template: '%s | Bright Smile Dental' },
  description: '…',
  openGraph: {
    title: '…', description: '…', url: 'https://brightsmile.com',
    siteName: 'Bright Smile Dental', locale: 'en_US', type: 'website',
    images: [{ url: '/og.png', width: 1200, height: 630, alt: '…' }]
  },
  twitter: { card: 'summary_large_image', images: ['/og.png'] },
  alternates: { canonical: '/' }
}
```

### oEmbed

For sites that embed media (real estate video tours, fitness class previews), expose an oEmbed discovery tag:

```html
<link rel="alternate" type="application/json+oembed"
      href="https://brightsmile.com/oembed?url=https://brightsmile.com/virtual-tour" title="Virtual Tour">
```

---

## 9. robots.txt, sitemap.xml, Canonicals, hreflang

### robots.txt 2026 template (with AI crawler controls)

```
User-agent: *
Allow: /
Disallow: /admin
Disallow: /api/
Disallow: /_next/static/chunks/
Disallow: /*?*utm_

# AI crawlers — allow (they drive referral traffic)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

# Aggressive scrapers — block
User-agent: CCBot
Disallow: /

User-agent: Bytespider
Disallow: /

Sitemap: https://brightsmile.com/sitemap.xml
```

Block vs allow is a business decision — blocking Google-Extended removes the site from Gemini training data AND AIO eligibility for some query types ([Tencent Cloud](https://www.tencentcloud.com/techpedia/143900)). Default for local service businesses: **allow everything** except abusive scrapers. Visibility > exclusivity.

### sitemap.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://brightsmile.com/</loc>
    <lastmod>2026-04-04</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://brightsmile.com/services/invisalign</loc>
    <lastmod>2026-04-04</lastmod>
  </url>
</urlset>
```

Rules:
- `<lastmod>` must be **accurate** — Google's John Mueller has repeatedly said inflated lastmod values get the whole sitemap ignored.
- Max 50,000 URLs / 50MB uncompressed per sitemap.
- Submit in Google Search Console + Bing Webmaster Tools.
- For multi-location businesses, use a **sitemap index** and split by location.
- In Next.js 15, use `app/sitemap.ts` (auto-generates; returns `MetadataRoute.Sitemap`).

### Canonical rules

- **Self-referencing canonical on every page**, absolute URL.
- One canonical per page — never multiple.
- Canonicalize `http → https`, `www → non-www` (or reverse, pick one), remove trailing slashes consistently, strip tracking params (utm_*, gclid).
- `noindex` wins over canonical — don't combine them.

### hreflang (multi-language/region)

```html
<link rel="alternate" hreflang="en-us" href="https://brightsmile.com/">
<link rel="alternate" hreflang="es-us" href="https://brightsmile.com/es/">
<link rel="alternate" hreflang="x-default" href="https://brightsmile.com/">
```

- Every variant must reference every other variant **and itself**.
- `x-default` is required — points to the language picker or primary version.
- Use ISO 639-1 language + optional ISO 3166-1 region.

---

## 10. Page Speed Budgets

### Targets (compressed/transferred over the wire)

| Asset | Budget |
|---|---|
| **Total JS** | ≤ 170 KB (gzipped) for first load |
| Per-route JS | ≤ 70 KB additional |
| **CSS** | ≤ 60 KB (critical inline ≤ 14 KB) |
| **HTML** | ≤ 50 KB |
| **Images above fold** | ≤ 200 KB total (AVIF) |
| **Fonts** | ≤ 100 KB total (2 weights max, WOFF2, subset) |
| **Total page weight** | ≤ 1 MB |
| **Requests** | ≤ 50 |

Sources: [web.dev performance budgets](https://web.dev/articles/performance-budgets-101), [Next.js perf docs](https://nextjs.org/docs).

### Font loading pattern

```html
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="font" type="font/woff2"
      href="/fonts/inter-var.woff2" crossorigin>

<style>
  @font-face {
    font-family: 'Inter';
    src: url('/fonts/inter-var.woff2') format('woff2-variations');
    font-weight: 100 900;
    font-display: swap;   /* or 'optional' for zero CLS */
    font-style: normal;
  }
</style>
```

- Prefer **self-hosted variable fonts** on Vercel/Netlify edge.
- `font-display: swap` for brand fonts, `optional` when layout stability matters more than font fidelity.
- Next.js 15: use `next/font/google` or `next/font/local` — it auto-optimizes, self-hosts, and eliminates layout shift.
- Subset fonts to only the characters you use (Latin only → ~20 KB from ~120 KB).

### Critical CSS

- Inline the first 14 KB (one TCP packet) of CSS in `<head>`.
- Defer non-critical CSS: `<link rel="preload" as="style" onload="this.rel='stylesheet'">`.
- Use `content-visibility: auto` on below-the-fold sections to skip rendering work.

### JS discipline

- Ship ES modules to modern browsers (`<script type="module">`).
- Use `<link rel="modulepreload">` for critical modules.
- Defer or `async` all non-critical scripts.
- Do not ship polyfills to modern browsers (use `module/nomodule` or bundler targets).
- Route-level code splitting (automatic in Next.js App Router).

---

## 11. Mobile-First Indexing

### Status 2026

- Google **completed** the mobile-first indexing transition in **July 2024**. All sites are now crawled primarily by Googlebot Smartphone. Desktop-only content is effectively invisible.
- There is no longer a "mobile-first indexing" toggle — it's the default.

### Checklist

- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1">`
- [ ] Identical structured data on mobile and desktop.
- [ ] Identical content (text, headings, images) on mobile and desktop — no content hidden behind desktop-only media queries.
- [ ] Tap targets ≥ 48 CSS px (Google's UX recommendation; WCAG 2.2 minimum is 24).
- [ ] Form inputs use appropriate `inputmode` and `type` (`tel`, `email`, `numeric`).
- [ ] Horizontal scroll = never (test at 320 CSS px width).
- [ ] Fonts ≥ 16 px body size.
- [ ] Mobile conversion gap: desktop converts 2× mobile (4.8% vs 2.5%) — invest in mobile form UX ([Lovable](https://lovable.dev/guides/landing-page-best-practices-convert)).

---

## 12. Local SEO for Service Businesses

### Key findings

- Google's 2026 local algorithm shifted weight from **"prominence"** toward **"popularity"** (real GBP interaction metrics: calls, direction requests, website clicks, photo views) ([Digital Applied](https://www.digitalapplied.com/blog/local-seo-2026-google-business-profile-ai-guide)).
- Each GBP location should link to a **unique local landing page** — Google now penalizes template pages that only swap city names ([Digital Applied](https://www.digitalapplied.com/blog/local-seo-2026-google-business-profile-ai-guide)).
- GBP completeness and accuracy now **outweigh website effort** for many local searches ([Big Red SEO](https://www.bigredseo.com/google-business-profile-local-seo/)).
- GBP is a direct feed into AI Overviews for local queries ([Map Ranks](https://www.mapranks.com/2026/01/12/how-google-business-profile-rankings-impact-local-seo-in-2026/)).

### Google Business Profile requirements

- [ ] 100% profile completeness.
- [ ] Primary + secondary categories set precisely (e.g., primary "Dentist", secondary "Cosmetic dentist", "Dental implants provider").
- [ ] 10+ photos: exterior, interior, team, service in action, logo, cover.
- [ ] Hours accurate including holidays.
- [ ] All services listed with descriptions and prices where possible.
- [ ] Weekly GBP post (offers, updates, events).
- [ ] Q&A section seeded with the top 10 real questions + owner answers.
- [ ] Products/Services tab populated.
- [ ] Attributes filled (wheelchair accessible, free wifi, accepts new patients, etc.).
- [ ] Messaging enabled.

### NAP consistency

- [ ] **Name, Address, Phone** identical on GBP, website, Yelp, Facebook, Apple Maps, Bing Places, industry directories (Healthgrades, Zocdoc, TripAdvisor, Zillow, etc.).
- [ ] Phone: one local number (not toll-free); use same formatting everywhere.
- [ ] Address: exactly matches USPS format.

### Review acquisition

- Target: **25+ reviews in first 90 days**, ongoing rate of 4+/month.
- Send review request link via SMS 2 hours after appointment (highest conversion window).
- Respond to **every** review within 48 hours — positive with gratitude + owner name, negative with empathy + offline resolution offer. Response rate is itself a ranking signal.
- Never incentivize reviews (violates Google policy).

### "Near me" + service-area pages

For each service × city combination, ship a dedicated page:
- `/services/invisalign` (service page)
- `/austin/invisalign` (geo landing page for Austin)
- `/round-rock/invisalign` (geo landing page for Round Rock)

Each geo page needs: unique local copy (not a swap), staff who serve that area, local testimonials, local landmarks/neighborhoods referenced, embedded map, local phone if different, LocalBusiness schema with `areaServed`.

### Industry-specific notes

- **Dental**: `Dentist` schema, `medicalSpecialty`, license, insurance accepted list. YMYL — E-E-A-T is critical.
- **Restaurant**: `Restaurant` schema, `servesCuisine`, `menu` URL, `acceptsReservations`, `hasMenu` schema.
- **Barber shop**: `BarberShop` or `HairSalon`, `priceRange`, services with `Offer` pricing.
- **Real estate**: `RealEstateAgent` schema, each listing = `SingleFamilyResidence` or `Apartment` with `offers`, `numberOfRooms`, `floorSize`.
- **Fitness studio**: `HealthClub` or `SportsActivityLocation`, `amenityFeature`, class schedule as `Event` schema.

---

## 13. Content SEO for Landing Pages

### Benchmarks (2026)

- Median landing-page conversion rate: **6.6%**. "Good" ≥ 10%. Top 10%: ≥ 11% ([SEO Sherpa](https://seosherpa.com/landing-page-statistics/)).
- Companies with **40+ landing pages generate 500% more conversions** than those with < 10 ([GetPassionFruit](https://www.getpassionfruit.com/blog/how-to-optimize-landing-pages-for-higher-conversions-the-2026-guide-with-industry-benchmarks)).
- Biggest conversion killer: **message mismatch** between ad and page (bounces > 70%).
- Second killer: load time. **>5s loses 3× more visitors than 1s**.
- A 0.1s mobile speed improvement → **8–10% conversion lift**.

### Word count

- Not a direct ranking factor, but AIO citation correlates strongly with depth: pages > 20,000 characters average 10.18 citations. Landing pages can't be 20k characters without hurting conversion, so:
- **Minimum 800 words, target 1,200–1,800** for a local service landing page.
- Expand via FAQ, service descriptions, testimonials with rich text, neighborhood coverage, not filler.

### Required sections (landing page blueprint)

1. **Hero** — headline matches ad keyword exactly, subhead, CTA, hero image (LCP-optimized), trust bar (licenses, years in business, review count + stars).
2. **Value props** — 3–6 benefit cards with icons.
3. **Services** — each service = own `Service` schema block + 100-word description.
4. **Social proof** — review carousel with real names + dates + photos, review count, average rating, `aggregateRating` schema.
5. **Team** — photos + bios + credentials, `Person` schema.
6. **Process / How it works** — 3–5 steps.
7. **FAQ** — 8–12 real questions, each answered in 130–170 words (Island Test), `FAQPage` schema.
8. **Location + hours** — embedded Google Map, clickable phone, `LocalBusiness` schema.
9. **Final CTA** — sticky mobile CTA + in-page form (≤ 3 fields).
10. **Footer** — NAP, social links with `rel="me"`, policies, sitemap link.

### Trust signals

- Review count + star rating in the hero.
- Third-party badges (BBB A+, Yelp, Google, industry associations).
- "Years in business" stat.
- Insurance/payment logos.
- License numbers (regulated industries).
- Press mentions ("As seen in...").
- Before/after photos (first-party).

### Conversion-focused SEO

- **One** primary CTA, repeated ≥ 3× down the page.
- CTA button ≥ 44 px tall (Google) or 48 px (WCAG-friendly), high contrast, action verb.
- Form ≤ 3 fields above the fold. Additional fields progressively revealed.
- Sticky mobile CTA (click-to-call for service businesses).
- Exit-intent offer (optional).
- Remove all nav that isn't the logo + phone + primary CTA on ad-landing variants.

---

## 14. Technical SEO Checklist

*Full audit checklist lives in §15. This section covers the technical foundation.*

### Core

- [ ] HTTPS everywhere, HSTS header, `http → https` 301.
- [ ] One canonical host (`www` OR non-www), enforced by 301.
- [ ] Trailing-slash consistency enforced.
- [ ] 404 returns proper 404 status, custom page.
- [ ] 500 returns proper 500, custom page.
- [ ] No chains of redirects > 1 hop.
- [ ] `robots.txt` present and valid.
- [ ] `sitemap.xml` present, valid, referenced in robots.txt and submitted to GSC.
- [ ] Canonical URL on every page, self-referencing, absolute.
- [ ] No mixed HTTP content.
- [ ] HTTP/2 or HTTP/3 (automatic on Vercel/Netlify).
- [ ] gzip/brotli compression (automatic on Vercel/Netlify).
- [ ] Strong caching headers on static assets.

### Crawlability

- [ ] All important pages reachable within 3 clicks from homepage.
- [ ] Internal linking rich (every page links to and from ≥ 3 others).
- [ ] No orphan pages.
- [ ] No `noindex` on pages meant to rank.
- [ ] No `Disallow` in robots.txt blocking CSS/JS (Google must render the page).
- [ ] Breadcrumbs on every non-home page.

### Meta

- [ ] Unique `<title>` ≤ 60 characters per page.
- [ ] Unique `<meta description>` ≤ 160 characters per page.
- [ ] Exactly one `<h1>` per page.
- [ ] Logical heading hierarchy (no skipping levels).
- [ ] `<html lang="en">`.
- [ ] `<meta name="viewport">` present.
- [ ] `<meta charset="UTF-8">`.

### Structured data

- [ ] Organization + LocalBusiness subtype on every page.
- [ ] WebSite + SearchAction on homepage.
- [ ] BreadcrumbList on every non-home page.
- [ ] Service schema on every service page.
- [ ] FAQPage schema on pages with FAQs.
- [ ] All schemas validate in [Schema Markup Validator](https://validator.schema.org) and [Google Rich Results Test](https://search.google.com/test/rich-results).

---

## 15. Automated Audit Checklist

**This is the list the skill iterates through on every build.** Each item is a boolean check + a fix action. Save the results to `audit-report.json` next to the build output.

```yaml
# stride-website-builder-pipeline/audit.yaml
crawlability:
  - id: robots_txt_exists
    check: GET /robots.txt returns 200
    fix: generate from template in §9
  - id: sitemap_exists
    check: GET /sitemap.xml returns 200, valid XML
    fix: generate from app/sitemap.ts
  - id: sitemap_in_robots
    check: robots.txt contains "Sitemap:" directive
  - id: canonical_self_ref
    check: every page has <link rel="canonical"> with absolute URL matching the page
  - id: no_noindex_on_landing
    check: no <meta name="robots" content="noindex"> on landing pages
  - id: no_mixed_content
    check: all resources load over HTTPS

meta:
  - id: title_length
    check: <title> 30-60 chars, unique per page
  - id: description_length
    check: <meta name="description"> 100-160 chars, unique per page
  - id: h1_single
    check: exactly one <h1> per page
  - id: heading_hierarchy
    check: no skipped levels (h1 -> h3 without h2)
  - id: html_lang
    check: <html lang="..."> present
  - id: viewport_meta
    check: <meta name="viewport" content="width=device-width, initial-scale=1">
  - id: charset
    check: <meta charset="UTF-8"> in first 1024 bytes

open_graph:
  - id: og_title
  - id: og_description
  - id: og_image  # absolute URL, 1200x630, <5MB
  - id: og_image_dimensions  # width + height tags present
  - id: og_url
  - id: og_type
  - id: og_site_name
  - id: og_locale
  - id: twitter_card  # summary_large_image
  - id: twitter_image

structured_data:
  - id: organization_jsonld
    check: Organization or LocalBusiness subtype present
  - id: localbusiness_complete
    check: name, address (full), geo, telephone, url, openingHoursSpecification, priceRange, image, sameAs (3+)
  - id: breadcrumb_list
    check: BreadcrumbList on every non-home page
  - id: website_schema
    check: WebSite + SearchAction on homepage only
  - id: service_schema
    check: Service schema on every /services/* page
  - id: faq_schema
    check: FAQPage schema where FAQs exist
  - id: validates_rich_results
    check: Google Rich Results Test passes with zero errors
  - id: validates_schema_org
    check: validator.schema.org passes

images:
  - id: lcp_image_preloaded
    check: <link rel="preload" as="image" fetchpriority="high"> for hero
  - id: lcp_image_priority
    check: LCP <img> has fetchpriority="high" and NOT loading="lazy"
  - id: avif_format
    check: <picture> with AVIF source for all content images
  - id: explicit_dimensions
    check: every <img> has width + height attributes
  - id: lazy_below_fold
    check: loading="lazy" on all below-the-fold images
  - id: alt_text
    check: every <img> has alt attribute (empty OK for decorative)
  - id: descriptive_filenames
    check: no IMG_1234.jpg, hero-1.png style generic names

core_web_vitals:
  - id: lcp_under_2500
    check: Lighthouse LCP <= 2500ms (target 2000ms)
  - id: inp_under_200
    check: Lighthouse / field INP <= 200ms (target 150ms)
  - id: cls_under_0_1
    check: Lighthouse CLS <= 0.1 (target 0.05)
  - id: ttfb_under_800
    check: TTFB <= 800ms
  - id: fcp_under_1800
    check: FCP <= 1800ms

performance_budget:
  - id: js_under_170kb
    check: first-load JS <= 170KB gzipped
  - id: css_under_60kb
    check: total CSS <= 60KB
  - id: fonts_under_100kb
    check: fonts total <= 100KB, WOFF2, max 2 weights
  - id: page_under_1mb
    check: total initial page weight <= 1MB
  - id: requests_under_50
    check: <= 50 network requests on initial load
  - id: font_display_swap
    check: font-display: swap or optional on all custom fonts
  - id: font_preload
    check: critical font preloaded

accessibility:
  - id: wcag_22_aa
    check: axe-core passes with zero AA violations
  - id: target_size
    check: all tap targets >= 24x24 CSS px (prefer 48x48)
  - id: color_contrast
    check: body text contrast >= 4.5:1, large text >= 3:1
  - id: focus_visible
    check: focus indicator present on all interactive elements
  - id: skip_to_content
    check: skip link is first focusable element
  - id: form_labels
    check: every <input> has associated <label for>
  - id: button_vs_link
    check: <button> for actions, <a href> for navigation
  - id: semantic_landmarks
    check: <main>, <nav>, <header>, <footer> present and unique

local_seo:
  - id: nap_consistent
    check: name/address/phone in footer matches GBP exactly
  - id: embedded_map
    check: Google Maps embed on contact/location section
  - id: click_to_call
    check: phone number is <a href="tel:...">
  - id: hours_visible
    check: opening hours on page and in schema
  - id: geo_coordinates
    check: LocalBusiness.geo.latitude + longitude present
  - id: area_served
    check: areaServed array with 3+ cities/neighborhoods
  - id: reviews_displayed
    check: aggregateRating shown visually + in schema
  - id: same_as_directories
    check: sameAs array with 5+ URLs (GBP, Yelp, FB, IG, industry directory)

content:
  - id: word_count
    check: main content >= 800 words (target 1200-1800)
  - id: faq_section
    check: FAQ section with 8+ questions, each answer 130-170 words
  - id: h2_island_test
    check: each H2 section answers a complete question standalone
  - id: trust_signals_hero
    check: review count + stars visible above the fold
  - id: cta_above_fold
    check: primary CTA visible without scrolling on mobile
  - id: form_fields
    check: lead form has <= 3 fields above the fold
  - id: team_bios
    check: named team members with photos + credentials
  - id: first_party_photos
    check: no stock photography on hero or team sections

ai_optimization:
  - id: entity_sameAs
    check: Organization.sameAs has >= 5 authoritative URLs including Wikidata if exists
  - id: knows_about
    check: Organization.knowsAbout has 8-15 entities
  - id: date_modified_fresh
    check: dateModified updated on deploy
  - id: llms_txt
    check: /llms.txt exists (even if low priority)
  - id: semantic_completeness
    check: each section passes 130-170 word Island Test

redirects:
  - id: http_to_https
    check: http:// URLs 301 to https://
  - id: www_canonicalization
    check: www/non-www enforced via 301
  - id: trailing_slash
    check: consistent trailing-slash handling
  - id: no_redirect_chains
    check: no redirect chain > 1 hop
  - id: 404_status
    check: 404 page returns 404 HTTP status
```

### How the skill uses this file

1. **Build** the site with Claude Code + Next.js 15.
2. **Run** `lighthouse`, `axe-core`, `pa11y`, and a schema validator against the built output.
3. **Parse** results into the audit.yaml structure above.
4. **For each failure**, the skill runs its corresponding `fix` action (regenerate schema, replace `<img>` with `<picture>`, add preload tags, etc.) and re-audits.
5. **Block deploy** on any crawlability, meta, structured_data, core_web_vitals, or accessibility failure.
6. **Warn** on local_seo, content, or ai_optimization failures.
7. **Save** final `audit-report.json` next to the build output.

---

## Appendix: Key Sources

**Primary authoritative sources**
- [Google Search Central — SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Google Search Central — Structured Data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [web.dev — Core Web Vitals](https://web.dev/articles/vitals)
- [web.dev — LCP optimization](https://web.dev/articles/lcp)
- [web.dev — INP optimization](https://web.dev/articles/inp)
- [MDN — Fix LCP image loading](https://developer.mozilla.org/en-US/blog/fix-image-lcp/)
- [W3C — WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/)
- [Schema.org — LocalBusiness](https://schema.org/LocalBusiness)
- [Next.js Metadata API](https://nextjs.org/docs/app/api-reference/functions/generate-metadata)

**2026 analyses cited inline**
- Averi — [AI Overviews Optimization 2026](https://www.averi.ai/blog/google-ai-overviews-optimization-how-to-get-featured-in-2026)
- ALM Corp — [AI Overview Citations Drop 2026](https://almcorp.com/blog/google-ai-overview-citations-drop-top-ranking-pages-2026/)
- Digital Applied — [SEO After AI Overviews 2026](https://www.digitalapplied.com/blog/seo-after-ai-overviews-complete-strategy-guide-2026)
- Digital Applied — [Schema Markup After March 2026](https://www.digitalapplied.com/blog/schema-markup-after-march-2026-structured-data-strategies)
- Digital Applied — [Local SEO 2026 GBP AI Guide](https://www.digitalapplied.com/blog/local-seo-2026-google-business-profile-ai-guide)
- Digital Applied — [Site Speed Rankings 2026](https://www.digitalapplied.com/blog/site-speed-rankings-2026-march-core-update-performance)
- Wellows — [AI Overview Ranking Factors](https://wellows.com/blog/google-ai-overviews-ranking-factors/)
- The Digital Bloom — [AI Citation Position Revenue Report 2026](https://thedigitalbloom.com/learn/ai-citation-position-revenue-report-2026/)
- Keywords Everywhere — [E-E-A-T Guidelines Overview](https://keywordseverywhere.com/blog/google-e-e-a-t-guidelines-an-overview/)
- ClickRank — [E-E-A-T and AI 2026](https://www.clickrank.ai/e-e-a-t-and-ai/)
- Rivulet IQ — [Core Web Vitals 2026](https://www.rivuletiq.com/core-web-vitals-2026-whats-changed-and-how-to-pass/)
- DebugBear — [Core Web Vitals Metrics](https://www.debugbear.com/docs/core-web-vitals-metrics)
- Senorit — [Core Web Vitals 2026](https://senorit.de/en/blog/core-web-vitals-2026)
- LinkBuildingHQ — [Should You Implement llms.txt 2026](https://www.linkbuildinghq.com/blog/should-websites-implement-llms-txt-in-2026/)
- DEV / Mariano Codes — [Baseline Web Features 2026](https://dev.to/marianocodes/baseline-web-features-you-can-safely-use-today-to-boost-performance-4bnb)
- FreeImages — [WebP vs JPEG vs AVIF 2026](https://blog.freeimages.com/post/webp-vs-jpeg-vs-avif-best-format-for-web-photos)
- Request Metrics — [High Performance Images 2026](https://requestmetrics.com/web-performance/high-performance-images/)
- imgsrc — [Open Graph Meta Tags Guide](https://imgsrc.io/guides/open-graph-meta-tags)
- Tencent Cloud — [AI Crawler Control 2026](https://www.tencentcloud.com/techpedia/143900)
- Big Red SEO — [Google Business Profile 2026](https://www.bigredseo.com/google-business-profile-local-seo/)
- Map Ranks — [GBP Rankings & Local SEO 2026](https://www.mapranks.com/2026/01/12/how-google-business-profile-rankings-impact-local-seo-in-2026/)
- GetPassionFruit — [Landing Page Optimization 2026](https://www.getpassionfruit.com/blog/how-to-optimize-landing-pages-for-higher-conversions-the-2026-guide-with-industry-benchmarks)
- Lovable — [Landing Page Best Practices](https://lovable.dev/guides/landing-page-best-practices-convert)
- SEO Sherpa — [Landing Page Statistics 2026](https://seosherpa.com/landing-page-statistics/)

---

*End of seo-research-2026.md — load this file into the stride-website-builder-pipeline skill and iterate §15 on every build.*
