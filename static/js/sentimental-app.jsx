const { useState, useEffect, useRef } = React;

// Lucide icons as inline SVG components since we can't import them directly
const Search = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8"/>
    <path d="m21 21-4.35-4.35"/>
  </svg>
);

const Heart = ({ size = 16, filled = false }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill={filled ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
  </svg>
);

const MessageCircle = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
  </svg>
);

const Sparkles = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .962 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.582a.5.5 0 0 1 0 .962L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.962 0L9.937 15.5z"/>
  </svg>
);

const Plus = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 5v14M5 12h14"/>
  </svg>
);

const BookOpen = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
  </svg>
);

const ArrowLeft = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="19" y1="12" x2="5" y2="12"/>
    <polyline points="12,19 5,12 12,5"/>
  </svg>
);

const X = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="6" x2="6" y2="18"/>
    <line x1="6" y1="6" x2="18" y2="18"/>
  </svg>
);

// Format icons
const getFormatIcon = (formatType) => {
  const icons = {
    // Social Media Formats
    twitter: '🐦',
    linkedin: '💼', 
    instagram: '📸',
    facebook: '👥',
    tweet: '🐦',
    
    // Creative Formats
    song: '🎵',
    poem: '🎭',
    video: '🎬',
    script: '🎬',
    
    // Modern Viral Formats
    tiktok_script: '📱',
    instagram_reel: '🎬',
    twitter_thread: '🧵',
    youtube_short: '▶️',
    instagram_story: '📸',
    
    // Content Formats
    article: '📝',
    blog_post: '✍️',
    short_story: '📚',
    presentation: '📊',
    newsletter: '📰',
    
    // Reflection Formats
    insights: '💡',
    reflection: '🤔',
    growth_summary: '🌱',
    journal_entry: '📔',
    diary_entry: '📔',
    
    // Professional Formats
    podcast_segment: '🎧',
    email: '✉️',
    letter: '💌'
  };
  return icons[formatType] || '📄';
};

