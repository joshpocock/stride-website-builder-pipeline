# Kling 3.0 Video Animation Prompt Template

Used to transition the NanoBanana start frame → end frame into a cinematic
5-second animation that will drive the scroll experience.

---

## Variables (filled by skill)

- `{{motion_description}}` — the exact physical motion (e.g., "lid lifts off,
  components drift apart smoothly")
- `{{camera_behavior}}` — "fixed camera" | "slow push-in" | "slow pull-back"
- `{{timing_feel}}` — "smooth and cinematic" | "snappy and mechanical"
- `{{environment_cues}}` — optional atmospheric notes

---

## Template: Exploding View (most common)

```
A single continuous 5-second shot with a fixed camera and no cuts. The
{{product_description}} begins fully assembled as shown in the first image
and gradually deconstructs into the exploded view shown in the second
image. {{motion_description}}. Each component separates with smooth
cinematic timing, each layer drifting apart in sequence. No zoom, no cuts,
no camera rotation, no hand appearing in frame. Maintain identical lighting,
identical background, identical framing throughout. Photorealistic render,
ultra high detail, 1080p quality. Style: {{timing_feel}}.
```

---

## Template: Cinematic Orbit (use Cinema Studio on Higgsfield instead if available)

```
A single continuous 5-second shot. The camera slowly orbits around the
{{product_description}} at a 360-degree angle, revealing all sides. Fixed
subject position, smooth circular camera motion, constant distance. No cuts,
no zoom, no human elements. Identical lighting throughout. Photorealistic,
1080p. Style: cinematic and premium.
```

---

## Template: Dolly Push-In

```
A single continuous 5-second shot. The camera slowly pushes forward toward
the {{product_description}}, moving from the wide framing in the first image
to the close framing in the second image. Constant smooth motion, no
acceleration, no cuts, no zoom lens change (actual camera movement, not
digital zoom). Identical lighting, identical subject, identical background.
Photorealistic, 1080p.
```

---

## Template: Environment Pan

```
A single continuous 5-second shot. The camera pans through a 3D environment
from the starting position shown in image 1 to the ending position shown in
image 2. Smooth cinematic tracking shot, no cuts, no zoom. Maintain identical
lighting and atmosphere throughout. The {{product_description}} may or may
not be in frame — focus is on the environmental motion. Photorealistic, 1080p.
```

---

## Kling 3.0 Settings (always)

| Setting | Value | Why |
|---|---|---|
| Duration | 5 seconds | Sweet spot for scroll loops |
| Quality | 1080p | Minimum for professional output |
| Enhance | OFF | Keep full prompt control |
| Model | Kling 3.0 | Best for start/end frame transitions |
| Aspect ratio | 16:9 | Website hero standard |

Cost: ~$0.36 per generation on Higgsfield, faster on Kie.ai. Budget 2-3
generations per build to pick the best = $1-3 total.

---

## Two-Pass Strategy (Short + Reverse Loop)

If the user picks "short + reverse loop" for seamless looping:

1. Generate ONE 5-second Kling video
2. Use ffmpeg to reverse it: `ffmpeg -i hero.mp4 -vf reverse hero-reverse.mp4`
3. Concatenate: `ffmpeg -f concat -i list.txt -c copy hero-loop.mp4`
4. Result: 10-second seamless loop

Claude Code handles this automatically if the user picks this approach.

---

## Pro Tips from Creators

- **Use Claude Code to write your video prompt** — it generates better prompts
  than you can manually (Nate Herk)
- **Describe the exact physical motion** — not "cool transition" but "the lid
  lifts 15 degrees, the components detach in a starburst pattern, each layer
  drifts 20% further from center"
- **Specify "fixed camera, no cuts, no zoom"** for clean scroll animations
- **For product orbits, use Cinema Studio on Higgsfield** instead of Kling —
  it's purpose-built for circular camera motion
- **Keep enhance OFF** — you want full prompt control, not Kling's
  "improvements" on top
- **Test with 2-3 variants** before picking — Kling has significant variance
  between generations even with identical inputs
