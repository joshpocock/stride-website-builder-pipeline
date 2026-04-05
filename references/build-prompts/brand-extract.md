# Brand Extract Prompt (Vision)

Used when the user provides screenshots instead of a URL. Feed this to Claude
with the screenshot(s) attached.

---

Look at the attached screenshot(s) and extract a complete brand identity.
Return a JSON object matching this schema exactly:

```json
{
  "name": "string",
  "tagline": "string",
  "description": "string (one sentence)",
  "colors": {
    "primary": "#hex",
    "secondary": "#hex",
    "accent": "#hex",
    "background": "#hex",
    "text": "#hex"
  },
  "fonts": {
    "heading": "font family name",
    "body": "font family name"
  },
  "logo_description": "string (for later regeneration)",
  "personality": ["adjective1", "adjective2", "adjective3"],
  "industry": "string",
  "visual_notes": "string (anything else important)"
}
```

Rules:

1. Colors must be hex codes. Estimate from the pixels in the image. Do NOT
   invent colors that aren't visually present.
2. Font names: identify as closely as you can. If uncertain, use the category
   ("modern sans-serif", "geometric display", etc.) and suggest a Google
   Font alternative.
3. Personality: 3-5 adjectives that describe the overall feel.
4. If anything is unclear from the screenshot, add a note in `visual_notes`
   rather than guessing.
5. Return ONLY the JSON — no commentary, no markdown code fences.