// Main App Component
const SentimentalApp = () => {
  const [currentView, setCurrentView] = useState('discover');
  const [previousView, setPreviousView] = useState('discover');
  const [user, setUser] = useState(null);
  const [stories, setStories] = useState([]);
  const [selectedStory, setSelectedStory] = useState(null);
  const [showLogin, setShowLogin] = useState(false);
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [loadingFormat, setLoadingFormat] = useState(false);
  const [loginForm, setLoginForm] = useState({ name: '', email: '', password: '' });
  const [isSignupMode, setIsSignupMode] = useState(false);
  const [appInitialized, setAppInitialized] = useState(false);

  // Format viewing state
  const [currentFormat, setCurrentFormat] = useState(null);
  const [formatContent, setFormatContent] = useState('');
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadingAudio, setUploadingAudio] = useState(false);

  // Initialize
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Load initial data
        await fetchStories();
        
        // Check for existing user session
        const savedUser = localStorage.getItem('sentimental_user');
        if (savedUser) {
          try {
            setUser(JSON.parse(savedUser));
          } catch (e) {
            localStorage.removeItem('sentimental_user');
          }
        }

        // Set up Firebase auth state listener
        const unsubscribe = window.firebaseAuth?.onAuthStateChanged(async (firebaseUser) => {
          if (firebaseUser) {
            const userData = {
              id: firebaseUser.uid,
              email: firebaseUser.email,
              name: firebaseUser.displayName || firebaseUser.email.split('@')[0],
              emailVerified: firebaseUser.emailVerified,
              photoURL: firebaseUser.photoURL
            };
            
            setUser(userData);
            localStorage.setItem('sentimental_user', JSON.stringify(userData));
          } else {
            // User is signed out or authentication failed
            // Only clear if user was previously authenticated via Firebase
            const savedUser = localStorage.getItem('sentimental_user');
            if (savedUser) {
              try {
                const parsedUser = JSON.parse(savedUser);
                // Only clear if it's a Firebase user (not a demo user)
                if (parsedUser.id && !parsedUser.id.startsWith('demo_')) {
                  setUser(null);
                  localStorage.removeItem('sentimental_user');
                }
              } catch (e) {
                // If parsing fails, clear anyway
                setUser(null);
                localStorage.removeItem('sentimental_user');
              }
            }
          }
        });

        // Mark app as initialized
        setAppInitialized(true);
        
        return () => unsubscribe?.();
      } catch (error) {
        console.error('App initialization error:', error);
        // Still mark as initialized even if there are errors
        setAppInitialized(true);
      }
    };

    initializeApp();
  }, []);

  const fetchStories = async () => {
    try {
      const response = await fetch('/api/stories');
      if (response.ok) {
        const data = await response.json();
        setStories(data);
      }
    } catch (error) {
      console.error('Error fetching stories:', error);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // For now, just create a demo user
      const demoUser = {
        id: 'demo_' + Date.now(),
        name: loginForm.name || 'Demo User',
        email: loginForm.email || 'demo@example.com'
      };
      setUser(demoUser);
      localStorage.setItem('sentimental_user', JSON.stringify(demoUser));
      setShowLogin(false);
    } catch (error) {
      console.error('Login error:', error);
      alert('Login failed. Please try again.');
    }
    
    setIsLoading(false);
  };

  const handleGoogleAuth = async () => {
    setIsLoading(true);
    try {
      if (window.firebaseAuth && window.authProviders) {
        const result = await window.firebaseAuth.signInWithPopup(window.authProviders.google);
        // User will be set automatically by the auth state listener
        setShowLogin(false);
      }
    } catch (error) {
      console.error('Google login error:', error);
      alert('Google login failed. Please try again.');
    }
    setIsLoading(false);
  };

  const handleLogout = async () => {
    try {
      if (window.firebaseAuth) {
        await window.firebaseAuth.signOut();
      }
      setUser(null);
      localStorage.removeItem('sentimental_user');
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const sendMessage = async () => {
    if (!message.trim()) return;
    
    // Check if user is authenticated before allowing chat
    if (!user || !user.id || user.id === 'anonymous' || user.id === 'anonymous_user' || user.id === '' || user.id === 'null' || user.id === 'undefined') {
      setShowLogin(true);
      return;
    }
    
    const userMessage = message;
    setMessage('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          user_id: user.id
        })
      });

      const data = await response.json();
      if (response.status === 401) {
        // Authentication required
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: data.message || 'Please sign in to continue chatting.' 
        }]);
        setShowLogin(true);
      } else if (data.success) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      } else {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: 'Sorry, I encountered an error. Please try again.' 
        }]);
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }]);
    }
    setIsLoading(false);
  };

  const createStoryFromConversation = async () => {
    if (messages.length === 0) return;
    
    // Require authentication for story creation
    if (!user || !user.id || user.id === 'anonymous' || user.id === 'anonymous_user' || user.id === '' || user.id === 'null' || user.id === 'undefined') {
      setShowLogin(true);
      return;
    }
    
    setIsLoading(true);
    try {
      const response = await fetch('/api/stories/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation: messages,
          user_id: user.id,
          author: user.name || 'User',
          is_public: false  // Always create as private by default
        })
      });

      const data = await response.json();
      if (response.status === 401) {
        // Authentication required
        alert(data.message || 'Please sign in to create stories.');
        setShowLogin(true);
      } else if (data.success) {
        await fetchStories();
        setMessages([]);
        setCurrentView('stories');
        alert('Story created successfully!');
      } else {
        alert('Failed to create story. Please try again.');
      }
    } catch (error) {
      console.error('Error creating story:', error);
      alert('Error creating story. Please try again.');
    }
    setIsLoading(false);
  };

  // Extract song title from content
  const extractSongTitle = (content) => {
    // Safety check - ensure content is a string
    if (!content || typeof content !== 'string') {
      return 'Generated Song'; // Generic fallback
    }
    
    // Look for "TITLE: 'Song Name'" or "TITLE: "Song Name""
    const titleMatch = content.match(/TITLE:\s*['"]([^'"]+)['"]/i);
    if (titleMatch) {
      return titleMatch[1];
    }
    
    // Look for title without quotes: "TITLE: Song Name"
    const titleMatch2 = content.match(/TITLE:\s*([^\n]+)/i);
    if (titleMatch2) {
      return titleMatch2[1].trim();
    }
    
    // Check if content starts with a potential title (short line, not lyrics)
    const lines = content.split('\n').filter(line => line.trim());
    const firstLine = lines[0]?.trim();
    
    // Avoid using lyrics as titles (they usually start with common words)
    const lyricStarters = ['walking', 'got this', 'man i', 'verse', 'chorus', 'bridge', '♪', 'i was', 'there was', 'in the'];
    const isLyric = lyricStarters.some(starter => 
      firstLine?.toLowerCase().startsWith(starter.toLowerCase())
    );
    
    // If first line looks like a title (short, not lyrics), use it
    if (firstLine && !isLyric && firstLine.length < 60 && !firstLine.includes(',') && !firstLine.includes('.')) {
      return firstLine;
    }
    
    // Look for patterns like "Song about..." or "A song about..."
    const aboutMatch = content.match(/(?:song about|a song about)\s+([^\n\.]{10,50})/i);
    if (aboutMatch) {
      return aboutMatch[1].trim();
    }
    
    // Try to extract meaningful words from the content to create a title
    const meaningfulWords = content
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 3 && !['this', 'that', 'with', 'from', 'they', 'them', 'were', 'have', 'been', 'will', 'would', 'could', 'should'].includes(word.toLowerCase()))
      .slice(0, 3);
    
    if (meaningfulWords.length >= 2) {
      return meaningfulWords.join(' ');
    }
    
    return 'Generated Song'; // Generic fallback
  };

  // Audio upload function
  const uploadAudio = async (file, storyId, formatType) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('story_id', storyId);
    formData.append('format_type', formatType);
    
    const response = await fetch('/api/upload/audio', {
      method: 'POST',
      body: formData
    });
    
    return response.json();
  };

  // Format viewing functions
  const viewFormat = async (story, formatType) => {
    setLoadingFormat(true);
          setCurrentFormat({ story, formatType, title: null });
    setCurrentView('format-detail');
    
    try {
      // First check if format content is already in story data
      if (story.formats && story.formats[formatType]) {
        setFormatContent(story.formats[formatType]);
        // Extract title for song format from local data
        if (formatType === 'song') {
          const contentText = typeof story.formats[formatType] === 'object' ? story.formats[formatType].content || '' : story.formats[formatType] || '';
          // Prioritize database title over extraction
          const databaseTitle = typeof story.formats[formatType] === 'object' ? story.formats[formatType].title : null;
          const title = databaseTitle || extractSongTitle(contentText);
          const audioUrl = typeof story.formats[formatType] === 'object' ? story.formats[formatType].audio_url : null;
          setCurrentFormat(prev => ({...prev, title, audio_url: audioUrl}));
        }
        setLoadingFormat(false);
        return;
      }

      // Otherwise fetch from API
      const response = await fetch(`/api/stories/${story.id}/formats/${formatType}`);
      if (response.ok) {
        const data = await response.json();
        setFormatContent(data.content);
        // Extract title for song format
        if (formatType === 'song') {
          const contentText = typeof data.content === 'object' ? data.content.content || '' : data.content || '';
          const title = data.title || extractSongTitle(contentText);
          const audioUrl = data.audio_url || (typeof data.content === 'object' ? data.content.audio_url : null);
          setCurrentFormat(prev => ({...prev, title, audio_url: audioUrl}));
        }
      } else {
        // Format doesn't exist, try to generate it
        const generateResponse = await fetch(`/api/stories/${story.id}/generate-format`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ format_type: formatType })
        });
        
        if (generateResponse.ok) {
          const generateData = await generateResponse.json();
          setFormatContent(generateData.content);
          // Extract title for song format
          if (formatType === 'song' && generateData.title) {
            setCurrentFormat(prev => ({...prev, title: generateData.title}));
          }
        } else {
          setFormatContent('Error loading format. Please try again.');
        }
      }
    } catch (error) {
      console.error('Error viewing format:', error);
      setFormatContent('Error loading format. Please try again.');
    } finally {
      setLoadingFormat(false);
    }
  };

  // Toggle story privacy
  const toggleStoryPrivacy = async (storyId, currentIsPublic) => {
    if (!user || !user.id) {
      setShowLogin(true);
      return;
    }
    
    try {
      const response = await fetch(`/api/stories/${storyId}/privacy`, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json',
          'X-User-ID': user.id
        },
        body: JSON.stringify({
          is_public: !currentIsPublic
        })
      });

      const data = await response.json();
      
      if (response.ok) {
        // Update the story in our local state
        setStories(prev => prev.map(story => 
          story.id === storyId 
            ? { ...story, public: data.is_public, privacy: data.is_public ? 'public' : 'private' }
            : story
        ));
        
        // Show success message
        alert(data.message || `Story is now ${data.is_public ? 'public' : 'private'}`);
      } else {
        alert(data.message || 'Failed to update privacy settings');
      }
    } catch (error) {
      console.error('Error updating story privacy:', error);
      alert('Failed to update privacy settings');
    }
  };

  // UI Components
  const renderNavbar = () => (
    <nav className="bg-white border-b border-gray-200 px-4 py-2 sticky top-0 z-50">
      <div className="max-width-full flex items-center justify-between">
        <div className="flex items-center gap-6">
          <a href="#" className="text-xl font-bold text-purple-600 no-underline">
            Sentimental
          </a>
          
          <div className="hidden md:flex items-center gap-1">
            {[
              { id: 'discover', label: 'Discover', icon: Search },
              { id: 'share', label: 'Share', icon: MessageCircle },
              { id: 'stories', label: 'Stories', icon: BookOpen }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setCurrentView(tab.id)}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  currentView === tab.id 
                    ? 'bg-purple-100 text-purple-700' 
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                }`}
              >
                <tab.icon />
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-3">
          {user ? (
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                {user.photoURL ? (
                  <img 
                    src={user.photoURL} 
                    alt={user.name}
                    className="w-8 h-8 rounded-full border border-gray-200"
                  />
                ) : (
                  <div className="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-semibold">
                      {user.name?.[0]?.toUpperCase() || 'U'}
                    </span>
                  </div>
                )}
                <span className="hidden md:block text-sm font-medium text-gray-700">
                  {user.name}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="text-sm text-gray-500 hover:text-gray-700 px-3 py-1 rounded-lg hover:bg-gray-100 transition-colors"
              >
                Logout
              </button>
            </div>
          ) : (
            <button
              onClick={() => setShowLogin(true)}
              className="bg-purple-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-purple-700 transition-colors"
            >
              Login
            </button>
          )}
        </div>
      </div>
    </nav>
  );

  const renderLoginModal = () => {
    if (!showLogin) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-2xl max-w-md w-full p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-gray-900">
              {isSignupMode ? 'Create Account' : 'Welcome Back'}
            </h2>
            <button 
              onClick={() => {
                setShowLogin(false);
                setIsSignupMode(false);
                setLoginForm({ name: '', email: '', password: '' });
              }}
              className="text-gray-400 hover:text-gray-600"
            >
              <X />
            </button>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            {isSignupMode && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  value={loginForm.name}
                  onChange={(e) => setLoginForm({...loginForm, name: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="Your name"
                  required={isSignupMode}
                />
              </div>
            )}
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                value={loginForm.email}
                onChange={(e) => setLoginForm({...loginForm, email: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="your@email.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <input
                type="password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Enter your password"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-purple-600 text-white py-3 rounded-lg font-medium hover:bg-purple-700 transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Please wait...' : (isSignupMode ? 'Create Account' : 'Sign In')}
            </button>
          </form>

          <div className="mt-4 text-center">
            <button
              onClick={() => {
                setIsSignupMode(!isSignupMode);
                setLoginForm({ name: '', email: '', password: '' });
              }}
              className="text-purple-600 hover:text-purple-700 text-sm font-medium"
            >
              {isSignupMode ? 'Already have an account? Sign in' : 'Need an account? Sign up'}
            </button>
          </div>

          <div className="my-4 flex items-center">
            <div className="flex-1 border-t border-gray-300"></div>
            <span className="px-4 text-sm text-gray-500">or</span>
            <div className="flex-1 border-t border-gray-300"></div>
          </div>

          <button
            onClick={handleGoogleAuth}
            disabled={isLoading}
            className="w-full bg-white border border-gray-300 text-gray-700 py-3 px-4 rounded-lg font-medium hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 shadow-sm"
          >
            {isLoading ? (
              <>
                <div className="w-5 h-5 border-2 border-gray-400 border-t-transparent rounded-full animate-spin"></div>
                Signing in...
              </>
            ) : (
              <>
                <svg width="20" height="20" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Continue with Google
              </>
            )}
          </button>
        </div>
      </div>
    );
  };

  // Discover Page with beautiful story cards
  const renderDiscover = () => (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Discover Stories</h1>
        <p className="text-lg text-gray-600">Beautiful stories from real people around the world</p>
      </div>

      {loadingFormat ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
        </div>
      ) : (
        <div className="grid gap-6">
          {stories.map(story => (
            <div key={story.id} className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-all duration-200">
              {/* Story Header */}
              <div className="p-6 pb-4">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold text-sm">
                      {story.author?.[0]?.toUpperCase() || 'U'}
                    </span>
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">{story.author || 'Anonymous'}</p>
                    <p className="text-sm text-gray-500">
                      {story.timestamp ? new Date(story.timestamp).toLocaleDateString() : '1 day ago'}
                    </p>
                  </div>
                </div>

                <h2 className="text-xl font-bold text-gray-900 mb-3 leading-tight">{story.title}</h2>
                
                <div className="bg-gray-50 rounded-xl p-4 mb-4">
                  <p className="text-gray-700 leading-relaxed">
                    {story.content?.substring(0, 200)}
                    {story.content?.length > 200 && '...'}
                  </p>
                </div>

                {/* Format Tags */}
                {story.createdFormats && story.createdFormats.length > 0 && (
                  <div className="mb-4 p-3 bg-purple-50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Sparkles />
                      <span className="text-sm font-medium text-purple-700">Available formats:</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {story.createdFormats.map(format => (
                        <span key={format} className="inline-flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-700 rounded-md text-xs font-medium">
                          {getFormatIcon(format)} {getFormatDisplayName(format)}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="flex items-center justify-end pt-4 border-t border-gray-100">
                  <button 
                    onClick={() => {
                      setSelectedStory(story);
                      setPreviousView('discover');
                      setCurrentView('story-detail');
                    }}
                    className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium"
                  >
                    Read Story
                  </button>
                </div>
              </div>
            </div>
          ))}
          
          {stories.length === 0 && (
            <div className="text-center py-12 bg-white rounded-2xl border border-gray-200">
              <div className="text-6xl mb-4">📚</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">No stories to discover yet</h3>
              <p className="text-gray-600 mb-6">Be the first to share your story!</p>
              <button 
                onClick={() => setCurrentView('share')}
                className="px-6 py-3 bg-purple-600 text-white rounded-xl hover:bg-purple-700 transition-all font-medium"
              >
                Share Your Story
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );

  // Share Page - Chat Interface
  const renderShare = () => (
    <div className="flex flex-col min-h-[calc(100vh-4rem)] md:min-h-[calc(100vh-5rem)]">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4 flex-shrink-0">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">Create Viral Content</h1>
            <p className="text-sm text-gray-600">Turn your conversations into songs, movies & more</p>
          </div>
          
          {messages.length > 0 && (
            <button
              onClick={createStoryFromConversation}
              disabled={isLoading}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Creating...
                </>
              ) : (
                <>
                  <Plus size={16} />
                  Create Story
                </>
              )}
            </button>
          )}
        </div>
      </div>

      {/* Chat Container */}
      <div className="flex-1 max-w-4xl mx-auto w-full flex flex-col min-h-0">
        {/* Messages - Scrollable area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 min-h-0">
          {messages.length === 0 ? (
            <div className="text-center py-12">
              {!user || !user.id || user.id === 'anonymous' || user.id === 'anonymous_user' || user.id === '' || user.id === 'null' || user.id === 'undefined' ? (
                // Show authentication required for unauthenticated users
                <>
                  <div className="w-16 h-16 bg-gradient-to-br from-gray-400 to-gray-500 rounded-full flex items-center justify-center mx-auto mb-6">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                    </svg>
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Sign In to Share Your Story</h2>
                  <p className="text-gray-600 mb-8 max-w-lg mx-auto">
                    Create an account to start meaningful conversations with your AI companion 
                    and transform your experiences into beautiful, shareable stories.
                  </p>
                  <div className="space-y-3 max-w-sm mx-auto">
                    <button
                      onClick={() => setShowLogin(true)}
                      className="w-full bg-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-purple-700 transition-colors"
                    >
                      Sign In to Start Chatting
                    </button>
                    <p className="text-gray-500 text-sm">
                      Join thousands creating their personal story collections
                    </p>
                  </div>
                </>
              ) : (
                // Show normal welcome for authenticated users
                <>
                  <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6">
                    <MessageCircle />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Turn Your Life Into Viral Content! 🎵🎬</h2>
                  <p className="text-gray-600 mb-4 max-w-lg mx-auto">
                    Share your dreams, achievements, or wild moments with me and I'll help you turn them into:
                  </p>
                  <div className="flex flex-wrap justify-center gap-3 mb-6">
                    <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm font-medium">🎵 Songs</span>
                    <span className="bg-pink-100 text-pink-700 px-3 py-1 rounded-full text-sm font-medium">🎬 Movie Scripts</span>
                    <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium">📖 Stories</span>
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium">🎪 Poems</span>
                  </div>
                  <p className="text-gray-600 mb-6 max-w-lg mx-auto text-sm">
                    Tell me about your startup idea, that crazy trip, your grind story, or literally anything that excites you!
                  </p>
                </>
              )}
            </div>
          ) : (
            <>
              {messages.map((msg, index) => (
                <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] p-4 rounded-2xl ${
                    msg.role === 'user' 
                      ? 'bg-purple-600 text-white' 
                      : 'bg-gray-100 text-gray-900'
                  }`}>
                    {msg.content}
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 p-4 rounded-2xl">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
        
        {/* Input - Fixed at bottom */}
        <div className="border-t bg-white p-4 flex-shrink-0">
          {user && user.id && user.id !== 'anonymous' && user.id !== 'anonymous_user' && user.id !== '' && user.id !== 'null' && user.id !== 'undefined' && (
            // Show normal chat input for authenticated users
            <div className="flex gap-3">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type your message..."
                className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500"
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={isLoading || !message.trim()}
                className="bg-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Send
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  // Stories Page
  const renderStories = () => {
    // Require authentication for stories
    if (!user || !user.id || user.id === 'anonymous' || user.id === 'anonymous_user' || user.id === '' || user.id === 'null' || user.id === 'undefined') {
      return (
        <div className="p-6">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">My Stories</h1>
            <p className="text-lg text-gray-600">Your personal collection of stories</p>
          </div>
          
          <div className="text-center py-12">
            <div className="text-6xl mb-4">👤</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Sign in to see your stories</h3>
            <p className="text-gray-600 mb-6">Create an account to save and access your personalized stories.</p>
            <button
              onClick={() => setShowLogin(true)}
              className="bg-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-purple-700 transition-colors"
            >
              Sign In
            </button>
          </div>
        </div>
      );
    }

    // Filter stories for authenticated user only
    const userStories = stories.filter(story => story.user_id === user.id);

    return (
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">My Stories</h1>
          <p className="text-lg text-gray-600">Your personal collection of stories</p>
        </div>

        {userStories.length > 0 ? (
          <div className="grid gap-6">
            {userStories.map((story) => (
              <div
                key={story.id}
                className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow cursor-pointer border border-gray-100 p-6"
                onClick={() => {
                  setSelectedStory(story);
                  setPreviousView('stories');
                  setCurrentView('story-detail');
                }}
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold text-sm">
                      {story.author?.[0]?.toUpperCase() || 'U'}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{story.author || 'Anonymous'}</p>
                    <p className="text-sm text-gray-500">
                      {story.timestamp ? new Date(story.timestamp).toLocaleDateString() : '1 day ago'}
                    </p>
                  </div>
                </div>

                <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                  {story.title}
                </h3>
                
                <p className="text-gray-600 text-sm line-clamp-3 mb-4">
                  {story.content}
                </p>

                {/* Privacy toggle and formats */}
                <div className="flex items-center justify-between mt-4">
                  <div className="flex items-center gap-2">
                    {/* Privacy Toggle */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleStoryPrivacy(story.id, story.public);
                      }}
                      className={`text-xs px-3 py-1 rounded-full border transition-colors ${
                        story.public 
                          ? 'bg-green-100 text-green-700 border-green-200' 
                          : 'bg-gray-100 text-gray-700 border-gray-200'
                      }`}
                    >
                      {story.public ? '🌍 Public' : '🔒 Private'}
                    </button>
                    
                    {/* Available formats */}
                    {story.createdFormats && story.createdFormats.length > 0 && (
                      <>
                        <span className="text-xs text-purple-600 font-medium">•</span>
                        {story.createdFormats.slice(0, 2).map(format => (
                          <span key={format} className="bg-purple-100 text-purple-700 px-2 py-1 rounded-full text-xs">
                            {getFormatDisplayName(format)}
                          </span>
                        ))}
                        {story.createdFormats.length > 2 && (
                          <span className="text-xs text-gray-500">+{story.createdFormats.length - 2} more</span>
                        )}
                      </>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <BookOpen className="mx-auto mb-4 text-gray-400" size={48} />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No stories yet</h3>
            <p className="text-gray-600 mb-6">Chat with your AI companion to create personalized stories.</p>
            <button
              onClick={() => setCurrentView('share')}
              className="bg-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-purple-700 transition-colors"
            >
              Start Chatting
            </button>
          </div>
        )}
      </div>
    );
  };

  // Story Detail View
  const renderStoryDetail = () => {
    if (!selectedStory) return null;

    return (
      <div className="p-6">
        <div className="mb-6">
          <button
            onClick={() => setCurrentView(previousView || 'discover')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft />
            Back
          </button>
          
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                <span className="text-white font-semibold">
                  {selectedStory.author?.[0]?.toUpperCase() || 'U'}
                </span>
              </div>
              <div>
                <p className="font-semibold text-gray-900 text-lg">{selectedStory.author || 'Anonymous'}</p>
                <p className="text-gray-500">
                  {selectedStory.timestamp ? new Date(selectedStory.timestamp).toLocaleDateString() : '1 day ago'}
                </p>
              </div>
            </div>

            <h1 className="text-3xl font-bold text-gray-900 mb-6">{selectedStory.title}</h1>
            
            <div className="prose max-w-none">
              <p className="text-gray-700 leading-relaxed text-lg whitespace-pre-wrap">
                {selectedStory.content}
              </p>
            </div>

            {/* Format Buttons */}
            {selectedStory.createdFormats && selectedStory.createdFormats.length > 0 && (
              <div className="mt-8 p-4 bg-purple-50 rounded-xl">
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles />
                  <span className="font-medium text-purple-700">Available formats:</span>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {selectedStory.createdFormats.map(format => (
                    <button 
                      key={format} 
                      onClick={() => viewFormat(selectedStory, format)}
                      className="bg-purple-100 text-purple-700 rounded-lg p-3 text-center hover:bg-purple-200 transition-colors cursor-pointer border-none"
                    >
                      <div className="text-2xl mb-1">{getFormatIcon(format)}</div>
                      <div className="text-sm font-medium">{getFormatDisplayName(format)}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  // Get format display name
  const getFormatDisplayName = (formatType) => {
    const displayNames = {
      script: 'Reel',
      video: 'Reel', 
      tiktok_script: 'TikTok Reel',
      instagram_reel: 'Instagram Reel',
      // Add other custom names as needed
    };
    
    const displayName = displayNames[formatType] || formatType.replace('_', ' ');
    return displayName.replace(/\b\w/g, l => l.toUpperCase());
  };

  // Format Detail View
  const renderFormatDetail = () => {
    if (!currentFormat) return null;

    // Special designs for different format types
    const renderFormatContent = () => {
      if (currentFormat.formatType === 'song') {
        const contentText = typeof formatContent === 'object' ? formatContent.content || '' : formatContent || '';
        
        // Priority: database title > extracted title > generic fallback
        let songTitle = 'Generated Song';
        if (currentFormat.title && currentFormat.title !== 'Default Title') {
          songTitle = currentFormat.title;
        } else {
          const extractedTitle = extractSongTitle(contentText);
          if (extractedTitle && extractedTitle !== 'Generated Song') {
            songTitle = extractedTitle;
          }
        }
        
        // Clean content: remove TITLE: line since we show it separately
        let cleanContent = contentText;
        if (cleanContent) {
          cleanContent = cleanContent.replace(/^TITLE:\s*['""]([^'""]+)['""]?\s*\n?/i, '');
          cleanContent = cleanContent.replace(/^TITLE:\s*([^\n]+)\s*\n?/i, '');
          cleanContent = cleanContent.trim();
        }
        
        // Try to get audio URL from multiple sources
        const audioUrl = currentFormat.audio_url || (typeof formatContent === 'object' ? formatContent.audio_url : null);
        const hasAudio = audioUrl;
        
        return (
          <div className="bg-gradient-to-r from-pink-500 to-purple-600 rounded-xl p-6 text-white">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="text-3xl">🎵</div>
                <div>
                  <h2 className="text-xl font-semibold">{songTitle}</h2>
                  <p className="text-sm opacity-90">Based on: {currentFormat.story.title}</p>
                </div>
              </div>
              
              {/* Admin Upload Button */}
              {(user?.email === 'admin@sentimental.com' || user?.id === 'admin' || user?.name === 'Admin' || user?.name?.includes('Admin') || user?.email?.includes('admin')) && (
                <button
                  onClick={() => setShowUploadModal(true)}
                  className="mr-2 px-3 py-1 bg-white/20 rounded-lg text-xs hover:bg-white/30 transition-colors"
                >
                  Upload MP3
                </button>
              )}
            </div>
            
            {/* Audio Player */}
            {hasAudio ? (
              <div className="bg-black/20 rounded-lg p-4 mb-4">
                <audio 
                  controls 
                  className="w-full"
                  onError={(e) => console.error('Audio error:', e, 'URL:', audioUrl)}
                  onCanPlay={() => console.log('Audio can play:', audioUrl)}
                >
                  <source src={audioUrl} type="audio/mpeg" />
                  Your browser does not support the audio element.
                </audio>
              </div>
            ) : (
              <div className="bg-black/20 rounded-lg p-4 mb-4">
                <div className="flex items-center justify-between text-sm mb-2">
                  <span>🎧 Music Player</span>
                  {(user?.email === 'admin@sentimental.com' || user?.id === 'admin' || user?.name === 'Admin' || user?.name?.includes('Admin') || user?.email?.includes('admin')) && (
                    <button 
                      onClick={() => setShowUploadModal(true)}
                      className="bg-white/20 hover:bg-white/30 px-2 py-1 rounded text-xs transition-colors"
                    >
                      Upload MP3
                    </button>
                  )}
                </div>
                <div className="w-full bg-white/20 rounded-full h-2">
                  <div className="bg-white/50 h-2 rounded-full w-0"></div>
                </div>
                {(user?.email === 'admin@sentimental.com' || user?.id === 'admin' || user?.name === 'Admin' || user?.name?.includes('Admin') || user?.email?.includes('admin')) ? (
                  <div className="text-xs text-center mt-2 opacity-75">Click "Upload MP3" to add audio</div>
                ) : (
                  <div className="text-xs text-center mt-2 opacity-75">Audio coming soon...</div>
                )}
              </div>
            )}

            <div className="prose prose-invert max-w-none">
              <pre className="whitespace-pre-wrap font-sans leading-relaxed text-sm">
                {cleanContent || contentText}
              </pre>
            </div>
            
            {(user?.email === 'admin@sentimental.com' || user?.id === 'admin' || user?.name === 'Admin' || user?.name?.includes('Admin') || user?.email?.includes('admin')) && (
              <div className="mt-4 text-xs opacity-75">
                {hasAudio ? 
                  '🎵 Music ready to play!' : 
                  '🎧 Upload MP3 file to enable playback'
                }
              </div>
            )}
          </div>
        );
      }
      
      if (currentFormat.formatType === 'script' || currentFormat.formatType === 'video' || currentFormat.formatType.includes('reel')) {
        return (
          <div className="bg-gray-900 rounded-xl overflow-hidden">
            <div className="aspect-video bg-gradient-to-br from-gray-800 to-gray-900 relative flex items-center justify-center">
              <button className="w-16 h-16 bg-white/90 rounded-full flex items-center justify-center hover:bg-white transition-colors group">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" className="text-gray-900 ml-1">
                  <polygon points="5 3 19 12 5 21 5 3"/>
                </svg>
              </button>
              <div className="absolute bottom-4 left-4 text-white">
                <p className="font-semibold text-sm">{getFormatDisplayName(currentFormat.formatType)}: {currentFormat.story.title}</p>
                <p className="text-xs opacity-75">60s • Ready for Veo3 generation</p>
              </div>
            </div>
            
            <div className="p-6 bg-white">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Video Script</h3>
              <div className="prose max-w-none">
                <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed text-sm">
                  {typeof formatContent === 'object' ? formatContent.content || JSON.stringify(formatContent, null, 2) : formatContent}
                </pre>
              </div>
              <div className="mt-4 text-xs text-gray-500">
                📹 This script will be used to generate the reel automatically
              </div>
            </div>
          </div>
        );
      }

      // Default format display
      return (
        <div className="prose max-w-none">
          <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed text-lg">
            {typeof formatContent === 'object' ? formatContent.content || JSON.stringify(formatContent, null, 2) : formatContent}
          </pre>
        </div>
      );
    };

    return (
      <div className="p-6">
        <div className="mb-6">
          <button
            onClick={() => {
              setCurrentView('story-detail');
              setCurrentFormat(null);
              setFormatContent('');
            }}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft />
            Back to Story
          </button>
          
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center gap-3">
                <div className="text-3xl">{getFormatIcon(currentFormat.formatType)}</div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    {currentFormat.formatType === 'song' ? (
                      currentFormat.title && currentFormat.title !== 'Default Title' ? 
                        currentFormat.title : 
                        extractSongTitle(typeof formatContent === 'object' ? formatContent.content || '' : formatContent || '') || getFormatDisplayName(currentFormat.formatType)
                    ) : getFormatDisplayName(currentFormat.formatType)}
                  </h1>
                  <p className="text-gray-600">{currentFormat.story.title}</p>
                </div>
              </div>
            </div>

            <div className="p-6">
              {loadingFormat ? (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
                  <span className="ml-3 text-gray-600">Loading format...</span>
                </div>
              ) : (
                renderFormatContent()
              )}
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Upload Modal Component
  const renderUploadModal = () => {
    if (!showUploadModal) return null;

    const handleFileUpload = async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      if (!file.type.startsWith('audio/')) {
        alert('Please select an audio file (MP3, WAV, etc.)');
        return;
      }

      setUploadingAudio(true);
      try {
        const result = await uploadAudio(file, currentFormat.story.id, currentFormat.formatType);
        if (result.success) {
          // Update current format with audio URL
          setCurrentFormat(prev => ({...prev, audio_url: result.audio_url}));
          setShowUploadModal(false);
          alert('Audio uploaded successfully! 🎵');
        } else {
          alert('Upload failed: ' + (result.error || 'Unknown error'));
        }
      } catch (error) {
        console.error('Upload error:', error);
        alert('Upload failed. Please try again.');
      }
      setUploadingAudio(false);
    };

    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Upload Audio File</h3>
            <button
              onClick={() => setShowUploadModal(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              <X />
            </button>
          </div>
          
          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">
              Upload an MP3 file for: <strong>{currentFormat?.title || 'Song'}</strong>
            </p>
            <p className="text-xs text-gray-500">
              Supported formats: MP3, WAV, OGG, M4A (Max 16MB)
            </p>
          </div>

          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
            {uploadingAudio ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-600"></div>
                <span className="ml-2 text-gray-600">Uploading...</span>
              </div>
            ) : (
              <>
                <div className="text-4xl mb-2">🎵</div>
                <p className="text-gray-600 mb-2">Choose audio file</p>
                <input
                  type="file"
                  accept="audio/*"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="audio-upload"
                />
                <label
                  htmlFor="audio-upload"
                  className="inline-block px-4 py-2 bg-purple-600 text-white rounded-lg cursor-pointer hover:bg-purple-700 transition-colors"
                >
                  Select File
                </label>
              </>
            )}
          </div>
        </div>
      </div>
    );
  };

  // Main Render Logic
  const renderMainContent = () => {
    switch(currentView) {
      case 'discover': return renderDiscover();
      case 'share': return renderShare();
      case 'stories': return renderStories();
      case 'story-detail': return renderStoryDetail();
      case 'format-detail': return renderFormatDetail();
      default: return renderDiscover();
    }
  };

  // Mobile Footer Navigation
  const renderMobileFooter = () => (
    <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
      <div className="flex items-center justify-around py-2">
        {[
          { 
            id: 'discover', 
            label: 'Discover', 
            icon: () => (
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
              </svg>
            )
          },
          { 
            id: 'share', 
            label: 'Share', 
            icon: () => (
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
              </svg>
            )
          },
          { 
            id: 'stories', 
            label: 'Stories', 
            icon: () => (
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
              </svg>
            )
          },
          { 
            id: 'inner-space', 
            label: 'Space', 
            icon: () => (
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <polygon points="16.24,7.76 14.12,14.12 7.76,16.24 9.88,9.88"/>
              </svg>
            )
          }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => {
              if (tab.id === 'inner-space') {
                alert('🚀 Inner Space is coming soon! A personal dashboard for deeper insights into your stories and patterns.');
              } else {
                setCurrentView(tab.id);
              }
            }}
            className={`flex flex-col items-center gap-1 px-3 py-2 rounded-lg transition-colors ${
              currentView === tab.id 
                ? 'text-purple-600' 
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <div className={`${currentView === tab.id ? 'text-purple-600' : 'text-gray-500'}`}>
              <tab.icon />
            </div>
            <span className="text-xs font-medium">{tab.label}</span>
          </button>
        ))}
      </div>
    </div>
  );

  // Don't render anything until app is initialized to prevent flashing
  if (!appInitialized) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {renderNavbar()}
      {renderLoginModal()}
      {renderUploadModal()}
      
      {/* Main Content with bottom padding on mobile for footer */}
      <div className="max-w-6xl mx-auto pb-20 md:pb-0">
        {renderMainContent()}
      </div>

      {/* Mobile Footer Navigation */}
      {renderMobileFooter()}
    </div>
  );
};

// Make it available globally
window.SentimentalApp = SentimentalApp;