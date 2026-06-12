# 07 — Immediate Tooling & Budget

> Constraint from the founder: solutions must be deployable now, produce the best
> possible result fast, and not cost thousands of euros. This doc turns the
> provider choices in 03 into a cost ladder with an immediate path for each.

## Ground truth on Suno (verified June 2026)

- **Suno still has no official public API.** No developer portal, no self-service
  keys. This has not changed since 2025.
- The founder's (almost-)paid Suno subscription grants **commercial rights to songs
  generated through the Suno app/web UI** while subscribed — that subscription is
  an asset we can use immediately, just not programmatically.
- Third-party Suno wrappers exist (Sunor, TTAPI, GPTProto, AIMLAPI, etc.) at
  roughly **$0.02–0.10 per song**, pay-as-you-go. They are unofficial: acceptable
  stability/ToS risk for a paid quality tier later, not as the foundation.
- **Do not** use cookie/session-based wrappers that log into the founder's own
  Suno account programmatically — ToS violation with a real account-ban risk to
  the exact account whose commercial rights we depend on.

## The music ladder (use in this order)

### Rung 1 — now, ~€0: founder's Suno account, concierge mode

The pipeline automates everything except the click:

```
story → lyrics + style prompt (LLM, automated)
      → "Studio queue" screen shows ready-to-paste lyrics + style string
      → founder pastes into Suno UI, generates, downloads MP3
      → uploads via the existing MP3-upload path (already built in legacy!)
      → artifact attaches to the story, share page works normally
```

- Marginal cost ≈ €0 (subscription already nearly in place), best-in-class quality
  (Suno v5 is still the consumer quality leader), commercial rights clean.
- This is a classic concierge MVP: at validation scale (tens of songs/week) the
  manual step is minutes per day and — bonus — the founder hears every song the
  product makes, which is exactly the quality feedback loop Phase 2 needs.
- Build cost: trivial. The "Studio queue" is one admin screen; the upload path
  already exists in the legacy app and ports easily.

### Rung 2 — automated + cheap: MiniMax Music via fal.ai (official API)

- **MiniMax Music 2.5/2.6**: full songs with vocals, up to 5 min, official
  pay-as-you-go API (via fal.ai and similar), **~$0.035–0.05 per song** flat
  (Pro variant ~$0.21). Quality rated "high" — a tier below Suno on some genres,
  far above "good enough" for an automated free tier.
- This becomes the default automated pipeline when manual volume hurts:
  100 songs ≈ **€4–20**. Effectively noise in the budget.
- fal.ai doubles as our aggregator for image/video/TTS models — one account, one
  billing, pay-per-use, no subscription. Fewer vendors than the 03 baseline; 03 is
  amended accordingly.

### Rung 3 — scale/premium: Suno via third-party wrapper, or ElevenLabs Music

- When data shows song quality drives conversion: add a "studio quality" tier via
  a reputable Suno wrapper ($0.05–0.10/song; pick one with refunds-on-failure and
  webhooks; treat as swappable — the provider interface in 03 makes this a
  config change).
- ElevenLabs Music (~$0.15/min native) only if license-cleanliness ever becomes a
  commercial requirement (B2B/agency use); it is the expensive, legally bulletproof
  option, not the default.

## The same ladder applied to video and voice

| Artifact | Rung 1 (now, ~€0) | Rung 2 (automated, cheap) | Rung 3 (scale) |
|---|---|---|---|
| Memory Film visuals | founder's Higgsfield subscription, concierge via the same Studio queue | image-gen cover + Ken Burns motion assembled with ffmpeg (cents per film) | full video models via fal.ai/Higgsfield API (€0.5–3 per 15–30s film — the costliest artifact; gate behind credits from day one) |
| Voiceover | user's own recorded voice IS the voiceover (free, and more intimate than TTS) | ElevenLabs free/starter tier (TTS is cheap at low volume) | ElevenLabs scale plan / voice cloning |
| Cover images | — | fal.ai image models, ~$0.01–0.04 per image | same |

The Rung-1 video insight matters: the user already *spoke* the story. The first
Memory Film format uses their real voice over generated/Ken-Burns visuals — cheaper
AND emotionally stronger than synthetic narration.

## Always-cheap core (no ladder needed)

| Item | Cost reality |
|---|---|
| Transcription (gpt-4o-mini-transcribe class) | ~$0.003/min → 2-min entry ≈ **$0.006** |
| Story distillation + title + signature (LLM) | ~$0.01–0.03 per entry |
| Infra (Cloud Run, Firestore, Hosting, Cloud Tasks) | free tiers cover validation scale; expect **€0–20/month** |
| Sentry, GitHub Actions | free tiers |

**Full loop cost per daily active user: under €0.05/day** excluding films.
A validation cohort of 50 active users runs **well under €100/month** all-in,
with songs on Rung 1 costing nothing beyond the existing Suno subscription.

## Budget guardrails (binding for implementation)

1. Per-user daily generation budget enforced at the API from the first release
   (already specified in 03); films additionally gated by explicit credits.
2. Every provider call logs estimated cost to `generation_events` — the monthly
   spend is a dashboard query, never a surprise invoice.
3. Hard monthly spend alarm (provider dashboards + a daily aggregate check) set at
   €100 during validation; raising it is a deliberate founder decision.
4. No annual contracts, no subscriptions beyond what the founder already has
   (Suno, possibly Higgsfield); everything else pay-as-you-go.

## Impact on the roadmap (05)

- **P2.1 Song pipeline** is re-scoped: build the lyrics+style generation, the
  Studio queue (Rung 1), and the provider interface with a MiniMax implementation
  (Rung 2) behind a flag. Suno-wrapper integration moves to the Phase 5 backlog
  with a metric hypothesis ("studio tier lifts share rate by X").
- **P3.2 Memory Film** starts at Rung 2 (Ken Burns + real voice) by default;
  full video generation is the premium variant, not the baseline.
- Secrets needed *now* shrink to: LLM key, `FAL_KEY`, `SENTRY_DSN`. ElevenLabs and
  Higgsfield keys move to "when their rung activates."
