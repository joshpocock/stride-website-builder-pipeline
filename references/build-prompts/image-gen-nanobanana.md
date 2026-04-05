# Hero Image Generation Prompt Template

Distilled from 13 creator videos. Used to generate the start + end frames for
the Kling 3.0 scroll animation. Works with Nano Banana 2, Nano Banana Pro,
and Gemini 3 Pro Image — the prompt framework is provider-agnostic.

> **See also: `cinematic-frame-method.md`** — the six-layer thinking framework
> (ANCHOR, WORLD, LUMINANCE, AIR, OPTICS, EXCLUSIONS) behind every prompt in
> this file. Use the templates below for standard product heroes. Switch to
> the cinematic frame method when the project is non-standard (environmental
> heroes, editorial/lifestyle, luxury brand tone) or when the first pass from
> these templates does not land.

---

## Provider Selection

The pipeline supports two image providers. The prompt template is the same
for both — only the wrapper script and model name change.

| Provider | Env var | Primary model | Resolution | Cost/img | When to use |
|---|---|---|---|---|---|
| **Wavespeed (preferred)** | `WAVESPEED_API_KEY` | `google/gemini-3-pro-image/text-to-image` | 4K native | $0.025 | Any project where `WAVESPEED_API_KEY` is set. Newest Gemini-family model, cheaper than Nano Banana Pro, 4K means no upscale for retina desktop heroes. |
| **Kie.ai (fallback)** | `KIE_AI_API_KEY` | `nanoBanana2` or `nanoBananaPro` | 2K | $0.013–0.030 | Fallback when Wavespeed key is missing. Battle-tested across all creator tutorials. Excellent at targeted edits. |

Video generation (Kling 3.0) always goes through Kie.ai — Wavespeed does not
replace Kie.ai for video in this pipeline.

**Wrapper scripts:**
- `references/call-wavespeed.py image --model gemini-3-pro --prompt "..." --n 4`
- `references/call-kie.py image --prompt "..." --aspect 16:9 --n 4`

---

## Variables (filled by skill)

- `{{product_description}}` — what the hero subject is
- `{{brand_colors}}` — palette from brand.json
- `{{background}}` — "pure black" | "clean white" | "environmental"
- `{{vibe}}` — the archetype (Ethereal Glass, Brutalist, etc.)
- `{{aspect_ratio}}` — typically 16:9
- `{{resolution}}` — 2K minimum

---

## Template: Start Frame (intact product)

```
Professional studio-grade photograph of {{product_description}}, fully
assembled and intact, centered in the frame against a {{background}}
background. Completely flat even lighting, no shadows, no hands, no
reflections, no people. Product occupies ~60% of the frame with clean
negative space on all sides — nothing touching the edges. 16:9 aspect
ratio, {{resolution}} resolution, photographic realism, ultra high detail,
sharp focus throughout. Brand palette: {{brand_colors}}. Style match:
{{vibe}}. Do not add any text, watermarks, or logos unless explicitly
described.
```

---

## Template: End Frame (exploded/deconstructed)

```
Same {{product_description}} as the previous image, but now in an exploded
/ deconstructed view. All internal components separated and floating in 3D
space with the same framing, same lighting, same {{background}} background.
Each component clearly visible and identifiable. Components arranged
symmetrically around the center. No hands, no shadows, no reflections.
16:9 aspect ratio, {{resolution}} resolution. Maintain perfect visual
continuity with the start frame — same camera angle, same lighting, same
scale. Brand palette: {{brand_colors}}. Style: {{vibe}}.
```

---

## Hard Rules (apply to every generation)

1. **No shadows, no hands, no reflections** — always in the prompt
2. **Nothing touching edges** — clean negative space
3. **16:9 aspect ratio** — website hero standard
4. **2K minimum resolution** — Jack Roberts rule
5. **Reference images welcome** — upload product photos + logo for consistency
6. **Generate 4 variants** — pick the best
7. **No text/watermarks** unless explicitly requested
8. **Match lighting between start + end** — this is critical for the Kling
   transition to look seamless

---

## Non-Product Hero Alternatives

If the project isn't a product (e.g., a service business like a dental office):

### Environmental hero

```
Cinematic wide-angle photograph of a {{environment}} (e.g., a modern
minimalist dental clinic reception, warm natural light from large windows,
soft morning sun, plants visible, warm wood accents). Empty of people.
Professional architectural photography style, shallow depth of field,
16:9 aspect ratio, 2K resolution. Color palette: {{brand_colors}}. Vibe:
{{vibe}}.
```

### Abstract hero

```
Abstract 3D composition of {{shapes}} in the colors {{brand_colors}},
floating in space against a {{background}} background. Soft volumetric
lighting, photorealistic render, studio quality, 16:9 aspect ratio,
2K resolution. Style: {{vibe}}.
```

---

## Style Adjustments per Vibe

| Vibe | Background | Lighting | Mood |
|---|---|---|---|
| Ethereal Glass | soft gradient navy | diffuse with rim light | serene, premium |
| Editorial Luxury | ivory or deep burgundy | dramatic single-source | sophisticated |
| Soft Structuralism | warm cream | golden hour natural | organic, inviting |
| Brutalist | pure white or pure black | harsh flat | raw, mechanical |
| Minimalist | off-white | even studio | calm, precise |

---

## JSON Prompting Mode (Dan Kieft technique)

For complex scenes, switch to JSON:

```json
{
  "subject": "{{product_description}}",
  "state": "fully assembled",
  "background": "{{background}}",
  "lighting": {
    "style": "studio flat",
    "shadows": "none",
    "reflections": "none"
  },
  "composition": {
    "aspect_ratio": "16:9",
    "framing": "centered, 60% of frame",
    "negative_space": "clean, nothing touching edges"
  },
  "rules": ["no hands", "no people", "no text", "no watermarks"],
  "style": "{{vibe}}",
  "palette": {{brand_colors}},
  "resolution": "{{resolution}}"
}
```

Dan Kieft: JSON prompting is more accurate than natural language for detailed
scenes, especially product shots with specific requirements.
