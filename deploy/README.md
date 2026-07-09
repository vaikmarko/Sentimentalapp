# Deployment config (Sentimental v2)

v2 deploys to its own surfaces so the legacy app stays untouched until the
traffic flip (see `LEGACY.md` and `docs/plan/03`):

| Surface | Where | Config |
|---|---|---|
| API | Cloud Run service `sentimental-api-v2` (europe-west1) | `.github/workflows/deploy.yml` |
| Web | Firebase Hosting site `sentimentalapp-test` | this folder |

Root `firebase.json` / `.firebaserc` remain the **legacy** hosting config.

## Required GitHub Actions secrets

| Secret | Purpose |
|---|---|
| `GCP_SA_KEY` | service account JSON: Cloud Run deploy + build |
| `FIREBASE_SA_KEY` | service account JSON: Firebase Hosting deploy |
| `OPENAI_API_KEY` | passed to Cloud Run; enables real providers |

Without the first two, the deploy workflow skips quietly. Without the third,
the API starts with `FAKE_PROVIDERS=true` (deterministic outputs, zero spend).
