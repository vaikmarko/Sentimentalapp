# Sentimental App

Transform your personal moments into creative stories, music, and meaningful content with AI-powered insights.

## 🆕 What's New - Mobile App Interface

We've added a **complete mobile-first React interface** that provides:

- **📱 PWA Support** - Install as a mobile app
- **🎨 Modern UI** - Clean, Instagram-like design
- **📊 Story Discovery** - Browse community stories
- **💫 Inner Space Integration** - Connect to your 3D inner space
- **🔄 Multiple Formats** - Transform stories into songs, articles, videos
- **💬 Chat Interface** - Talk with Sentimental AI

## 🚀 Getting Started

### 1. Start the Flask Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### 2. Access the Different Interfaces

- **🏠 Main Website**: `http://localhost:8080/` - Marketing landing page
- **📱 Mobile App**: `http://localhost:8080/app` - New React mobile interface
- **💬 Chat Beta**: `http://localhost:8080/chat` - Original chat interface
- **🌌 3D Inner Space**: `http://localhost:8080/inner-space` - 3D visualization
- **📚 Story Deck**: `http://localhost:8080/deck` - Story management

## 📱 Mobile App Features

### Four Main Views:

1. **Discover** 🔍
   - Browse public stories from the community
   - Filter by format (Songs, Articles, Videos, etc.)
   - Like and explore full stories

2. **Your Stories** 📖
   - View your personal stories
   - See generated formats for each story
   - Cosmic integration status
   - Edit and manage stories

3. **Share** 💬
   - Chat with Sentimental AI
   - Create new stories through conversation
   - Voice memos and text input

4. **Space** ✨
   - Your inner space dashboard
   - AI insights and patterns
   - Link to 3D inner space visualization
   - Personal analytics

### PWA Installation

The mobile app can be installed on your phone:

1. Visit `/app` on your mobile browser
2. Look for the "Install" banner or "Add to Home Screen"
3. Install and use like a native app
4. Works offline with cached content

## 🔧 Technical Architecture

### Frontend Stack
- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first styling
- **PWA** - Service Worker for offline support
- **Responsive Design** - Mobile-first approach

### Backend APIs
- `GET /api/stories` - Fetch all stories
- `POST /api/stories` - Create new story
- `POST /api/stories/{id}/formats` - Generate story formats
- `GET /api/inner-space-data` - Inner space visualization data
- `GET /api/connections/{id}` - Story connections
- `GET /api/insights/{id}` - Story insights

### Database Structure (Firestore)

```javascript
// Stories Collection
{
  id: string,
  title: string,
  content: string,
  author: string,
  timestamp: string,
  format: string,
  public: boolean,
  reactions: number,
  inInnerSpace: boolean,
  createdFormats: string[],
  analysis: {
    themes: string[],
    emotions: string[],
    sentiment_score: number
  }
}

// Connections Collection
{
  story_id: string,
  connected_story_id: string,
  common_words: string[],
  strength: number,
  created_at: timestamp
}
```

## 🎨 Story Formats

The app can transform your stories into:

- **🎵 Songs** - Lyrics with melody descriptions
- **📹 Videos** - Visual story scripts
- **📝 Articles** - Blog-style content
- **🐦 Tweet Threads** - Social media format
- **💼 LinkedIn Posts** - Professional insights
- **👥 Facebook Posts** - Social sharing format
- **📚 Book Chapters** - Literary narrative
- **📖 Diary Entries** - Personal reflection format

## 🌌 Inner Space Integration

The 3D inner space view (`/inner-space`) visualizes:
- Story connections and relationships
- Emotional patterns and themes
- Personal growth journey
- Interactive 3D exploration

## 🔮 AI Features

- **Text Analysis** - Extract themes and emotions
- **Story Connections** - Find patterns between stories
- **Format Generation** - Create multiple content types
- **Insights** - Personal pattern recognition
- **Therapeutic Reflection** - Self-understanding tools

## 📱 Mobile-First Design

The new interface prioritizes:
- **Touch-friendly** interactions
- **Swipe gestures** for navigation
- **Loading states** for better UX
- **Offline capability** through PWA
- **App-like experience** with full-screen mode

## 🚀 Deployment

### Firebase Hosting + Cloud Run

1. **Backend**: Deploy Flask app to Google Cloud Run
2. **Frontend**: Static assets served via Flask
3. **Database**: Firestore for scalable storage
4. **PWA**: Automatic app installation prompts

### Environment Variables

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
PORT=8080
```

## 🔧 Development

### Adding New Story Formats

1. Update `generate_format_content()` in `app.py`
2. Add format icons in React component
3. Update format colors in UI
4. Test format generation API

### Customizing UI

The React component is in `/static/js/sentimental-app.jsx`:
- Modify colors in `formatColors` object
- Update icons in inline SVG components  
- Adjust layouts in render functions

## 🎯 Next Steps

- [ ] Add user authentication
- [ ] Implement real AI format generation
- [ ] Voice recording for stories
- [ ] Push notifications for PWA
- [ ] Social sharing features
- [ ] Premium format types
- [ ] Analytics dashboard
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on mobile devices
5. Submit a pull request

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: This README
- **Chat**: `/chat` interface for testing

---

**Ready to transform your life into meaningful stories?** Visit `/app` to start your journey! 🌟 