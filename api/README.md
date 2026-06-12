# Sentimental API (v2)

FastAPI service on Cloud Run. Architecture and decisions: `docs/plan/03`.

## Commands

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000   # dev server
pytest                                       # tests (fake providers, in-memory store)
ruff check app tests
mypy app
```

## Structure

```
app/core/        config (env settings), auth (Firebase ID-token dependency)
app/pipelines/   the pipeline-run primitive: models, store, runner, demo "echo"
app/providers/   provider interface + fake mode; real impls land per phase
app/clients/     Cloud Tasks enqueue helper
app/routes/      health, demo endpoints, /internal/tasks worker routes
```

## Execution modes (env)

| Variable | Default | Meaning |
|---|---|---|
| `ENVIRONMENT` | `test` | `test` uses in-memory run store; otherwise Firestore |
| `FAKE_PROVIDERS` | `true` | deterministic provider outputs, zero spend |
| `TASKS_INLINE` | `true` | execute pipeline steps in-process instead of Cloud Tasks |
| `WORKER_BASE_URL` | — | Cloud Run URL for task callbacks (required when `TASKS_INLINE=false`) |
| `SENTRY_DSN` | — | enables Sentry |

Deployment flips `TASKS_INLINE=false` and `FAKE_PROVIDERS=false` per provider
as real implementations land (docs/plan/05 phases, docs/plan/07 budget ladder).
