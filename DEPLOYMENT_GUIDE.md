# 🚀 Sentimental App Deployment Guide

## 🏗️ System Architecture Overview

### Components
- **Frontend**: Static files served by Firebase Hosting
- **Backend**: Python Flask app running on Google Cloud Run
- **Database**: Firebase Firestore
- **Authentication**: Firebase Auth
- **API**: OpenAI GPT for conversations and story generation

### Infrastructure Flow
```
User → Firebase Hosting → Cloud Run Service → Firestore + OpenAI API
```

## 🔑 API Key Management

### How API Keys Work
The OpenAI API key is loaded using Python's `dotenv` package:

```python
# In app.py lines 22-23:
load_dotenv('functions/.env')  # Load from functions/.env first
load_dotenv()                 # Then try root .env as fallback
```

### Key Storage Locations
1. **Local Development**: System environment variables (loaded via dotenv)
2. **Production**: Cloud Run environment variables

### Getting the API Key
To find the current API key that's working locally:
```bash
python3 -c "import os; from dotenv import load_dotenv; load_dotenv('functions/.env'); load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

## 🌍 Environment Setup

### Regions & Services
- **Primary Region**: `europe-west1` 
- **Test Services**: 
  - `sentimentalapp-test` (europe-west1) ← **Main test environment**
  - `sentimentalapp-test` (us-central1) ← **Backup/experimental**

### Firebase Hosting Configuration
Firebase hosting redirects are configured in `firebase.json`:
```json
{
  "redirects": [
    {
      "source": "/app/**",
      "destination": "https://sentimentalapp-test-319737737925.europe-west1.run.app/app/**",
      "type": 301
    },
    {
      "source": "/**", 
      "destination": "https://sentimentalapp-test-319737737925.europe-west1.run.app/**",
      "type": 301
    }
  ]
}
```

## 📋 Step-by-Step Deployment Process

### 1. Deploy Code to Cloud Run

#### For Test Environment (europe-west1):
```bash
# Deploy with API key from local environment
gcloud run deploy sentimentalapp-test \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY="$(python3 -c "import os; from dotenv import load_dotenv; load_dotenv('functions/.env'); load_dotenv(); print(os.getenv('OPENAI_API_KEY'))")"
```

#### For Production Environment:
```bash
gcloud run deploy sentimentalapp \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY="$(python3 -c "import os; from dotenv import load_dotenv; load_dotenv('functions/.env'); load_dotenv(); print(os.getenv('OPENAI_API_KEY'))")"
```

### 2. Deploy Firebase Hosting
```bash
firebase deploy --only hosting
```

### 3. Verify Deployment
Check that the correct service is running:
```bash
gcloud run services list --filter="sentimentalapp-test"
```

## 🔧 Environment Variables Setup

### Required Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for chat and story generation
- `ENVIRONMENT`: Set to `test`, `demo`, or `production`

### Setting Environment Variables in Cloud Run
```bash
gcloud run services update [SERVICE_NAME] \
  --region [REGION] \
  --set-env-vars OPENAI_API_KEY="[YOUR_API_KEY]"
```

## 🐛 Troubleshooting Common Issues

### Issue 1: Chat Giving Hardcoded Responses
**Symptoms**: Chat always responds with "I'm here to listen and help you discover more about yourself..."

**Causes**:
1. OpenAI API key not set in Cloud Run
2. Firebase pointing to wrong service
3. Old code deployed without fixes

**Solutions**:
1. Check API key: `gcloud run services describe [SERVICE] --region [REGION]`
2. Verify Firebase redirects in `firebase.json`
3. Redeploy latest code with API key

### Issue 2: Firebase Hosting Pointing to Wrong Service
**Symptoms**: Changes not appearing on test site

**Causes**:
1. Multiple services in different regions
2. Firebase redirects pointing to old service

**Solutions**:
1. Check `firebase.json` redirects
2. Ensure region matches deployed service
3. Deploy Firebase hosting after changes

### Issue 3: API Key Not Found
**Symptoms**: Logs show "OPENAI_API_KEY not found"

**Solutions**:
1. Get key from local: `python3 -c "import os; from dotenv import load_dotenv; load_dotenv('functions/.env'); load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"`
2. Set in Cloud Run: `gcloud run services update [SERVICE] --set-env-vars OPENAI_API_KEY="[KEY]"`

## 📝 Deployment Checklist

### Before Deployment
- [ ] Test changes locally
- [ ] Verify API key is accessible locally
- [ ] Check which region/service Firebase is pointing to

### During Deployment
- [ ] Deploy to correct region (europe-west1 for test)
- [ ] Include API key in deployment command
- [ ] Deploy Firebase hosting after Cloud Run changes
- [ ] Wait for deployment to complete

### After Deployment
- [ ] Check service status: `gcloud run services list`
- [ ] Verify API key is set in service
- [ ] Test chat functionality on live site
- [ ] Check logs for any errors

## 🔗 Useful Commands

### View Service Details
```bash
gcloud run services describe sentimentalapp-test --region europe-west1
```

### Check Logs
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=sentimentalapp-test" --limit=10
```

### List All Services
```bash
gcloud run services list
```

### Get Firebase Hosting Info
```bash
firebase hosting:sites:list
```

## ⚠️ Important Notes

1. **Always deploy to `europe-west1`** for the main test environment
2. **Include API key** in every Cloud Run deployment
3. **Deploy Firebase hosting** after Cloud Run changes
4. **Check logs** if chat isn't working properly
5. **Test locally first** before deploying

## 🎯 Quick Fix Commands

### Full Redeployment (when in doubt):
```bash
# 1. Deploy Cloud Run with API key
gcloud run deploy sentimentalapp-test \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY="$(python3 -c "import os; from dotenv import load_dotenv; load_dotenv('functions/.env'); load_dotenv(); print(os.getenv('OPENAI_API_KEY'))")"

# 2. Deploy Firebase hosting
firebase deploy --only hosting

# 3. Test the site
echo "Test at: https://sentimentalapp-test.web.app/app"
``` 