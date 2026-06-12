# 06 — Agent Prompts & Prompt Engineering Process

> Two kinds of prompts live here: (A) prompts for development agents that build the
> product, and (B) the product's own generation prompts (the creative engine).
> Both are treated as versioned, reviewed assets — not throwaway strings.

## A. Development-agent prompts (one per workstream)

Usage: paste into a fresh cloud agent run, one workstream per agent/branch.
Every prompt below implicitly begins with this **shared preamble**:

```
You are building Sentimental v2. Before writing any code, read /docs/plan/00
through /docs/plan/05 in full — they contain binding decisions on stack, design
language, IA, and acceptance criteria. Do not re-litigate decided choices; if you
hit a genuine blocker with a decision, document it in your PR description instead
of silently deviating. Legacy code under /legacy (or the repo root, pre-migration)
is read-only reference. Work on a feature branch, commit in logical units, open a
draft PR. Quality bar: this product competes on craft; no placeholder UI, no
TODO-littered code, no unstyled states.
```

### F0.1 — Web skeleton

```
Task: scaffold /web per docs/plan/03 repo layout.
- Vite + React 18 + TypeScript strict + Tailwind. PWA manifest + service worker
  (vite-plugin-pwa). Firebase Auth (Google + email link), auth-gated app shell.
- Implement the design tokens from docs/plan/02 as Tailwind theme: Night Studio
  system — Night base (#0E0C12 → #1A1622 elevations), Lamplight amber (#E8A849
  family), Dusk violet (#8639E8), the 8-tone Signature Spectrum with AA-checked
  text pairings, Fraunces (variable, optical size) for artifact prose + Inter for
  UI, spacing/radius/motion tokens (150–300ms springs, 4s breathe cycle, the
  "develop" transition primitive: blur+grain → sharp).
- App shell: 5 tabs (Tonight, Chronicle, Create, Resonance, You) as routes with
  empty states that already look intentional (not "coming soon" text).
- /src/capabilities: define TypeScript interfaces for Mic, Push, ShareSheet,
  Haptics; implement web versions (MediaRecorder, Web Push stub, navigator.share,
  vibration). Capacitor implementations come later — only the interfaces must be
  shaped for it now.
- Mobile-first 390×844; desktop = centered column with ambient background.
- Deliverables: running app, Vitest setup with example tests, README for /web.
Acceptance: lighthouse PWA installable; bundle < 250KB gz; auth roundtrip works.
```

### F0.2 — API skeleton

```
Task: scaffold /api per docs/plan/03.
- FastAPI, Python 3.12, Pydantic v2 models for all request/response bodies.
- Middleware: Firebase ID-token verification → request.user; structured logging;
  Sentry init from env.
- Clients: Firestore, Cloud Storage (signed upload/download URLs), Cloud Tasks
  enqueue helper targeting /internal/tasks/* worker routes (OIDC-authenticated).
- Implement the pipeline-run primitive: Firestore doc {id, type, user_id, steps:
  [{name, status, provider_job_id?, output_ref?, error?, cost_estimate?}],
  created/updated}. One demo pipeline ("echo") that round-trips a Cloud Task.
- /providers: stub modules (llm, transcribe, suno, higgsfield, elevenlabs) with a
  common interface: submit(args) -> job, check(job) -> status, plus a fake mode
  switched by env for tests.
- Dockerfile + Cloud Run deploy config; /healthz, /version.
- Deliverables: pytest suite (fake providers), README for /api.
Acceptance: demo pipeline completes through real Cloud Tasks in the test project.
```

### F0.3 — CI/CD

```
Task: GitHub Actions per docs/plan/03+05.
- PR pipeline: web (typecheck, eslint, vitest, build, bundle-size budget gate) +
  api (ruff, mypy, pytest). Block merge on failure.
- Main pipeline: deploy api → Cloud Run, web → Firebase Hosting; inject version.
- Preview: per-PR Firebase Hosting preview channel for /web.
Keep it boring and fast (<5 min PR pipeline). Document required repo secrets.
```

### P1.1 — Speak screen

```
Task: the recording experience per docs/plan/02 ("over-invest here").
- Full-screen route from Tonight tab. One large record affordance, live waveform
  from mic levels (Canvas/WebAudio, 60fps, degrades gracefully), elapsed time,
  pause/resume, auto-stop after 8s silence with gentle confirmation.
- Micro-prompts if user stops < 30s in ("what happened next?") — copy provided in
  the same PR for review, max 6 variants.
- Typing fallback: visually secondary "write instead" affordance.
- Upload: chunked to signed Storage URL with retry; offline-tolerant (queue and
  send when back online); then POST /entries to start the distill pipeline.
- Reduced-motion compliant; AA contrast; works in iOS Safari standalone PWA
  (test MediaRecorder mimeType fallbacks: audio/mp4 vs webm).
Acceptance: founder can record a 2-min entry on a phone over flaky 4G and it
arrives; the screen feels calm, not like a voice memo utility.
```

