# Stitch Section Prompt Templates

Per-section prompt templates for Phase 2.5. Each template is filled with brand + vibe + audience variables, then passed to `mcp__stitch__generate_screen_from_text`.

All templates share a common **suffix** that enforces anti-slop rules:

```
ANTI-PATTERNS (do NOT do any of these):
- Centered hero headline with subtitle and two buttons (only acceptable if vibe = Editorial Luxury)
- 3-column equal-width feature card rows
- AI cliché copy: "Elevate your", "Seamless integration", "Unlock the power", "Empower teams"
- Inter, Roboto, or Arial as the heading font
- Pure black (#000000) backgrounds — use a warm dark tone instead
- Purple/neon gradients unless vibe = Brutalist or Custom
- Emoji in UI text
- Spinner loaders — use skeletal loaders instead

REQUIRED PATTERNS:
- Asymmetric or Bento-grid layouts
- Staggered reveal animation hints (add data-animate attributes)
- Semantic HTML5 (<header>, <section>, <nav>, <main>, <footer>, <article>)
- WCAG 2.2 AA contrast ratios
- Responsive breakpoints at 640px, 768px, 1024px, 1280px
```

---

## Hero Section

```
Hero section for {{brand_name}}, {{brand_description}}.

Target audience: {{target_audience}}
Vibe: {{vibe_archetype}} ({{vibe_description}})
Brand colors: primary {{brand.colors.primary}}, accent {{brand.colors.accent}}
Headline direction: {{tagline}}

Layout requirements:
- Left-aligned headline (NOT centered unless vibe = Editorial Luxury)
- Subhead 1-2 lines max
- ONE primary CTA button + one secondary text link (no double-button hero)
- Space reserved on the right for a hero video/image (we'll replace this with a scroll-bound animation in the build step — leave it as a placeholder block sized for 16:9)
- Visible trust signals BELOW the fold line (logo row or social proof stat) — not in the hero itself

{{ANTI_PATTERNS_BLOCK}}
```

---

## Features / Benefits Section

```
Features section for {{brand_name}}.

Audience: {{target_audience}}
Vibe: {{vibe_archetype}}
Content direction: {{feature_hints}} (from survey Q3 description, infer 3-5 real features)

Layout requirements:
- Bento-grid or asymmetric card layout — NOT 3 equal columns
- Each feature: icon + headline + 1-2 sentence description
- Mix card sizes (one large "hero feature", others smaller)
- Icons should be abstract or line-art, not decorative illustrations
- Include one feature card that spans 2 columns with a small inline visualization (chart, diagram, or stat)

{{ANTI_PATTERNS_BLOCK}}
```

---

## Pricing Section

```
Pricing section for {{brand_name}}.

Audience: {{target_audience}}
Vibe: {{vibe_archetype}}
Tier count: 3 (Starter / Pro / Enterprise — infer realistic pricing from {{brand_description}})

Layout requirements:
- 3 side-by-side tiers
- Middle tier visually emphasized (elevated, glow, badge, or larger)
- Each tier: name, price, billing cadence, 5-7 feature checkmarks, CTA button
- Currency and billing period clearly marked
- "Most popular" or "Recommended" badge on the emphasized tier
- Monthly/annual toggle above the tiers

{{ANTI_PATTERNS_BLOCK}}
```

---

## Testimonials / Reviews Section

```
Testimonials section for {{brand_name}}.

Audience: {{target_audience}}
Vibe: {{vibe_archetype}}

Layout requirements:
- 3-4 testimonial cards in a masonry or offset grid (NOT a carousel by default)
- Each card: quote (2-3 sentences), attribution (name + role + company), avatar, optional star rating
- Include one "featured" testimonial that's 2x the size of the others
- Avatar photos should be round, with a subtle border in brand accent color

{{ANTI_PATTERNS_BLOCK}}
```

---

## FAQ Section

```
FAQ section for {{brand_name}}.

Audience: {{target_audience}}
Vibe: {{vibe_archetype}}

Layout requirements:
- Accordion pattern, left-aligned
- 5-7 questions with realistic, specific answers (not generic fluff)
- Questions phrased as the user would ask them, not marketing speak
- First question expanded by default
- Subtle + / − icons on each row
- Two-column layout on desktop (questions 1, 3, 5 on left; 2, 4, 6 on right) for Brutalist/Minimalist vibes; single column for Editorial Luxury

{{ANTI_PATTERNS_BLOCK}}
```

---

## CTA / Contact Form Section

```
CTA section for {{brand_name}}.

Audience: {{target_audience}}
Vibe: {{vibe_archetype}}
CTA action: {{primary_cta_action}} (e.g., "Book a call", "Start free trial", "Request a quote")

Layout requirements:
- Full-width banner with strong headline
- Either: (a) a single prominent CTA button with supporting text, OR (b) an inline email-capture form with a single field + button
- Background should be a solid brand accent color or a subtle gradient using primary + secondary
- No form with more than 2 fields in this section (longer forms belong on a dedicated contact page)

{{ANTI_PATTERNS_BLOCK}}
```

---

## Gallery / Portfolio Section

```
Gallery section for {{brand_name}}.

Audience: {{target_audience}}
Vibe: {{vibe_archetype}}

Layout requirements:
- Masonry or bento grid with 6-9 items at varied sizes
- Each item: image placeholder (we'll replace with real assets in the build step), title, 1-line description on hover
- Filter chips at the top if the gallery has categories
- Lightbox/modal behavior implied (but not rendered in this screen)

{{ANTI_PATTERNS_BLOCK}}
```

---

## Team / About Section

```
Team section for {{brand_name}}.

Audience: {{target_audience}}
Vibe: {{vibe_archetype}}

Layout requirements:
- 3-6 team members in a grid
- Each card: photo, name, role, one-sentence bio, social links (LinkedIn, Twitter/X, personal site)
- Photos consistent in framing and color treatment
- Hover state reveals longer bio or swaps to a candid photo

{{ANTI_PATTERNS_BLOCK}}
```

---

## Blog Preview Section

```
Blog preview section for {{brand_name}}.

Audience: {{target_audience}}
Vibe: {{vibe_archetype}}

Layout requirements:
- 3 recent post cards
- Each card: cover image placeholder, category tag, headline, excerpt (2 lines), date, read time
- "View all posts" link aligned top-right of the section
- One card featured as 2x size if there's a clear hero post

{{ANTI_PATTERNS_BLOCK}}
```

---

## Custom / User-Defined Section

When the user adds a custom section via Q11's "+ Add your own" free-text field, use this template:

```
{{custom_section_name}} section for {{brand_name}}.

User's description of what this section should contain:
{{custom_section_description}}

Audience: {{target_audience}}
Vibe: {{vibe_archetype}}

Layout requirements:
- Interpret the user's description literally — do not add unrelated elements
- Match the visual density and motion intensity of the rest of the site
- If the description is ambiguous, default to an asymmetric single-column layout with one hero element and supporting content

{{ANTI_PATTERNS_BLOCK}}
```

---

## How the skill uses these templates

1. Load this file at the start of Phase 2.5
2. For each section in Q11's selected list, find the matching template (hero/features/pricing/etc.)
3. Substitute `{{brand_*}}`, `{{vibe_*}}`, `{{target_audience}}`, `{{tagline}}`, etc. from `brand.json` and survey answers
4. Append the shared `{{ANTI_PATTERNS_BLOCK}}` from the top of this file
5. Pass the final string as `prompt` to `mcp__stitch__generate_screen_from_text`
6. Use `modelId: GEMINI_3_1_PRO` by default, fall back to `GEMINI_3_FLASH` on rate limits
