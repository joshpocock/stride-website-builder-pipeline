# Survey Questions Spec

Full question spec for the website-builder-pipeline skill. Each question is invoked via `AskUserQuestion`. Questions are adaptive — skip or rewrite based on earlier answers.

---

## Q1: Project Type

**question:** "What are we building?"
**header:** "Project type"
**options:**
- Landing page (single scroll, conversion-focused)
- Multi-page site (home + about + services + contact)
- Full app (auth, database, dashboard)
- Portfolio (personal or creative)

**default recommendation:** Landing page (first option, labeled Recommended)

**adaptive:** If "Full app" → also trigger Lovable/Bolt recommendation path instead of Claude Code from scratch.

---

## Q2: Brand Source

**question:** "Where does the brand come from?"
**header:** "Brand source"
**options:**
- Existing website URL (Firecrawl extracts everything)
- Upload logo + colors + fonts manually
- Build from scratch (I'll define it with you)
- Screenshots (Claude vision extracts from images)

**adaptive:**
- "Existing URL" → ask for URL, then skip Q6 color palette, Q7 fonts
- "Screenshots" → request uploads, use vision extraction
- "Build from scratch" → keep Q6 + Q7, add sub-questions
- "Upload manually" → parse inputs into brand.json

---

## Q3: Business Info (free text, multi-part)

- Company name
- Tagline (10-15 words)
- One-sentence description

If Q2 = "Existing URL", pre-fill from Firecrawl extract and ask "does this look right?".

---

## Q4: Target Audience (free text)

"Who is this for? (industry, age range, what they care about)"

Used to tune copy tone, imagery style, section emphasis.

---

## Q4b: Competitor/Inspiration Sources (optional)

**question:** "Do you have competitor or inspiration sites you want to copy structure from?"
**header:** "Inspiration"
**options:**
- Yes, I have URLs to paste
- Yes, I have screenshots
- No, let me pick from curated examples
- Skip

If URLs: fetch HTML via view-page-source.com, save to `project/inspiration/`
If screenshots: save to `project/inspiration/`, pass to build prompt via vision
If curated: show links from `references/design-inspiration.md`

---

## Q5: Vibe Archetype

**question:** "Pick a vibe (or let me suggest one based on your brand)"
**header:** "Vibe"
**options with previews (ASCII mockups — see vibe-archetypes.md):**
- Ethereal Glass — Frosted, translucent, layered
- Editorial Luxury — Magazine-grade, high contrast, serif
- Soft Structuralism — Organic geometry, warm tones
- Brutalist — Raw mechanical, monospace, grid
- Minimalist — Warm monochrome, bento grids, serif+sans
- Custom — Paste a URL and 3 adjectives, I generate a new archetype

Each option's `preview` field shows a small ASCII layout mockup.

**adaptive:** If Q4 mentions "law firm / medical / finance" → default to Editorial Luxury or Minimalist. If "creative agency / art" → default to Ethereal Glass or Custom. If "tech startup / SaaS" → default to Brutalist or Minimalist.

---

## Q6: Color Palette (skipped if Q2 = Existing URL with successful Firecrawl)

**question:** "How do you want colors handled?"
**header:** "Colors"
**options:**
- Use extracted brand colors (if Firecrawl ran)
- Pick from preset palettes (see vibe-archetypes.md)
- Custom hex codes (I'll enter 4)
- AI suggests based on vibe + target audience

---

## Q7: Font Pairing

**question:** "Font pairing?"
**header:** "Fonts"
**options:**
- Geist + Satoshi (modern, taste-skill default)
- Cabinet Grotesk + Inter (editorial)
- JetBrains Mono + Space Grotesk (mager's stack)
- Playfair + Inter (luxury)
- Custom — I'll name them

**adaptive:** Pre-select based on vibe archetype.

---

## Q8: Hero Animation

**question:** "What hero animation style?"
**header:** "Hero animation"
**options:**
- Exploded view (product decomposes into layers) — Recommended for products
- Cinematic orbit (camera rotates around product)
- Dolly zoom (camera pushes toward/away)
- Environment pan (camera travels through a 3D scene)
- Static image (no animation)
- I have my own MP4 to use

**adaptive:** If "Static" or "Own MP4" → skip Q9 image generation details.

---

## Q9: Product Images (skipped if static or own MP4)

**question:** "How should we handle product imagery?"
**header:** "Images"
**options:**
- AI-generate via NanoBanana 2 (Recommended)
- Upload my own product photos
- Mix (some AI, some real)

**adaptive:** If "Upload" → request file paths. If "Mix" → ask what to upload vs generate.

---

## Q10: Sections Needed (multi-select)

**question:** "Which sections does the site need?"
**header:** "Sections"
**multiSelect:** true
**options:**
- Hero (always required)
- Features / Benefits
- Pricing
- Testimonials / Reviews
- Team / About
- FAQ
- CTA / Contact Form
- Gallery / Portfolio
- Blog preview

---

## Q11: Deploy Target

**question:** "Where should we deploy?"
**header:** "Deploy"
**options:**
- Vercel + GitHub (Recommended — auto-deploys on push)
- Netlify (free forever, simple)
- Cloudflare Pages (Leon Furze favorite)
- Manual (I'll handle it myself)
- Skip deploy for now

---

## Q12: Budget Tier

**question:** "Budget tier?"
**header:** "Budget"
**options:**
- Free ($0 — Google AI Studio, free Vercel, slower)
- Budget (~$5 — Kie.ai credits, fast generation)
- Pro (~$20 — Higgsfield + full skill stack + Lighthouse audit)

**adaptive:**
- Free → force image/video gen to Google AI Studio, skip Kie.ai path
- Budget → default to Kie.ai, recommend basic skills
- Pro → enable full stack including premium integrations

---

## Q13: Integrations (multi-select, conditional on Q12)

**question:** "Which integrations should we use?"
**header:** "Integrations"
**multiSelect:** true
**options:** (filtered by Q12 tier)
- Firecrawl (brand extraction)
- Kie.ai (NanoBanana + Kling)
- Higgsfield (unified AI platform)
- Google AI Studio (free NanoBanana)
- GitHub (code storage)
- Vercel (deploy + MCP)
- Netlify (deploy)
- 21st.dev Magic MCP (component picker)
- Google Stitch MCP (design exploration)
- cc-nano-banana skill (NanoBanana inside Claude Code)
- Lighthouse CLI (SEO audit)

Each selected integration → corresponding env var row in `.env` template.

---

## Q14: Inspiration (free input, optional)

"Paste any URLs or drop screenshots of sites you want this to look like or learn from."

- URLs → fetched via view-page-source.com, saved to `inspiration/`
- Screenshots → saved to `inspiration/`, referenced in build prompt
- Empty → skip

---

## Q15: SEO Tier

**question:** "SEO optimization level?"
**header:** "SEO"
**options:**
- Full audit (Recommended) — JSON-LD schemas, meta, sitemap, llms.txt, Lighthouse check
- Basic — meta tags + OG + sitemap only
- Skip — no SEO pass

**adaptive:** If Q4 audience = "local service business" → strongly recommend Full Audit (local SEO matters most here).

---

## Q16 (Confirmation): Plan Summary

Generate a summary of everything and ask:

```
Here's what I'll do:

1. Brand: [name] from [source]
2. Vibe: [archetype] with colors [hex list] and fonts [heading + body]
3. Hero: [animation type] generated via [tool]
4. Sections: [list]
5. SEO: [tier]
6. Deploy: [target]
7. Estimated cost: $[X]
8. Estimated time: [X] minutes

Proceed?
```

**Options:**
- Looks good, run it
- Let me change [X]
- Cancel

---

## Adaptive Rules Summary

| If user says... | Then skip or rewrite... |
|---|---|
| Free budget | Skip Kie.ai, force Google AI Studio |
| I have my own video | Skip Q9 image generation |
| No hero animation | Skip Q9 entirely |
| Build from scratch | Keep Q6+Q7, add color picker sub-Q |
| Existing URL brand | Skip Q6, Q7 (use extracted) |
| Local service business target | Force Full SEO + LocalBusiness schema |
| Creative/portfolio site | Default Ethereal Glass or Custom vibe |
| Tech SaaS | Default Brutalist or Minimalist vibe |
| First time user (no history) | Explain each tool before asking |
| Repeat user | Pre-fill from history.json |

## Escape Hatches

Every question supports these as implicit sub-options via "Other":
- "Skip this question"
- "Let me paste this manually"
- "Show me a screenshot of what you mean"
- "Use the default"

The skill never blocks on a question. If the user skips, use sensible defaults from vibe archetype + budget tier.