### P1.2 — Distill pipeline

```
Task: voice → story, per docs/plan/01 step 3 and docs/plan/03 pipeline rules.
- Steps: transcribe (gpt-4o-transcribe, language auto incl. Estonian) → story
  extraction (LLM, prompt from /api/prompts/distill@vN — see part B below) →
  title + emotional signature {tone, themes[], people[]}.
- Prime directive enforced in prompt AND in a post-check: no facts in the story
  absent from the transcript (run an entailment check prompt; flag, don't block).
- Port the useful logic from legacy prompts_engine.py / personal_context_mapper.py
  as typed modules with tests; do not port their OpenAI 0.x client usage.
- Store: entry doc, story doc, pipeline-run doc with per-step cost estimates.
- Golden tests: 6 fixture transcripts (provided: EN + ET, happy/sad/mundane) with
  snapshot-reviewed outputs; CI fails on unreviewed output drift.
Acceptance: P95 distill latency < 30s for a 2-min entry; founder review of 10
real entries finds zero invented details.
```

### P2.1 — Song pipeline

```
Task: story → playable song per docs/plan/03 and the cost ladder in docs/plan/07.
- Steps: lyrics+style prompt (LLM; style derived from emotional signature, prompt
  asset song@vN) → provider step with two implementations behind a flag:
  (a) "studio queue" — pipeline pauses at a human step; admin screen lists
  ready-to-paste lyrics + style string, founder generates in their own Suno
  account and uploads the MP3, pipeline resumes (reuse/port the legacy MP3
  upload path); (b) MiniMax Music via fal.ai (env: FAL_KEY; queue + webhook,
  poll fallback with backoff) → download MP3 + cover → Storage.
- Async UX contract: API returns pipeline-run id immediately; client shows
  "in the studio" state; push (or in-app event) on completion.
- Cost: log per-generation cost to generation_events; enforce per-user daily
  budget from env config; clear, friendly over-budget error.
- Failure UX: if provider fails after retries, user gets an apologetic state and
  an automatic retry later — never a dead spinner.
Acceptance: a real story produces a song the founder would actually send to
someone; cost per song known and logged.
```

(Prompts for P1.3, P1.4, P2.2–P2.4, P3.x, P4.x follow the same pattern: scope from
05, design from 02, infra rules from 03. Write them when the phase opens — earlier
phases will teach us things that should flow into later prompts.)

## B. Product generation prompts (the creative engine)

### Principles (binding for all generation prompts)

1. **Truth over polish**: never invent biographical facts. Style is free; facts
   are sacred. Every prompt carries this clause verbatim.
2. **The user's voice wins**: distillation preserves the speaker's idiom and
   specific images ("she always burned the rice") over generic eloquence.
3. **Find the agency**: when the raw material allows it, surface the narrator's
   choice/growth (redemptive framing per docs/plan/01) — but mundane entries are
   allowed to stay mundane; forced uplift reads as fake and kills trust.
4. **Format-true**: a song prompt thinks in hooks and repetition; a film script
   thinks in images and one emotional turn; a story thinks in scene and detail.
5. **Language**: respond in the language the user spoke (Estonian entries → 
   Estonian stories; lyrics may mix if the user does).

### Asset management process

- Prompts live in `/api/prompts/{name}@v{N}.md` with YAML front-matter:
  model, temperature, owner, changelog.
- Every change = PR with golden-test diff attached; founder approves tone changes.
- A/B at the pipeline level (run-doc records prompt version) so keep-rate and
  share-rate per prompt version are queryable — prompt quality becomes measurable,
  not vibes.

### Seed inventory to write in Phase 1

| Asset | Purpose |
|---|---|
| `distill@v1` | transcript → story (the single most important prompt in the company) |
| `signature@v1` | story → {tone, themes, people} |
| `title@v1` | story → evocative title (constraint: ≤ 6 words, no clichés list included) |
| `daily-question@v1` | context summary → tonight's question |
| `entailment-check@v1` | story + transcript → invented-detail flags |
| `recommend-format@v1` | signature → one format + one-line reason ("this wants to be a song because…") |

Phase 2 adds `song-lyrics@v1`, `song-style@v1`; Phase 3 adds `film-script@v1`,
`gift-*@v1`, `episode@v1`; safety adds `crisis-detect@v1` (Phase 1, runs on every
entry).
