# 01 — Core Loop & Product Spec

> The product is one loop executed beautifully, plus a weekly payoff and a gifting path.

## The core loop (the "2-minute thing")

```
┌────────────────────────────────────────────────────────────────────┐
│ 1. PROMPT   Daily question arrives (push/widget) or user opens app │
│ 2. SPEAK    User talks 1–3 min (voice-first; typing fallback)      │
│ 3. DISTILL  AI transcribes, extracts the story, names the moment   │
│ 4. REVEAL   Story presented as a crafted card < 30s later          │
│ 5. ELEVATE  App recommends ONE format: "this wants to be a song"   │
│ 6. KEEP / SHARE / GIFT                                             │
└────────────────────────────────────────────────────────────────────┘
```

Hard requirements per step:

1. **Prompt** — one question per day, selected by the context engine from the user's
   history (people they mention, themes, unfinished threads). Never generic
   ("how was your day?") after day 3; always specific ("you mentioned your brother
   on Tuesday — what's the story there?"). Question quality is a ranked, versioned
   prompt asset (see 06).
2. **Speak** — recording UI is full-screen, calm, with live waveform. Max friction
   allowed: one tap to start. Auto-stop on long silence with confirmation. Typing is
   available but visually secondary.
3. **Distill** — pipeline: speech-to-text → story extraction → title + emotional
   signature (e.g. `bittersweet / family / pride`). The extraction prompt's prime
   directive: **no invented details, ever** (this rule already exists in the legacy
   prompts — keep it; it's why outputs feel authentic instead of AI-sloppy).
4. **Reveal** — the story card is typographically beautiful (see 02). The reveal is
   the dopamine moment: subtle animation, the title appears first, then the prose.
5. **Elevate** — the app picks **one** recommended format based on emotional
   signature. Other formats are reachable via "more" but never presented as a grid
   of 19. Recommendation rules start hand-written, become learned later.
6. **Keep / Share / Gift** — every artifact has exactly these three actions.
   Keep = private vault. Share = public page (see 04). Gift = send to a person.

## Hero formats at launch (3, not 19)

| Format | Output | Pipeline | Why it's a hero |
|---|---|---|---|
| **Story** | Crafted prose card + cover image | LLM + image model | the base unit; fast, always works |
| **Song** | Playable 1–2 min song with lyrics | LLM (lyrics) → Suno v5 | most giftable + most shareable artifact |
| **Memory Film** | 15–30s vertical video: voiceover + visuals | LLM (script) → ElevenLabs (VO) → Higgsfield (visuals) → assembly | the Reels/TikTok-native artifact |

Retired from the launch surface (still in codebase history, may return as "more"):
X/LinkedIn/Facebook posts, newsletter, presentation, article, blog post, letter,
reflection/insights/growth-summary (these merge into the Wrapped, see below), book
chapter, fairytale (returns later as a Gift variant — it tested well emotionally).

## The weekly payoff: "Your Episode"

Every week, for users with ≥2 entries, the app auto-generates a **weekly episode**:
a 30–60s recap film (or audio episode) of their week's stories, with a title like a
TV episode ("S01E07: The Week You Stopped Waiting"). Delivered via push, opens to a
full-screen player.

- Zero user effort — this is the "story comes to you" mechanic.
- Monthly and yearly versions become **Wrapped** (see 04).
- Episodes are private by default; sharing one is a single tap.

## Psychology — built into mechanics, invisible in marketing

**Question raised: how does psychology come in, or does it not matter?**
It matters enormously, but as *mechanism design*, not as content:

| Psychological principle | Where it lives in the product |
|---|---|
| Expressive writing/speaking (Pennebaker) | the daily voice entry IS the intervention; zero-friction speaking lowers the barrier to it |
| Narrative identity & redemptive reframing (McAdams) | story distillation is instructed to find agency and growth in the raw material *without inventing facts*; the "Elevate" step offers reframes (e.g. fairytale = maximal distance) |
| Self-distancing | hearing your story in third person / as a song creates therapeutic distance automatically |
| Peak-end rule, memory dividends | weekly Episode + Wrapped resurface peaks; "on this day" resurfacing of old artifacts |
| Variable reward | the reveal moment (which title? which format recommendation?) — anchored to creation, never to scrolling |
| Self-disclosure reciprocity | anonymous resonance feed: reading others' stories prompts "ka mina / me too" — connection without exposure |
| Habit formation | daily prompt + streak shown as a "chronicle" (chapters filled), not a guilt-streak counter |

**Ethical guardrails (non-negotiable, encoded in prompts and UI):**

- Private-by-default for everything; publishing is always an explicit act.
- No invented biographical details in any generated artifact.
- No engagement-bait push notifications; pushes deliver value (your episode is ready,
  your daily question), never FOMO.
- Crisis language detection in entries routes to a gentle resources card, not to
  content generation.

## Entry points beyond the daily prompt

- **Gift flow** (see 04) — entered from a friend's birthday, no account needed to
  *receive* a gift.
- **Resonance feed** — anonymous stories; tapping "me too" offers "tell your
  version" → drops into the Speak step.
- **Photo spark** — user picks an old photo; app asks "tell me about this" →
  Speak step → Memory Film uses the actual photo as the visual seed
  (image-to-video). Emotionally the strongest single feature in the plan.

## What success looks like per session

First session (cold start): from app open to a finished Story artifact in under
90 seconds — the daily question is pre-loaded for first-timers with a universal
high-yield prompt ("tell me about a moment from this year you keep coming back to").
Returning session: open push → speak 2 min → artifact → done. Total under 4 minutes.
The product respects time; depth accumulates across sessions via the context engine.
