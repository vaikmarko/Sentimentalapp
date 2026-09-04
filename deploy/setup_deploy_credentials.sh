#!/usr/bin/env bash
# One-paste setup: run this in Google Cloud Shell (https://console.cloud.google.com
# -> ">_" Cloud Shell icon, top right). It creates the deploy service account,
# grants the roles needed for Cloud Run + Firebase Hosting deploys, and prints
# a JSON key to copy into GitHub / Cursor secrets.
#
#   curl -fsSL https://raw.githubusercontent.com/vaikmarko/sentimentalapp/main/deploy/setup_deploy_credentials.sh | bash
#
# Idempotent: safe to re-run (re-running creates a fresh key each time).

set -euo pipefail

PROJECT="sentimental-f95e6"
SA_NAME="github-deploy"
SA_EMAIL="${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
KEY_FILE="$(mktemp /tmp/deploy-key-XXXXXX.json)"

echo ">>> Using project: ${PROJECT}"
gcloud config set project "${PROJECT}" --quiet

if ! gcloud iam service-accounts describe "${SA_EMAIL}" >/dev/null 2>&1; then
  echo ">>> Creating service account ${SA_EMAIL}"
  gcloud iam service-accounts create "${SA_NAME}" \
    --display-name "GitHub Actions / Cursor deploy" --quiet
else
  echo ">>> Service account ${SA_EMAIL} already exists"
fi

# One service account covers both Cloud Run (API) and Firebase Hosting (web).
ROLES=(
  roles/run.admin
  roles/cloudbuild.builds.editor
  roles/iam.serviceAccountUser
  roles/storage.admin
  roles/artifactregistry.admin
  roles/firebasehosting.admin
  roles/serviceusage.serviceUsageConsumer
  roles/secretmanager.admin  # syncs OPENAI_API_KEY into Secret Manager + grants Cloud Run access
)
for ROLE in "${ROLES[@]}"; do
  echo ">>> Granting ${ROLE}"
  gcloud projects add-iam-policy-binding "${PROJECT}" \
    --member "serviceAccount:${SA_EMAIL}" \
    --role "${ROLE}" \
    --condition=None --quiet >/dev/null
done

echo ">>> Creating JSON key"
gcloud iam service-accounts keys create "${KEY_FILE}" \
  --iam-account "${SA_EMAIL}" --quiet

echo
echo "=================================================================="
echo "DONE. Copy EVERYTHING between the BEGIN/END lines below (the whole"
echo "JSON block) and paste it as the value of BOTH secrets:"
echo
echo "  1. GitHub -> repo Settings -> Secrets and variables -> Actions:"
echo "       GCP_SA_KEY       = <the JSON below>"
echo "       FIREBASE_SA_KEY  = <the same JSON>"
echo "       OPENAI_API_KEY   = <your OpenAI key>"
echo
echo "  2. (optional, lets Cursor agents deploy directly)"
echo "     cursor.com -> Dashboard -> Cloud Agents -> Secrets: same three."
echo
echo "----------------------- BEGIN KEY JSON --------------------------"
cat "${KEY_FILE}"
echo "------------------------ END KEY JSON ---------------------------"
rm -f "${KEY_FILE}"
