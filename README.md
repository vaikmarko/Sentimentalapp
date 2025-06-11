# Sentimental - Personal Story Generation Platform

A sophisticated AI-powered platform that transforms personal conversations into meaningful stories and formats them into various media types (songs, reels, podcasts, etc.).

## 🎯 Core Features

- **AI Chat Interface**: Natural conversation with intelligent context awareness
- **Story Generation**: Transform conversations into authentic personal narratives  
- **Multi-Format Creation**: Generate 17+ formats including songs, reels, podcasts, journal entries
- **Music Integration**: Upload MP3 files to generated songs
- **Real-time Updates**: Stories and formats update immediately without page refresh
- **Clean UX**: Simplified interface focused on user experience

## 🏗️ Project Structure

### Core Application Files
```
app.py                          # Main Flask application (2420 lines)
utils.py                        # Common utility functions
requirements.txt                # Python dependencies
```

### AI Engine System
```
prompts_engine.py              # Centralized prompt management (994 lines)
formats_generation_engine.py   # Format generation logic (364 lines)
smart_story_engine.py          # Story generation engine (769 lines)
personal_context_mapper.py     # User context analysis (515 lines)  
knowledge_engine.py            # Domain knowledge processing (391 lines)
format_types.py                # Format type definitions (37 lines)
```

### Frontend & UI
```
templates/
├── index.html                 # Landing page
└── app.html                   # Main application shell

static/
├── js/
│   └── sentimental-app.jsx    # Main React application
├── css/                       # Stylesheets
├── icons/                     # App icons and assets
├── uploads/                   # User uploaded files
└── manifest.json              # PWA manifest
```

### Configuration & Deployment
```
package.json                   # Node.js dependencies
firebase.json                  # Firebase configuration
firestore.rules               # Database security rules
Dockerfile                    # Container configuration
.gitignore                    # Git ignore rules
firebase-credentials.json     # Firebase service account
```

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

2. **Set Environment Variables**
   ```bash
   export OPENAI_API_KEY="your_openai_key"
   export ENVIRONMENT="test"  # or "demo", "production"
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the App**
   - Landing page: `http://localhost:8080`
   - Main app: `http://localhost:8080/app`

## 🧠 AI Engine Architecture

### Prompt Management (`prompts_engine.py`)
- Centralized prompt templates for all AI operations
- Support for multiple AI providers (OpenAI, Claude, etc.)
- Optimized prompts for different content types

### Format Generation (`formats_generation_engine.py`)
- Generates 17+ different content formats
- Context-aware generation using user profiles
- Quality optimization and validation

### Story Engine (`smart_story_engine.py`)
- Transforms conversations into authentic narratives
- Maintains natural, conversational tone
- Focuses on personal growth and insight

### Context Mapping (`personal_context_mapper.py`)
- Analyzes user conversation patterns
- Builds psychological and behavioral profiles
- Provides context for personalized content

### Knowledge Engine (`knowledge_engine.py`)
- Domain-specific insight analysis
- Emotional and thematic understanding
- Cross-story connection discovery

## 📋 Supported Formats

**Therapeutic & Growth**
- Reflection, Insights, Growth Summary, Journal Entry

**Social Media**
- Instagram Reel, TikTok Script, Twitter Thread, LinkedIn Post

**Long-form Content**  
- Blog Post, Newsletter, Podcast Episode, Letter

**Creative**
- Song (with MP3 upload), Poem, Short Story, Children's Story

**Professional**
- Email, Book Chapter

## 🔧 Key Features Implemented

### ✅ Music Upload for Everyone
- Removed admin restrictions
- All users can upload MP3 files to generated songs
- Audio integration with song formats

### ✅ Simplified UI
- Removed unnecessary lock icons and messages
- Clean, minimal interface for non-authors viewing stories
- Focus on content over restrictions

### ✅ Real-time Story Updates  
- Generated formats appear immediately in story lists
- No need to refresh pages or re-login
- Seamless user experience

### ✅ Clean Codebase
- Removed 80+ redundant test/debug files
- Centralized utility functions
- Eliminated duplicate code patterns
- Clear separation of concerns

## 🎨 User Experience

**For Story Authors:**
- Create stories from conversations
- Generate any format type
- Upload music to songs
- Manage privacy settings

**For Story Viewers:**
- View all existing formats
- Clean interface without restriction messages
- No unnecessary UI clutter

## 🔒 Authentication & Access

- Firebase Authentication integration
- Early access code system (`UNICORN`, `SENTI2025`)
- Demo user support
- Proper user session management

## 🚦 Environment Support

- **Test**: Local development with full debugging
- **Demo**: Polished experience for demonstrations  
- **Production**: Live deployment optimized

## 🚀 Deployment

For detailed deployment instructions, troubleshooting, and API key management, see **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)**.

### Quick Deploy to Test Environment
```bash
# Deploy with API key
gcloud run deploy sentimentalapp-test \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY="$(python3 -c "import os; from dotenv import load_dotenv; load_dotenv('functions/.env'); load_dotenv(); print(os.getenv('OPENAI_API_KEY'))")"

# Deploy hosting
firebase deploy --only hosting
```

---

**Clean, focused, and ready for users! 🎉** 