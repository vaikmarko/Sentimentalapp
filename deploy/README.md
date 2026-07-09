# Deployment config (Sentimental v2)

v2 deploys to its own surfaces so the legacy app stays untouched until the
traffic flip (see `LEGACY.md` and `docs/plan/03`):

| Surface | Where | Config |
|---|---|---|
| API | Cloud Run service `sentimental-api-v2` (europe-west1) | `.github/workflows/deploy.yml` |
| Web | Firebase Hosting site `sentimentalapp-test` | this folder |

Root `firebase.json` / `.firebaserc` remain the **legacy** hosting config.

## One-time credential setup

Open [Google Cloud Console](https://console.cloud.google.com) -> Cloud Shell
(`>_` icon, top right) and paste:

```bash
curl -fsSL https://raw.githubusercontent.com/vaikmarko/sentimentalapp/main/deploy/setup_deploy_credentials.sh | bash
```

It creates the `github-deploy` service account with all needed roles and
prints a JSON key. Paste that JSON as the value of these secrets:

| Where | Secrets |
|---|---|
| GitHub repo -> Settings -> Secrets and variables -> Actions | `GCP_SA_KEY` = key JSON, `FIREBASE_SA_KEY` = same JSON, `OPENAI_API_KEY` = OpenAI key |
| [Cursor Dashboard](https://cursor.com/dashboard) -> Cloud Agents -> Secrets (optional, lets agents deploy directly) | same three |

Without the first two, the deploy workflow skips quietly. Without the third,
the API starts with `FAKE_PROVIDERS=true` (deterministic outputs, zero spend).

## Deploying

- **Automatic:** every push to `main` runs `.github/workflows/deploy.yml`
  (once GitHub secrets exist). Manual trigger: repo -> Actions -> Deploy ->
  Run workflow.
- **From a machine / Cursor agent VM:** `bash deploy/deploy_v2.sh` (or
  `... api` / `... web` for one surface). Uses `GCP_SA_KEY` env var, a
  `GOOGLE_APPLICATION_CREDENTIALS` key file, or an existing `gcloud auth
  login` session; installs gcloud/firebase-tools itself if missing.
