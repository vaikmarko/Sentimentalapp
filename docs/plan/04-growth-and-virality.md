# 04 — Growth & Virality

> Doctrine: the viral unit is the artifact, not the app. Every artifact must be
> shareable-grade even if Sentimental didn't exist; the app rides along on it.

## The three growth loops, ranked

### Loop 1 — Gifting (highest conviction)

```
User makes a gift (song/fairytale/film about a shared memory)
  → recipient opens a cinematic gift page (no account needed to receive)
  → emotional peak moment ("someone made this FOR me")
  → CTA at the peak: "Make one for someone you love"
  → recipient becomes creator → loop repeats
```

Why ranked first: the recipient experiences the product's full magic at maximum
emotional receptivity, the artifact is inherently personal (can't be ignored like
an ad), and occasions are calendar-driven (birthdays, Mother's/Father's day,
anniversaries, graduations) giving us predictable campaign moments. Seasonal
spikes are plannable: a "make mom cry" Mother's Day campaign is the launch wedge.

Mechanics to build:
- Gift pages: artifact + "made for you by {name}" + unwrap animation (a held-breath
  moment before reveal — this is the single highest-leverage animation in the product).
- Receiving requires zero signup; *replying* with a gift back is the conversion point.
- Occasion reminders (opt-in contact dates) re-trigger the loop.

### Loop 2 — Share pages as landing pages

Every shared artifact (`/s/{id}/{format}`) is a full marketing surface:

- Cinematic template per format: film plays full-bleed; song gets an animated
  lyric-synced player; story gets the editorial card.
- Proper OG tags → rich unfurls in iMessage/WhatsApp/IG DMs (where personal
  artifacts actually get shared — DMs first, feeds second).
- The hook at the end of every artifact: **"Milline oleks sinu lugu?" / "What's
  your story?"** + a try-it-now widget (record 30s in-page, get a story, then
  signup to keep it). The artifact demos the product; the page converts.
- Watermark: subtle, elegant `sentimental` mark on films/song covers — brand
  distribution on every share, removable on paid tier later.

Instrumentation: every share page logs view → widget-try → signup funnel per
artifact type. This funnel IS our growth dashboard.

### Loop 3 — Wrapped (seasonal spike engine)

Monthly "Your Month" and yearly "Your Year in Stories": swipe-through sequence of
the user's themes, peaks, people-most-mentioned, plus one auto-generated montage
film. Spotify Wrapped works because it's **identity expression with scarcity**
(once a year, everyone at once). We replicate the December moment, and monthly
versions keep the muscle warm.

Each Wrapped card is individually exportable as a 9:16 image/clip — built for
IG Stories, where one screenshot carries the brand to the sharer's entire graph.

## Supporting mechanics

- **Resonance feed** (retention more than acquisition): anonymous stories, "me too"
  taps, "tell your version" → speak flow. Anonymity is what makes intimate content
  publishable at all; identity-attached confession feeds die of stage fright.
- **Photo spark + Memory Film**: "I animated my grandmother's old photo and made
  her tell the story behind it" is organic-press / TikTok-virality material. This
  feature is its own marketing.
- **Duet stories** (post-launch): two people each record their side of a shared
  memory; the AI weaves both perspectives into one story/film. Built-in tagging =
  built-in distribution. Data model supports it from day one (`participants[]`).
- **Creator seeding**: launch playbook = 20–50 mid-size storytelling/journaling
  creators get early access + a custom Wrapped; their share pages carry try-widgets.
  (The legacy early-access-code system — `UNICORN`, `SENTI2025` — becomes the
  scarcity mechanism: invite codes embedded in shared artifacts.)

## Monetization sketch (designed now, charged later)

Free tier: daily story loop, N song/film credits per month, watermarked shares.
Paid ("Studio"): unlimited/more credits, watermark-free, voice cloning for
narration, priority generation, yearly Wrapped film in full quality, gift bundles.
Gifting is also a one-off purchase path for non-subscribers (buy a single gift
song) — important because gift buyers are often not habitual users.

Costs are metered per generation from day one (see 03), so pricing decisions are
data-driven, not guessed.

## What we measure from day one

| Funnel | Metrics |
|---|---|
| Activation | open → first artifact (time, completion %) |
| Habit | entries/week, week-4 retention, episode open rate |
| Artifact quality | keep rate, replay rate, format acceptance rate (did user take the recommendation?) |
| Sharing | share rate per format, share-page views, view → try-widget %, try → signup % |
| Gifting | gifts sent, gift open rate, recipient → creator conversion |
| Cost | cost per artifact, cost per activated user |

## Anti-goals

- No follower counts, no public like-counts on identified content.
- No dark-pattern invites (no contact-book spam, no "X friends are waiting").
- No engagement-optimized feed ranking; resonance feed stays chronological/thematic.
  Growth comes from artifact quality and emotional peaks, or it doesn't come at all —
  that constraint is the brand.
