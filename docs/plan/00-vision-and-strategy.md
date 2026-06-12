# 00 — Vision & Strategy

> Part of the Sentimental v2 master plan. Read this first; every other doc derives from it.

## One-sentence vision

**Talk for two minutes — get back something beautiful enough to keep, share, or gift.**

Sentimental turns spoken personal moments into crafted media artifacts (stories, songs,
short films) using a long-term personal context engine, with private reflection as the
core and public artifacts as the output.

## What we are NOT building

These exclusions matter as much as the vision:

- **Not a therapy app.** Psychology is built into the mechanics (see 01), never into the
  marketing. "Therapy-coded" products repel the sharing audience and create liability.
- **Not a social network.** There is no follower graph, no engagement feed as the home
  screen. The feed (anonymous resonance) is a discovery surface, not the center.
- **Not a general AI chatbot.** The chat exists only to extract a story. The moment a
  story can be distilled, we move the user forward.
- **Not 19 formats.** v2 launches with **3 hero formats** (Story, Song, Memory Film) and
  earns the right to add more.

## Target audience decision

**Question raised: should this be Gen Z focused?**

**Decision: wedge at 18–30, but design the emotional jobs to be ageless.**

Reasoning:

- The *sharing engine* of this product is 18–30: they produce the public artifacts,
  they live in Reels/TikTok where the artifacts circulate, and "main character energy"
  / personal-lore aesthetics are native to them.
- The *paying and gifting* audience skews older: "make a song from a memory for mom's
  birthday" is bought by 25–45 year olds. Gifting is our strongest acquisition loop
  (see 04), and gift recipients of any age become users.
- Therefore: **Gen Z–fluent in tone and craft, never Gen Z–exclusive in mechanics.**
  Sincere, not ironic. Cinematic, not corporate. No slang in product copy that will
  age badly.

Launch wedge persona: **"the chronicler"** — 18–30, journals sporadically, posts
story-driven content, has strong feelings about their personal lore, gives
thoughtful gifts. They are ~5–10% of the cohort but produce ~90% of shared artifacts.

## App vs. web decision

**Question raised: do we need a native app? Webview copy first for testing?**

**Decision: PWA-first → Capacitor shell → native only if a hard capability forces it.**

This is exactly the "webview copy to test before committing to an app" instinct, done
the standard way:

1. **Phase A — Installable PWA.** One React codebase, mobile-first, served from the web.
   Full product loop works in the browser. This is the test vehicle: shareable links,
   instant iteration, no app-store review cycle.
2. **Phase B — Capacitor wrapper.** The *same* web build shipped inside a native shell
   to the App Store / Play Store. Capacitor gives us the native pieces we actually
   need — push notifications, high-quality microphone access, share sheet, haptics —
   without a second codebase.
3. **Phase C — go native per-surface only if needed** (e.g., if audio recording
   latency or background recording in the webview proves inadequate). Decide on
   evidence, not in advance.

Why not native-first: the product's risk is *product-market fit*, not rendering
performance. Every week spent on Swift/Kotlin before the loop is proven is waste.
Why not web-only forever: daily-ritual retention (see 01) depends on push
notifications and home-screen presence, which need the native shell on iOS.

## Positioning & tone

- Category in the user's head: **"the app that makes my life into art."**
- Emotional register: warm, cinematic, a little magical. The craft level of the best
  AI-video creators (the "insane dark gaming site" reference) is the bar for our
  *launch surfaces* (landing page, share pages, Wrapped) — the product interior is
  calmer, because its job is intimacy, not spectacle.
- Privacy is a feature with a face: "Your reflections are yours. Only what you choose
  to publish leaves the vault." This must be visibly true in the UI (see 02).

## The honest answer to "kas suudame?" (can we do it?)

What is fully in our control and we will execute at world-class level:

- Craft quality of the loop and artifacts (UX, design, generation pipelines).
- Smart, non-overkill technical choices (see 03).
- Building virality *mechanics* into every artifact (see 04).

What is **not** guaranteed by craft alone: actual viral growth. That requires
iteration with real users and luck of timing. The plan therefore builds measurement
into the loop from day one (activation %, share rate, gift conversion) so each
release teaches us something. We control the inputs; we instrument the outputs.

## Success metrics (north stars)

| Metric | Definition | Why it matters |
|---|---|---|
| **Time-to-magic** | seconds from first open → first finished artifact | activation; target < 90s |
| **Keep rate** | % of generated artifacts saved/favorited | artifact quality proxy |
| **Share rate** | % of artifacts shared externally | virality input |
| **K-factor of share pages** | signups per shared artifact view | virality output |
| **Weekly ritual retention** | % of users with ≥3 voice entries/week at week 4 | core habit |

## Relationship to existing assets

- `app.py` + engines: the **personal context engine** concept (`personal_context_mapper.py`,
  `prompts_engine.py`) survives as the moat; the monolith and the dual-bundle frontend
  do not (see 03 for the migration strategy).
- `MentalOS/`: parked. Its "inner work" direction is absorbed as the private layer of
  Sentimental v2 rather than a separate app. Revisit only after the core loop ships.
- `/s/<id>` share routes + Firebase Hosting rewrites: the seed of the growth engine,
  rebuilt properly in 04.
