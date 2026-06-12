# 03 — Technical Architecture

> Principle: smart choices, not overkill. One web codebase, one API service, one
> worker, managed infra everywhere. Every choice below states what we deliberately
> did NOT pick.

## Stack decision summary

| Layer | Choice | Deliberately not |
|---|---|---|
| Frontend | React 18 + TypeScript + Vite + Tailwind, PWA | Next.js (no SSR need beyond share pages), React Native (see 00) |
| Native shell | Capacitor (Phase B) | Swift/Kotlin twin codebases |
| Backend API | **FastAPI** (Python) on Cloud Run | microservices, k8s, Node rewrite |
| Async jobs | Cloud Tasks → worker endpoints on the same Cloud Run service | Celery+Redis, Pub/Sub fan-out (overkill at this scale) |
| Data | Firestore (keep), Cloud Storage for media (keep) | Postgres migration (not worth it yet; revisit if relational queries dominate) |
| Auth | Firebase Auth (keep) | custom auth |
| Speech-to-text | OpenAI `gpt-4o-transcribe` / Whisper API (fallback: Gemini) | self-hosted Whisper |
| Story/LLM | provider-agnostic layer; frontier model via API (Claude/GPT class) | fine-tuning at launch |
| Music | ladder per doc 07: founder's Suno account (concierge) → MiniMax Music via fal.ai (~$0.04/song, official) → Suno wrapper as premium tier | training our own music model; cookie-based Suno automation (ToS risk) |
| Video | ladder per doc 07: concierge via founder's Higgsfield subscription → ffmpeg Ken Burns over generated stills → fal.ai/Higgsfield video API as premium | direct multi-vendor integrations |
| Voice/TTS | user's own recorded voice first (free, more intimate); ElevenLabs when TTS needed | — |
| Images | fal.ai image models (~$0.01–0.04/image) | separate image vendor subscriptions |
| Observability | Cloud Logging + Sentry + a `generation_events` Firestore collection for product metrics | full OTel stack |
| CI/CD | GitHub Actions → Cloud Run deploy + Firebase Hosting deploy | — |

Why FastAPI over keeping Flask: the entire product is async media orchestration
(webhooks, polling, parallel generation steps). FastAPI gives native async, typed
request/response models (Pydantic) that double as our API contract, and auto OpenAPI
docs. Python is kept so the valuable legacy engine logic (prompts, context mapping)
ports by copy-paste, not rewrite.

## Repository layout (target)

```
/web                  # React+TS+Vite PWA (replaces static/ AND public/static/ duplicates)
  /src
    /app              # routes, shell, tabs
    /features         # speak, reveal, chronicle, gift, resonance, wrapped
    /capabilities     # mic, push, share, haptics — web impl + Capacitor impl behind one interface
    /design           # tokens, primitives, motion
/api                  # FastAPI service
  /routes             # entries, stories, artifacts, gifts, share, webhooks
  /engines            # ported: prompts_engine, context_mapper (renamed, typed, tested)
  /pipelines          # distill, song, film, episode — each a declarative step list
  /providers          # llm.py, transcribe.py, suno.py, higgsfield.py, elevenlabs.py
/share                # share-page renderer (see below)
/legacy               # frozen current app.py + engines, read-only reference
/docs/plan            # this plan
```

## Migration strategy (strangler pattern)

The legacy `app.py` (3.8k lines) + dual JSX bundles are not refactored — they are
**frozen** and replaced surface by surface:

1. Stand up `/api` (FastAPI) and `/web` (Vite) skeletons with auth + CI from day one.
2. New product surfaces are built only in the new stack.
3. Legacy keeps serving existing users/routes until the new loop is feature-complete;
   then Cloud Run traffic flips, legacy moves to `/legacy`.
4. Data is shared throughout (same Firestore project), so there is no migration big-bang.
   New collections are namespaced `v2_*` where schemas diverge.

This avoids the classic trap of a half-refactored monolith plus a half-built rewrite.

## The media pipeline (the heart of the system)

Every artifact is produced by a **pipeline run**: a Firestore document tracking a
sequence of steps, executed by Cloud Tasks hitting worker endpoints.

```
ENTRY (voice upload)
  └─ distill:    transcribe → extract story → title + emotional signature   (~10–30s)
STORY
  ├─ song:       lyrics+style prompt → Suno job → poll/webhook → store MP3  (~1–3min)
  ├─ film:       script → ElevenLabs VO → Higgsfield visuals (async, webhook)
  │              → ffmpeg assembly on worker → store MP4                    (~2–5min)
  └─ episode:    weekly cron (Cloud Scheduler) → same film pipeline over N stories
```

Design rules:

- **Every step idempotent and resumable.** A pipeline run doc stores per-step status,
  provider job IDs, and outputs. Retry = re-run failed step only.
- **Webhooks first, polling fallback.** Higgsfield/aggregators support webhooks;
  the webhook route verifies signatures and advances the pipeline.
- **The user never waits on a spinner for slow steps.** Story (fast) is delivered
  inline; song/film notify via push + an in-app "in the studio" state with honest
  progress. UX contract: fast magic immediately, big magic minutes later.
- **Cost control:** every generation logs estimated cost to `generation_events`;
  per-user daily generation budget enforced at the API layer; credits/paywall
  attaches here later without redesign.

## Secrets & environments

Required secrets now (Cloud Run env / Cursor Cloud Agents secrets for dev agents):
`OPENAI_API_KEY` (or chosen LLM key), `FAL_KEY`, `SENTRY_DSN`.
Deferred until their rung activates (see doc 07): `ELEVENLABS_API_KEY`,
`HIGGSFIELD_API_KEY`, Suno-wrapper key.
Environments: `test` and `production` only (legacy had three; `demo` is retired —
the production share pages ARE the demo).

## Share-page rendering

Share pages need real `<meta og:*>` tags for link unfurls, so they cannot be pure
client-side SPA routes. Solution without adopting a full SSR framework: a small
FastAPI route renders share pages server-side from a Jinja template per artifact
type (story/song/film), embedding the media player. Firebase Hosting rewrites
`/s/**` to Cloud Run (this rewrite already exists in `firebase.json` — keep it).

## Testing & quality gates

- API: pytest; every pipeline step has a unit test with provider calls faked;
  one integration test per pipeline runs against real providers nightly (budgeted).
- Web: Vitest + Playwright smoke of the core loop (mock mic input).
- Prompts are versioned files with golden-output snapshot tests (see 06): a prompt
  change that shifts tone fails review visibly instead of silently.
- CI blocks merge on: typecheck, lint, unit tests, bundle-size budget.

## What we explicitly defer

- Postgres / vector DB: context retrieval starts as recent-N + per-user theme summary
  docs in Firestore. Add embeddings retrieval only when context quality demands it.
- Realtime collaboration (duet stories): designed for in the data model (artifacts
  have `participants[]`), built after launch.
- Self-hosted anything.
