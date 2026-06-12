# 02 — UX & Design System

> Craft bar: the best AI-era creative software — the founder's "insane gaming site"
> reference sets the *level* of polish, not the aesthetic. The design language below
> is derived from our own context: a voice-first, end-of-day product that turns
> spoken memories into art, used by the "chronicler" persona (00), with an intimate
> inside and a cinematic outside. Confusing those two registers is the #1 design risk.

## Design concept: "Night Studio"

### The metaphor

A small private studio after dark. You step in from the noise of the day, a lamp
is on, you speak — and the studio develops what you said into something made:
a printed page, a pressed record, a short film. The metaphor merges three rooms,
and each maps to a product surface:

| Room | What happens there | Product surface |
|---|---|---|
| **The Booth** | you speak into warm quiet | Speak screen |
| **The Darkroom** | your words develop into an artifact | Reveal, "in the studio" states |
| **The Library** | your finished works live on shelves | Chronicle, artifact player |
| **The Lit Window** | how the studio looks from the street | landing page, share pages, Wrapped |

This metaphor was chosen against alternatives (constellation/space — too cold and
already used by the legacy "Inner Space"; scrapbook/journal — too crafty, skews
old; neon/cyber — spectacular but emotionally wrong for confession) because it
natively explains the product's two registers: warm intimacy inside, and the
glow seen from outside that makes a passerby want to come in.

### Light logic (the system's core rule)

In this world, **light = meaning**. The UI chrome stays dark and quiet; light is
reserved for three things only: the act of creation (the record button and live
waveform), the finished artifact (cards and players carry the glow), and the
invitation (CTAs). Decorative light is banned. This one rule keeps every screen
composed: if something glows, it matters.

### Color system

- **Night** — base surfaces: deep warm charcoal family (`#0E0C12` → `#1A1622`
  elevations). Never pure black; the room has warmth.
- **Lamplight** — warm amber (`#E8A849` family): the *human* color. Record button,
  live waveform, gift unwrap glow, primary CTAs. The color of the act of speaking.
- **Dusk** — violet (`#8639E8`, inherited from the existing brand): the *studio's*
  color — AI-made things in progress: distilling states, format recommendation
  chip, the reveal shimmer. Human warmth = amber, machine craft = violet; their
  meeting (the dusk-to-ember gradient) marks finished artifacts.
- **Signature Spectrum** — 8 muted tones mapped to emotional signatures
  (e.g. joy = pale gold, bittersweet = rose, grief = slate blue, pride = ember,
  calm = sage…). Used as the accent edge of story cards, chronicle dots, and
  Wrapped data visuals. The Chronicle becomes quietly beautiful at a glance:
  your month is visible as a strip of colors before you read a word.
- Text: warm off-white (`#F2EDE4`) on Night; AA-checked tints per Spectrum tone.

### Typography

- **Artifacts speak serif.** A warm, slightly characterful editorial serif
  (Fraunces, variable optical size) for story prose, titles, lyrics, gift pages —
  generated text must look like literature, never like chat output.
- **The studio speaks grotesque.** Inter for UI chrome, labels, settings —
  quiet, invisible, never competing with the artifact.
- Two families, ever. Display sizes are generous: tonight's question is set
  large enough to feel addressed *to you* (32–40px on mobile).

### Texture, materiality, motion

- **Grain:** fine film grain on artifact surfaces only (cards, players, share
  pages) — made things have material; UI chrome stays clean flat.
- **Motion identity — "breathe and develop":** at rest, lit elements breathe
  (subtle 4s glow cycles). Transitions *develop* like a darkroom print: soft
  blur + grain resolving into sharpness, 150–300ms springs. The two signature
  animations that must be perfect: (1) the live waveform — a thread of amber
  light that thickens and flares with the voice, more level-meter than
  oscilloscope; (2) the reveal — title develops first, prose settles line by
  line like ink drying.
- **Sound identity:** the product makes audio, so it may speak — sparingly:
  a soft tape-start click on record, near-silent room tone while recording
  (presence, not noise), one low warm chord on reveal. Off in silent mode.

### Voice & tone (copy)

The studio is a quiet collaborator: second person, lowercase calm, no
exclamation marks, no AI-assistant chirpiness, no therapy-speak. It asks good
questions and otherwise stays out of the way. Estonian and English copy are
written natively, never machine-translated tone.

## Per-surface art direction

### Inside (intimacy register)

- **Tonight (home):** a near-dark room. Today's question in large serif under a
  soft lamplight vignette; the record button is the only strong light source.
  Yesterday's artifact peeks from the bottom shelf. Nothing else.
- **Speak (the Booth):** full-screen, chrome fades away after recording starts;
  amber waveform thread, elapsed time in small type. Pausing early triggers a
  gentle micro-prompt in dusk violet ("what happened next?").
