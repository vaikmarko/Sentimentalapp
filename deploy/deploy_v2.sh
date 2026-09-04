#!/usr/bin/env bash
# Deploy Sentimental v2 (API -> Cloud Run, web -> Firebase Hosting) from any
# machine or Cursor cloud agent VM. Mirrors .github/workflows/deploy.yml.
#
# Credentials, one of:
#   - GCP_SA_KEY env var containing the service-account JSON (Cursor secret), or
#   - GOOGLE_APPLICATION_CREDENTIALS pointing to a key file, or
#   - an already-authenticated gcloud (local dev machine).
#
# Required for the API (first deploy; later deploys reuse Secret Manager):
#   OPENAI_API_KEY   synced into Secret Manager and mounted on Cloud Run.
#                    Production never runs in fake-provider mode.
#
# Usage:
#   bash deploy/deploy_v2.sh          # deploy API + web
#   bash deploy/deploy_v2.sh api      # API only
#   bash deploy/deploy_v2.sh web      # web only

set -euo pipefail

PROJECT="sentimental-f95e6"
REGION="europe-west1"
API_SERVICE="sentimental-api-v2"
HOSTING_TARGET="sentimentalapp-test"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-all}"

log() { echo ">>> $*"; }

# --- tooling ---------------------------------------------------------------

if ! command -v gcloud >/dev/null 2>&1; then
  log "gcloud not found - installing Google Cloud SDK (one-time, ~1 min)"
  curl -sSL https://sdk.cloud.google.com | bash -s -- --disable-prompts --install-dir="$HOME" >/dev/null
  export PATH="$HOME/google-cloud-sdk/bin:$PATH"
fi

if [[ "$TARGET" != "api" ]] && ! command -v firebase >/dev/null 2>&1; then
  log "firebase-tools not found - installing"
  npm install -g firebase-tools >/dev/null
fi

# --- auth ------------------------------------------------------------------

CLEANUP_KEY=""
if [[ -n "${GCP_SA_KEY:-}" ]]; then
  CLEANUP_KEY="$(mktemp /tmp/gcp-key-XXXXXX.json)"
  printf '%s' "$GCP_SA_KEY" > "$CLEANUP_KEY"
  export GOOGLE_APPLICATION_CREDENTIALS="$CLEANUP_KEY"
fi
trap '[[ -n "$CLEANUP_KEY" ]] && rm -f "$CLEANUP_KEY"' EXIT

if [[ -n "${GOOGLE_APPLICATION_CREDENTIALS:-}" ]]; then
  log "Activating service account from ${GOOGLE_APPLICATION_CREDENTIALS}"
  gcloud auth activate-service-account --key-file "$GOOGLE_APPLICATION_CREDENTIALS" --quiet
fi

if ! gcloud auth list --filter=status:ACTIVE --format='value(account)' | grep -q .; then
  echo "ERROR: no Google credentials." >&2
  echo "Set GCP_SA_KEY (service-account JSON) or run 'gcloud auth login' first." >&2
  echo "To create the key: run deploy/setup_deploy_credentials.sh in Cloud Shell." >&2
  exit 1
fi

gcloud config set project "$PROJECT" --quiet

# --- API -> Cloud Run --------------------------------------------------------

if [[ "$TARGET" == "all" || "$TARGET" == "api" ]]; then
  SECRET="openai-api-key"
  if [[ -n "${OPENAI_API_KEY:-}" ]]; then
    log "Syncing OPENAI_API_KEY into Secret Manager (${SECRET})"
    if ! gcloud secrets describe "$SECRET" --project "$PROJECT" >/dev/null 2>&1; then
      gcloud secrets create "$SECRET" --project "$PROJECT" --replication-policy automatic --quiet
    fi
    CURRENT="$(gcloud secrets versions access latest --secret "$SECRET" --project "$PROJECT" 2>/dev/null || true)"
    if [[ "$CURRENT" != "$OPENAI_API_KEY" ]]; then
      printf '%s' "$OPENAI_API_KEY" | gcloud secrets versions add "$SECRET" --project "$PROJECT" --data-file=- --quiet
    fi
    PROJECT_NUMBER="$(gcloud projects describe "$PROJECT" --format 'value(projectNumber)')"
    gcloud secrets add-iam-policy-binding "$SECRET" --project "$PROJECT" \
      --member "serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
      --role roles/secretmanager.secretAccessor --quiet >/dev/null
  elif ! gcloud secrets describe "$SECRET" --project "$PROJECT" >/dev/null 2>&1; then
    echo "ERROR: OPENAI_API_KEY is not set and Secret Manager has no '${SECRET}'." >&2
    echo "Production never runs with fake providers. Export OPENAI_API_KEY and retry." >&2
    exit 1
  else
    log "OPENAI_API_KEY not set locally - reusing the existing Secret Manager version"
  fi

  VERSION="$(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo manual)"
  log "Deploying API to Cloud Run (${API_SERVICE})"
  gcloud run deploy "$API_SERVICE" \
    --source "$REPO_ROOT/api" \
    --region "$REGION" \
    --project "$PROJECT" \
    --allow-unauthenticated \
    --set-env-vars "ENVIRONMENT=production,APP_VERSION=${VERSION},STORAGE_MODE=gcs,FAKE_PROVIDERS=false" \
    --update-secrets "OPENAI_API_KEY=${SECRET}:latest" \
    --quiet
fi

# --- web -> Firebase Hosting -------------------------------------------------

if [[ "$TARGET" == "all" || "$TARGET" == "web" ]]; then
  log "Building web app"
  (cd "$REPO_ROOT/web" && npm ci && npm run build)
  rm -rf "$REPO_ROOT/deploy/dist"
  cp -r "$REPO_ROOT/web/dist" "$REPO_ROOT/deploy/dist"

  log "Deploying web to Firebase Hosting (staging + production sites)"
  (cd "$REPO_ROOT/deploy" && firebase deploy \
    --only hosting \
    --project "$PROJECT" \
    --non-interactive)
fi

log "Done. Web: https://${HOSTING_TARGET}.web.app + https://sentimentalapp.com"
