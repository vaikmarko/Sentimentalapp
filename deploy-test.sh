#!/bin/bash

echo "🚀 Deploying Sentimental App TEST environment..."

# Build and deploy test version to Cloud Run
echo "📦 Building test container..."
gcloud builds submit --tag gcr.io/sentimental-f95e6/sentimentalapp-test .

echo "🌐 Deploying to Cloud Run (test)..."
gcloud run deploy sentimentalapp-test \
  --image gcr.io/sentimental-f95e6/sentimentalapp-test \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=test \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10

echo "🔗 Setting up Firebase hosting for test..."
firebase use sentimental-f95e6
firebase deploy --only hosting --config firebase-test.json

echo "✅ Test deployment complete!"
echo "🌍 Test URL: https://sentimentalapp-test.web.app"
echo "📱 Mobile view: https://sentimentalapp-test.web.app/app" 