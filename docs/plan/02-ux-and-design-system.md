# 02 — UX & Design System

> Bar: the visual craft of the best AI-era creative software. Two registers: a
> spectacular *outside* (landing, share pages, Wrapped) and an intimate *inside*
> (the daily loop). Confusing these two registers is the #1 design risk.

## Design language: "Night Studio"

The reference the founder gave (dark gaming site, neon, parallax, video-backed hero)
is the correct energy for the **outside** surfaces. The **inside** borrows its
materials but turns the volume down.

### Foundations

- **Mode:** dark-first. Deep warm charcoal (`#0E0C12` family), *not* pure black —
  this is a night-time, end-of-day product. Light mode ships later, not at launch.
- **Accent:** keep the existing brand purple lineage (`#8639E8`) but evolve it into a
  **dusk gradient** (violet → ember orange) used sparingly: progress moments, the
  reveal animation, CTAs. Never as large background fills inside the app.
- **Typography:** an editorial serif for story prose (the artifact must look like
  literature, not like chat output) + a clean grotesque for UI. Two families, ever.
- **Texture & depth:** subtle film grain on artifact surfaces, soft glow on active
  elements, glassmorphism only on overlays. Parallax and bold motion reserved for
  outside surfaces.
- **Motion:** every state change animated, 150–300ms, spring curves. The two
  signature animations that must be *perfect*: (1) the waveform while speaking,
  (2) the story reveal (title fades in, prose settles line by line).
- **Sound:** the product has a voice (it makes songs and films) — tasteful UI sound
  on reveal and on artifact completion, off by default in silent mode.

### Outside surfaces (spectacle register)

- **Landing page:** full-bleed background film (generated with our own pipeline —
  the product demos itself), dark + dusk gradient, parallax scroll through the loop:
  *speak → reveal → song → film → gift*. One CTA: "Tell your first story — no
  signup." A live demo widget records 30s and produces a real story card in-page.
  This is the "mega video taga" page the founder described, executed with intent.
- **Share pages (`/s/...`):** each artifact type has a cinematic template (see 04).
- **Wrapped:** full-screen story-format sequence, swipe-through, every card
  screenshot-worthy.

### Inside surfaces (intimacy register)

Calm, focused, generous whitespace (well — darkspace). No feed on the home screen.

## Information architecture

```
Home ("Tonight")     — today's question + speak button + latest artifact
Chronicle            — your vault: timeline of stories/artifacts, search, "on this day"
Create               — photo spark, gift flow, free-form entry, format browser ("more")
Resonance            — anonymous feed, "me too" interactions
You                  — profile, privacy vault controls, settings, Wrapped archive
```

Five tabs maximum. The legacy app's `Discover / Share / Stories / Inner Space`
maps roughly to `Resonance / Home / Chronicle / (Wrapped absorbs Inner Space)`.
Inner Space's 3D visualization is parked: high build cost, unclear retention value —
revisit as a Wrapped easter egg.

## Key screens (build order priority)

1. **Speak screen** — full-screen, one giant record affordance, live waveform,
   elapsed time, gentle "keep going" micro-prompts if the user pauses early.
   This screen is the product; over-invest here.
2. **Reveal / Story card** — editorial layout, serif prose, cover image, emotional
   signature as a small badge, the three actions (Keep / Share / Gift) + the single
   format recommendation as a glowing suggestion chip.
3. **Home ("Tonight")** — today's question in large type, speak button,
   yesterday's artifact peeking from the bottom.
4. **Artifact player** — unified player for songs and films: vertical, full-screen,
   custom controls, lyrics/captions synced.
5. **Chronicle** — timeline grouped by month, dense but beautiful; each entry is a
   small card with title + emotional signature color.
6. **Gift flow** — recipient name → relationship → memory prompt → speak →
   format choice (song/fairytale/film) → preview → send link. Must work start to
   finish in under 3 minutes.
7. **Share page templates** — see 04.
8. **Resonance feed** — last; the loop must work before discovery matters.

## Mobile-first rules

- Everything designed at 390×844 first; desktop is an adaptation (centered column,
  ambient background), not a separate design.
- Thumb-zone: primary actions in the bottom 40% of the screen.
- PWA installability: custom install prompt after the first kept artifact ("keep
  your chronicle on your home screen"), not on first visit.
- Capacitor shell (Phase B) adds: push, native share sheet, haptics on reveal,
  high-quality mic API. The web codebase must abstract these behind a
  capabilities layer from day one (see 03).

## Accessibility & quality bar

- WCAG AA contrast even in dark mode (the dusk gradient needs checked text colors).
- All voice features have full text equivalents (type instead of speak; read
  instead of listen).
- Reduced-motion media query honored — the reveal degrades to a crossfade.
- Performance budget: LCP < 2s on mid-range Android over 4G; JS bundle < 250KB
  gzipped at launch (achievable: the legacy app shipped React via CDN + in-browser
  Babel, so the bar we inherit is *very* low).

## Anti-patterns (explicitly banned)

- A grid of 19 format choices anywhere in the primary flow.
- Lock icons / restriction messaging on viewed content (legacy already removed these).
- Guilt-based streak UI ("you broke your streak 💔").
- Infinite-scroll as the home surface.
- Generic AI-product aesthetics: blue/teal gradients on white, sparkles-emoji-everything,
  template hero sections. The founder's reference image is the antidote — distinctive
  darkness, real art direction.
