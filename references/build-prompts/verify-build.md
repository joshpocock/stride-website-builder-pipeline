# Build Verification Prompt (agent-browser)

Runs automatically after Phase 6 (build) and Phase 7 (SEO pass). Uses
`agent-browser` to visually inspect the built site, take annotated
screenshots, extract the accessibility tree, and iterate on issues — without
asking the user to verify manually.

---

## Prerequisites

Install once (global):
```bash
npm install -g agent-browser
agent-browser install      # downloads Chrome for Testing
# Linux:
agent-browser install --with-deps
```

No API key, no env var. Runs locally against the dev server.

---

## The Prompt (Claude Code executes this)

```
You are verifying the build end-to-end using agent-browser (already installed
globally). The dev server is running at {{dev_server_url}} (typically
http://localhost:3000).

Do NOT ask the user to look at the site. You verify it yourself, take
screenshots, iterate on issues, and only show the user the final result.

## Phase A — Desktop Verification

1. Open the site at desktop width:
   agent-browser open {{dev_server_url}} --viewport 1920x1080

2. Take a full-page annotated screenshot:
   agent-browser screenshot --full-page --annotate --out screenshots/desktop-initial.png

3. Get the accessibility tree with element refs:
   agent-browser snapshot > snapshots/desktop.json

4. Inspect the snapshot for the expected landmarks:
   - <main> exists
   - <header> with <nav>
   - <footer>
   - One <h1>
   - All CTAs are buttons or <a> elements (not divs)
   - Every <img> has alt text

5. Scroll through the page in 500px increments, taking a screenshot at each
   stop, to verify the scroll-driven hero animation plays correctly:
   agent-browser execute "window.scrollBy(0, 500)"
   agent-browser screenshot --out screenshots/desktop-scroll-{{i}}.png

6. Verify scroll animation frames actually change (compare frames 1, 3, 5).
   If the frames are identical, the scroll animation is broken.

## Phase B — Mobile Verification

1. Open at mobile width:
   agent-browser open {{dev_server_url}} --viewport 375x812 --device-scale 3

2. Full-page screenshot:
   agent-browser screenshot --full-page --out screenshots/mobile-initial.png

3. Verify the video was replaced with the still image on mobile:
   agent-browser get attribute "video" src
   # If this returns a src, mobile is incorrectly loading the video. Fix.

4. Check tap targets:
   agent-browser snapshot --filter "role=button" > snapshots/mobile-buttons.json
   # Parse the JSON: every button's bounding box must be >= 24x24 CSS px

5. Check for horizontal scroll (must be zero):
   agent-browser execute "document.documentElement.scrollWidth > window.innerWidth"
   # Must return false

## Phase C — Interaction Tests

Test every interactive element the survey included:

1. Click the primary CTA:
   agent-browser find role button click --name "Book Now" "Get Started" "Contact"
   agent-browser screenshot --out screenshots/after-cta-click.png
   # Verify a form modal, /contact page, or mailto: opened

2. Test form submission (fill with test data, do NOT actually submit):
   agent-browser find role textbox fill --name "Email" "test@example.com"
   agent-browser find role textbox fill --name "Name" "Test User"
   agent-browser screenshot --out screenshots/form-filled.png

3. Test the navigation menu:
   agent-browser find role link click --name "Services"
   agent-browser screenshot --out screenshots/nav-services.png
   agent-browser execute "window.location.href"
   # Verify URL changed to /services or equivalent

## Phase D — Performance Verification

1. Run Lighthouse via agent-browser's HAR recording or via the lighthouse CLI
   directly against the dev server:
   lighthouse {{dev_server_url}} --only-categories=performance,accessibility,seo,best-practices \
     --output=json --output-path=lighthouse-report.json --chrome-flags="--headless"

2. Parse lighthouse-report.json. Required:
   - Performance >= 90 (target >= 95)
   - Accessibility >= 95
   - SEO >= 95
   - Best Practices >= 95

3. If any score is below target, identify the top 3 fixable issues and fix
   them BEFORE telling the user the build is done.

## Phase E — Visual Regression (if this is a rebuild)

If this is an iteration on a previous build:
1. Compare screenshots/desktop-initial.png against
   screenshots/previous-desktop-initial.png
2. Highlight any visual diffs
3. Report unexpected changes to the user

## Phase F — Report

Print a final verification report:

```
✓ Desktop render: OK
✓ Mobile render: OK
✓ Scroll animation: working (verified 5 frames)
✓ Mobile video suppressed: OK (using still image fallback)
✓ Primary CTA: functional (opens {{modal|page}})
✓ Form submission: functional
✓ Navigation: all links working
✓ Lighthouse: P {{perf}} / A {{acc}} / S {{seo}} / BP {{bp}}
✓ No horizontal scroll on mobile
✓ All tap targets >= 24x24 CSS px
{{any issues found + what was fixed}}

Screenshots saved to: screenshots/
Accessibility snapshots saved to: snapshots/
Lighthouse report saved to: lighthouse-report.json

Build verified. Ready for your review at {{dev_server_url}}.
```

## Fix Loop

For each failure, automatically:
- Scroll animation broken → check ffmpeg frame extraction, verify frame paths
  load in Network tab (`agent-browser get network-requests`)
- Mobile loading video → check media query and picture element sources
- Tap targets too small → bump padding on buttons to min-height: 48px
- Horizontal scroll → find the overflowing element via `agent-browser execute
  "Array.from(document.querySelectorAll('*')).filter(el => el.scrollWidth >
  el.clientWidth).map(el => el.tagName)"` and apply overflow-x fix
- Lighthouse perf < 90 → run the perf audit prompt (see §10 of seo-research-2026.md)

Re-run Phase A–D after each fix until all checks pass.

## Rules

- NEVER ask the user to verify visually until all automated checks pass
- ALWAYS kill the dev server cleanly when done (SIGINT)
- ALWAYS save screenshots to `screenshots/` and snapshots to `snapshots/` for
  the user to review if curious
- Budget: max 5 fix-and-reverify cycles before escalating to user
- If a fix would require changing the design (not just a bug), show the user
  the screenshot + problem + proposed fix before acting
```

---

## Variables

- `{{dev_server_url}}` — from the build phase, usually http://localhost:3000
- `{{i}}` — scroll iteration counter (skill loops 5-10 times)
- `{{perf}}`, `{{acc}}`, `{{seo}}`, `{{bp}}` — Lighthouse category scores

---

## Why agent-browser Specifically

- **Semantic locators** (`find role button`) work across framework changes
  without brittle CSS selectors
- **Reference-based targeting** (`click @e2` from snapshot) is faster than
  generating new locators each call
- **Accessibility tree output** in JSON is perfect for Claude to reason about
- **Network interception** for performance verification
- **Chrome for Testing** ensures reproducible results across environments
- **Rust CLI** = fast, no Node.js daemon overhead, no Playwright install

Alternative tools considered: Playwright MCP (heavier, more moving parts),
Puppeteer scripts (requires custom wrapper), vanilla screenshot tools (no
interaction). agent-browser is the minimum viable verification tool.
