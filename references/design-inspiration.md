# Design Inspiration Library

Curated reference sites and resources the skill can show users when they
answer Q14 "Do you have inspiration?" with "No, let me pick from curated."

---

## By Vibe Archetype

### Ethereal Glass
- https://linear.app
- https://vercel.com
- https://raycast.com
- https://arc.net
- https://orbital.so

### Editorial Luxury
- https://aesop.com
- https://www.theweek.com
- https://www.nytimes.com (editorial)
- https://www.rapha.cc
- https://fortnumandmason.com

### Soft Structuralism
- https://oatly.com
- https://allbirds.com
- https://www.goop.com
- https://www.everlane.com
- https://gardens.com

### Brutalist
- https://bun.sh
- https://deno.com
- https://railway.app
- https://shadcn.com
- https://www.val.town

### Minimalist
- https://notion.so
- https://cal.com
- https://stripe.com
- https://resend.com
- https://clerk.com

---

## By Section Type

### Hero Sections
- https://apple.com — scroll-driven product reveal
- https://framer.com — springy 3D hero
- https://cursor.sh — minimalist with video
- https://runway.com — video-first hero
- https://retool.com — product UI hero

### Pricing
- https://linear.app/pricing
- https://vercel.com/pricing
- https://stripe.com/pricing
- https://cal.com/pricing

### Features/Benefits
- https://notion.so/product
- https://figma.com
- https://superhuman.com

### Testimonials
- https://posthog.com (customer stories)
- https://clerk.com
- https://supabase.com

### Team/About
- https://basecamp.com/about
- https://supabase.com/company

### FAQ
- https://resend.com
- https://nango.dev

---

## Design Galleries

| Gallery | URL | Best For |
|---|---|---|
| Godly | https://godly.website | Premium landing pages |
| Land-book | https://land-book.com | Landing page database |
| One Page Love | https://onepagelove.com | Single-page design |
| Httpster | https://httpster.net | Modern web design |
| SiteInspire | https://siteinspire.com | Curated award-winners |
| Dribbble | https://dribbble.com/tags/landing-page | Landing page designs |
| Awwwards | https://awwwards.com | Award-winning sites |
| Footer.design | https://footer.design | Footer inspiration |

---

## Component Sources

| Source | URL | What It Offers |
|---|---|---|
| 21st.dev | https://21st.dev | Community components with Claude prompts |
| shadcn/ui | https://ui.shadcn.com | Foundation component library |
| Magic UI | https://magicui.design | Animated components |
| Aceternity UI | https://ui.aceternity.com | 3D and motion components |
| Cult UI | https://cult-ui.com | Premium animated components |
| Motion Primitives | https://motion-primitives.com | Framer Motion primitives |
| shadcntemplates.com | https://shadcntemplates.com | shadcn templates |

---

## Pinterest Searches That Actually Work

Viktor Oddy's rule: "Do not go to Google and type portfolio site — go to Pinterest."

Good Pinterest searches:
- "landing page design"
- "web design hero"
- "saas landing page"
- "product landing page"
- "dark mode website"
- "editorial web design"
- "brutalist website"

Bad searches (Pinterest returns garbage):
- "portfolio site"
- "website template"
- "cool websites"
- "modern website"

---

## Competitor Analysis Workflow

When the user says "I want to beat this competitor site":

1. Fetch HTML via view-page-source.com → save to `inspiration/{competitor}.html`
2. Take a full-page screenshot → save to `inspiration/{competitor}.png`
3. Run an analysis prompt:
   ```
   Analyze this competitor site. Identify:
   - Layout rhythm and section order
   - Typography choices
   - Color palette
   - Animation/motion patterns
   - What works well (steal this)
   - What's weak (improve on this)
   - Gaps or missing sections
   ```
4. Use the analysis to inform the build prompt
5. Explicitly instruct Claude: "Use this as structural inspiration only. Do
   NOT visually copy. Improve on their weaknesses."

This is Jack Roberts' HTML scaffolding technique, automated.
