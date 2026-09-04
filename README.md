# Sentimental v2

**Talk for two minutes — get back something beautiful enough to keep, share, or gift.**

Sentimental turns spoken personal moments into crafted media artifacts (stories,
songs, short films) using a long-term personal context engine. Design language:
"Night Studio" — see `docs/plan/02`.

## Repo layout

| Path | What |
|---|---|
| `web/` | React + TS + Vite + Tailwind v4 PWA (tabs: Tonight / Chronicle / You; Create + Resonance return when their features ship) |
| `api/` | FastAPI on Cloud Run — auth middleware, pipeline-run primitive, distill pipeline, versioned prompts |
| `docs/plan/` | the master plan (00–07). **Read `docs/plan/README.md` before any new work — decisions are binding.** |
| `deploy/` | v2 deploy config + scripts (`deploy_v2.sh`, credential bootstrap) |
| `LEGACY.md` | where the archived v1 app lives and what still runs |

## Development

```bash
# web
cd web && npm install && npm run dev

# api
cd api && pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload   # FAKE_PROVIDERS=true for zero-cost deterministic outputs

# tests
cd web && npm run test && npm run typecheck
cd api && pytest && ruff check . && mypy .
```

## Deploy

Pushes to `main` deploy automatically via `.github/workflows/deploy.yml`
(API → Cloud Run `sentimental-api-v2`, web → Firebase Hosting production site
`sentimentalapp.com` + staging site `sentimentalapp-test`). Manual deploy:
`bash deploy/deploy_v2.sh`.

- `OPENAI_API_KEY` (GitHub secret) is synced into Secret Manager (`openai-api-key`)
  and mounted on Cloud Run; the deploy fails if it is missing. Production never
  runs with fake providers (`app.main` refuses to start).
- `PLAUSIBLE_DOMAIN` (GitHub *variable*, optional) turns on the four funnel events
  in `web/src/lib/analytics.ts`. Unset = no analytics.

## Privacy

`/privacy` is the policy; `DELETE /api/me` (the "Delete my account" button under
*You*) erases recordings, entries, stories, pipeline runs and the Firebase Auth
user. Contact address lives in `web/src/features/legal/Privacy.tsx`.

Live: https://sentimentalapp.com (staging: https://sentimentalapp-test.web.app)
