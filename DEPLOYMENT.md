# Sentimental App - Deployment Guide

## Environment Overview

Sentimental App supports three different environments:

### 1. 🎭 Demo Environment (demo.sentimentalapp.com)
- **Purpose**: For showing to investors
- **Data**: Mock data (pre-created sample stories)
- **Features**: Read-only mode, adding new stories is blocked
- **Users**: Investors, partners

### 2. 🧪 Test Environment (test.sentimentalapp.com)  
- **Purpose**: For testing with real users
- **Data**: Real database
- **Features**: All features available
- **Users**: Beta testers, friends, acquaintances

### 3. 🚀 Production Environment (sentimentalapp.com)
- **Purpose**: Public version
- **Data**: Real database
- **Features**: All features available
- **Users**: General public

## Deployment Steps

### Prerequisites

1. Google Cloud SDK installed and configured
2. Firebase CLI installed (`npm install -g firebase-tools`)
3. Connected to Firebase project (`firebase login`)

### Demo Environment Deployment

```bash
# 1. Demo environment deployment
./deploy-demo.sh
```

This script:
- Builds Docker image for demo environment
- Deploys to Cloud Run
- Sets up Firebase hosting
- Sets environment variable `ENVIRONMENT=demo`

### Test Environment Deployment

```bash
# 2. Test environment deployment  
./deploy-test.sh
```

This script:
- Builds Docker image for test environment
- Deploys to Cloud Run
- Sets up Firebase hosting
- Sets environment variable `ENVIRONMENT=test`

### Production Environment Deployment

```bash
# 3. Production deployment (existing)
firebase deploy
```

## Environment Differences

### Demo Environment
- Uses `get_mock_stories()` function
- POST endpoints return 403 error
- Orange banner: "🎭 DEMO VERSION"
- Mock connections and inner space data

### Test Environment  
- Uses real database
- All features work
- Blue banner: "🧪 TEST VERSION"
- Real user data
- NLTK English stopwords fallback (if Estonian not available)

### Production Environment
- Uses real database
- All features work
- No banner
- Public usage

## URLs

- **Demo**: https://sentimentalapp-demo.web.app
- **Test**: https://sentimentalapp-test.web.app  
- **Production**: https://sentimentalapp.com

## Cloud Run Services

- **Demo**: https://sentimentalapp-demo-319737737925.europe-west1.run.app
- **Test**: https://sentimentalapp-test-319737737925.europe-west1.run.app
- **Production**: https://sentimentalapp-319737737925.europe-west1.run.app

## Mobile Views

- **Demo**: https://sentimentalapp-demo.web.app/app
- **Test**: https://sentimentalapp-test.web.app/app
- **Production**: https://sentimentalapp.com/app

## Monitoring

All environments use Google Analytics:
- Demo and Test environments are marked with environment variable
- Logs available in Google Cloud Console
- Firebase Hosting analytics

## Troubleshooting

### If deployment fails:

1. **Check Google Cloud authentication**:
   ```bash
   gcloud auth list
   gcloud config set project sentimental-f95e6
   ```

2. **Check Firebase authentication**:
   ```bash
   firebase login
   firebase use sentimental-f95e6
   ```

3. **Check Docker build**:
   ```bash
   docker build -f Dockerfile.demo -t test-demo .
   docker run -p 8080:8080 -e ENVIRONMENT=demo test-demo
   ```

### If environment doesn't work correctly:

1. **Check environment variable**:
   - In Cloud Run console check environment variables
   - Should be `ENVIRONMENT=demo` or `ENVIRONMENT=test`

2. **Check logs**:
   ```bash
   gcloud logs read --service=sentimentalapp-demo
   gcloud logs read --service=sentimentalapp-test
   ```

## Next Steps

1. **Demo deployment for investors**:
   - Deploy demo environment
   - Test all features
   - Send link to investors

2. **Test environment setup**:
   - Deploy test environment
   - Add beta testers
   - Collect feedback

3. **Production preparation**:
   - Apply changes based on test environment
   - Prepare for public launch 