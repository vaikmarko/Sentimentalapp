#!/bin/bash

echo "🚀 Deploying Sentimental App DEMO environment..."

# Build and deploy demo version to Cloud Run
echo "📦 Building demo container..."
gcloud builds submit --tag gcr.io/sentimental-f95e6/sentimentalapp-demo .

echo "🌐 Deploying to Cloud Run (demo)..."
gcloud run deploy sentimentalapp-demo \
  --image gcr.io/sentimental-f95e6/sentimentalapp-demo \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars ENVIRONMENT=demo \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10

echo "🔗 Setting up Firebase hosting for demo..."
firebase use sentimental-f95e6
firebase deploy --only hosting --config firebase-demo.json

echo "✅ Demo deployment complete!"
echo "🌍 Demo URL: https://sentimentalapp-demo.web.app"
echo "📱 Mobile view: https://sentimentalapp-demo.web.app/app" 