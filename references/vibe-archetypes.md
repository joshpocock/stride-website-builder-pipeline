# Vibe Archetypes

Six preset aesthetics that bundle taste-skill dials, font pairing, color palette, motion style, and reference sites. User picks one and gets a tuned premium result without needing to understand the dials.

---

## 1. Ethereal Glass

**Taste-skill dials:** DESIGN_VARIANCE=9, MOTION_INTENSITY=7, VISUAL_DENSITY=3
**Fonts:** Cabinet Grotesk (heading) + Inter (body)
**Colors:** Deep navy (#0B1220) bg, frosted white (#F8F9FB) surfaces, electric blue (#6699FF) accent, glass borders rgba(255,255,255,0.1)
**Motion:** Spring physics, staggered reveals, parallax scroll, backdrop-filter blur
**Best for:** SaaS with premium positioning, creative agencies, AI product pages
**Reference sites:** linear.app, vercel.com, raycast.com
**ASCII preview:**
```
┌─────────────────────────────┐
│  logo           menu  cta   │
│                             │
│    ╔═══════════════╗        │
│    ║ hero + blur   ║        │
│    ║ floating card ║        │
│    ╚═══════════════╝        │
│                             │
│  ◆ feature  ◆ feature       │
└─────────────────────────────┘
```

---

## 2. Editorial Luxury

**Taste-skill dials:** DESIGN_VARIANCE=6, MOTION_INTENSITY=4, VISUAL_DENSITY=5
**Fonts:** Playfair Display (heading, serif) + Inter (body)
**Colors:** Ivory (#FAF8F3) bg, near-black (#1A1A1A) text, burgundy (#6B1B2E) accent, gold (#BA9926) highlight
**Motion:** Gentle fades, line-reveal on scroll, no bouncy spring physics
**Best for:** Law firms, high-end real estate, luxury services, wedding/event brands
**Reference sites:** aesop.com, theweek.com, nytimes.com (editorial sections)
**ASCII preview:**
```
┌─────────────────────────────┐
│ BRAND              menu     │
│─────────────────────────────│
│                             │
│   Headline in serif type    │
│   sitting on ivory space    │
│                             │
│   Read story →              │
│                             │
│  ─── contrast rule ───      │
└─────────────────────────────┘
```

---

## 3. Soft Structuralism

**Taste-skill dials:** DESIGN_VARIANCE=7, MOTION_INTENSITY=5, VISUAL_DENSITY=4
**Fonts:** Satoshi (heading) + Inter (body)
**Colors:** Warm cream (#F5F0E8) bg, charcoal (#2C2824) text, terracotta (#C85841) accent, sage (#7D9471) secondary
**Motion:** Organic easing, rounded shape transitions, no harsh cuts
**Best for:** Wellness brands, artisanal food, boutique hotels, eco-friendly products
**Reference sites:** oatly.com, allbirds.com, goop.com
**ASCII preview:**
```
┌─────────────────────────────┐
│  ◯ brand       menu         │
│                             │
│   ╭─── big rounded ───╮     │
│   │   organic hero    │     │
│   │   imagery goes    │     │
│   ╰───── here ────────╯     │
│                             │
│  ◯ ──── ◯ ──── ◯            │
└─────────────────────────────┘
```

---

## 4. Brutalist

**Taste-skill dials:** DESIGN_VARIANCE=9, MOTION_INTENSITY=3, VISUAL_DENSITY=7
**Fonts:** JetBrains Mono (everything) or Space Grotesk (heading) + IBM Plex Mono (body)
**Colors:** Pure white (#FFFFFF) or pure black (#111111) bg, electric accent (#FF3B00 or #00FF88), thick borders, grid lines
**Motion:** Snap transitions, instant hover states, no easing
**Best for:** Tech tooling, dev platforms, CRT terminal vibes, anti-design portfolios
**Reference sites:** bun.sh, deno.com, railway.app
**ASCII preview:**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ [brand]         [menu] [cta]┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                             ┃
┃   MONO HEADING ▮            ┃
┃   raw.factual.copy          ┃
┃                             ┃
┃  [button]  [button]         ┃
┃                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 5. Minimalist

**Taste-skill dials:** DESIGN_VARIANCE=5, MOTION_INTENSITY=4, VISUAL_DENSITY=3
**Fonts:** Geist (everything) or Inter (body) + Cabinet Grotesk (heading)
**Colors:** Off-white (#FAFAFA) bg, deep gray (#1C1C24) text, single accent (#0066CC or #EA580C), soft dividers
**Motion:** Linear fades, no bouncy motion, small hover shifts
**Best for:** Developer portfolios, productivity tools, minimalist SaaS, Notion/Linear-style
**Reference sites:** notion.so, linear.app, cal.com
**ASCII preview:**
```
┌─────────────────────────────┐
│ brand              menu     │
│                             │
│   Clean heading             │
│   One sentence sub-copy     │
│                             │
│   [Primary CTA]             │
│                             │
│  ┌──┐  ┌──┐  ┌──┐  bento    │
│  └──┘  └──┘  └──┘           │
└─────────────────────────────┘
```

---

## 6. Custom

User pastes a reference URL + 3 adjectives. Skill generates a new archetype on the fly using:

1. Fetch HTML via view-page-source.com
2. Extract computed colors, fonts, layout patterns
3. Combine with the 3 adjectives as style guidance
4. Generate taste-skill dials from the adjective strength (e.g., "bold/dynamic/playful" → high variance + high motion)
5. Save as a one-time archetype for this project

---

## How To Use These in Build Prompts

In `site-build-premium.md`, reference the archetype like this:

```
Apply the {{vibe}} archetype:
- taste-skill dials: DESIGN_VARIANCE={{design_variance}}, MOTION_INTENSITY={{motion_intensity}}, VISUAL_DENSITY={{visual_density}}
- Heading font: {{heading_font}}
- Body font: {{body_font}}
- Color palette: bg={{bg}}, text={{text}}, accent={{accent}}, secondary={{secondary}}
- Motion style: {{motion_style}}
- Reference sites: {{reference_sites}}
```

The skill fills in the placeholders based on the picked archetype before sending the prompt to Claude Code.

---

## Audience → Archetype Default Mapping

| Audience type | Default archetype |
|---|---|
| Law firm, medical, finance | Editorial Luxury or Minimalist |
| Creative agency, art, photography | Ethereal Glass or Custom |
| Tech SaaS, dev tools, AI | Brutalist or Minimalist |
| Wellness, food, boutique, lifestyle | Soft Structuralism |
| Luxury retail, fashion, high-end hospitality | Editorial Luxury |
| Developer portfolio | Brutalist or Minimalist |
| Local service (dentist, salon, restaurant) | Soft Structuralism or Minimalist |

This mapping runs automatically based on Q4 audience text. User can override.
