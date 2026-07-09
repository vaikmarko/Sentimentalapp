#!/bin/bash
set -e

echo "🚀 Deploying to Production..."

# Build first
./deploy/scripts/build.sh

# Load env keys from .env without printing them
set -a
source .env
set +a

if [ -z "$OPENAI_API_KEY" ] || [ -z "$MENTALOS_OPENAI_API_KEY" ]; then
  echo "❌ OPENAI_API_KEY or MENTALOS_OPENAI_API_KEY missing from .env"
  exit 1
fi

ENV_VARS_FILE=$(mktemp)
trap 'rm -f "$ENV_VARS_FILE"' EXIT
cat > "$ENV_VARS_FILE" <<EOF
OPENAI_API_KEY: "$OPENAI_API_KEY"
MENTALOS_OPENAI_API_KEY: "$MENTALOS_OPENAI_API_KEY"
EOF

# Deploy backend to Cloud Run
echo "Deploying backend to Cloud Run..."
gcloud run deploy sentimentalapp \
  --project sentimental-f95e6 \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --env-vars-file "$ENV_VARS_FILE"

# Deploy frontend to Firebase
echo "Deploying frontend to Firebase Hosting..."
firebase deploy --only hosting --project sentimental-f95e6

echo "✅ Production deployment complete!"
echo "🌍 Live at: https://sentimentalapp.com"