- **Reveal (the Darkroom):** the develop animation; emotional signature appears
  as a small Spectrum-colored edge; three actions (Keep / Share / Gift) plus one
  violet recommendation chip ("this wants to be a song").
- **Chronicle (the Library):** month-grouped timeline; each entry a compact card
  with title + Spectrum edge; the month header shows the color strip summary;
  "on this day" resurfacing slot at top.

### Outside (spectacle register)

- **Landing page — "The Lit Window."** Background film, generated with our own
  pipeline (the product demos itself): a quiet street at night, one warm lit
  window; the camera drifts slowly closer; through the glass, glimpses of things
  being made — a record spinning, photographs developing, a waveform glowing on
  a desk. Scrolling walks you to the door and inside, through the loop:
  *speak → develop → song → film → gift*, each step a full-viewport scene with
  real product UI composited in. One CTA above the fold: "Tell your first
  story — no signup," opening the live 30-second demo widget. Parallax and
  cinematic motion live *here*, not inside the app.
- **Share pages (`/s/...`):** song = a **record sleeve** — cover art, a spinning
  center label, lyric lines lighting up amber as they're sung; film = a
  **projection** — full-bleed video with a faint beam-and-grain treatment;
  story = a **printed page** — editorial serif card in a lamplight vignette.
  Every page ends with the hook: "What would your story be?" + try-widget (04).
- **Gift page:** a parcel in lamplight; the unwrap interaction lets light spill
  out before the artifact appears — the held-breath moment (04) is built from
  the light logic: the gift literally brightens the room.
- **Wrapped:** a **contact sheet** of your month — film frames lighting up one
  by one in Spectrum colors, then cutting into the montage. Every card exports
  as a 9:16 frame composed for screenshots.

## Information architecture

```
Tonight     — today's question + speak button + latest artifact
Chronicle   — your vault: timeline, search, "on this day"
Create      — photo spark, gift flow, free-form entry, format browser ("more")
Resonance   — anonymous feed, "me too" interactions
You         — profile, privacy vault controls, settings, Wrapped archive
```

Five tabs maximum. The legacy app's `Discover / Share / Stories / Inner Space`
maps roughly to `Resonance / Tonight / Chronicle / (Wrapped absorbs Inner Space)`.
Inner Space's 3D visualization is parked: high build cost, unclear retention value —
revisit as a Wrapped easter egg.

## Key screens (build order priority)

1. **Speak screen** — this screen is the product; over-invest here (art direction
   above).
2. **Reveal / Story card** — the develop animation and editorial layout.
3. **Tonight (home)** — question + record button + yesterday's artifact.
4. **Artifact player** — unified for songs and films: vertical, full-screen,
   custom controls, lyrics/captions synced, record-sleeve / projection treatments.
5. **Chronicle** — timeline with Spectrum edges and month color strips.
6. **Gift flow** — recipient → relationship → memory prompt → speak → format
   choice (song/fairytale/film) → preview → send link. Under 3 minutes start to
   finish.
7. **Share page templates** — per art direction above (see 04 for funnel).
8. **Resonance feed** — last; the loop must work before discovery matters.

## Mobile-first rules

- Everything designed at 390×844 first; desktop is an adaptation (centered column,
  ambient room darkness around it), not a separate design.
- Thumb-zone: primary actions in the bottom 40% of the screen.
- PWA installability: custom install prompt after the first kept artifact ("keep
  your chronicle on your home screen"), not on first visit.
- Capacitor shell (Phase B) adds: push, native share sheet, haptics on reveal,
  high-quality mic API. The web codebase must abstract these behind a
  capabilities layer from day one (see 03).

## Accessibility & quality bar

- WCAG AA contrast even in dark mode (Lamplight/Dusk on Night and all Spectrum
  tints ship with checked text pairings in the token set).
- All voice features have full text equivalents (type instead of speak; read
  instead of listen).
- Reduced-motion honored — develop animations degrade to crossfades; breathing
  glow becomes static.
- Performance budget: LCP < 2s on mid-range Android over 4G; JS bundle < 250KB
  gzipped at launch (achievable: the legacy app shipped React via CDN + in-browser
  Babel, so the bar we inherit is *very* low). Grain implemented as a tiled
  texture/CSS, never a video layer inside the app.

## Anti-patterns (explicitly banned)

- A grid of 19 format choices anywhere in the primary flow.
- Decorative glow — light that doesn't mean creation, artifact, or invitation.
- Neon/cyber aesthetics inside the product; parallax inside the app.
- Lock icons / restriction messaging on viewed content (legacy already removed these).
- Guilt-based streak UI ("you broke your streak 💔").
- Infinite-scroll as the home surface.
- Generic AI-product aesthetics: blue/teal gradients on white,
  sparkles-emoji-everything, template hero sections, chat bubbles for story text.
