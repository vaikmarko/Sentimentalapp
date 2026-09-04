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
app/pipelines/   the pipeline-run primitive: models, store, runner, distill (+ "echo" test pipeline)
app/providers/   provider interface + fake mode; real impls land per phase
app/clients/     media storage, Cloud Tasks enqueue helper
app/routes/      health, entries, stories, account (DELETE /api/me), /internal/tasks worker
```

`/internal/tasks/step` is mounted only when `TASKS_INLINE=false` and verifies
the Cloud Tasks OIDC token itself (audience = its own URL, email = the queue's
service account), because the Cloud Run service is public for `/api/*`.

## Execution modes (env)

| Variable | Default | Meaning |
|---|---|---|
| `ENVIRONMENT` | `test` | `test` uses in-memory run store; otherwise Firestore |
| `FAKE_PROVIDERS` | `true` | deterministic provider outputs, zero spend |
| `TASKS_INLINE` | `true` | execute pipeline steps in-process instead of Cloud Tasks |
| `WORKER_BASE_URL` | — | Cloud Run URL for task callbacks (required when `TASKS_INLINE=false`) |
| `SENTRY_DSN` | — | enables Sentry |

Production deploys set `FAKE_PROVIDERS=false` and mount `OPENAI_API_KEY` from
Secret Manager; the app refuses to start in production with fake providers.
`TASKS_INLINE` is still `true` in production (steps run inside the request);
flipping it requires `WORKER_BASE_URL` and the `pipeline-steps` queue.
