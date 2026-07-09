# Sentimental v2

**Talk for two minutes — get back something beautiful enough to keep, share, or gift.**

Sentimental turns spoken personal moments into crafted media artifacts (stories,
songs, short films) using a long-term personal context engine. Design language:
"Night Studio" — see `docs/plan/02`.

## Repo layout

| Path | What |
|---|---|
| `web/` | React + TS + Vite + Tailwind v4 PWA (5 tabs: Tonight / Chronicle / Create / Resonance / You) |
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
(API → Cloud Run `sentimental-api-v2`, web → Firebase Hosting site
`sentimentalapp-test`). Manual deploy: `bash deploy/deploy_v2.sh`.

Live: https://sentimentalapp-test.web.app
