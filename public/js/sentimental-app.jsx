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

const InnerSpace = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <polygon points="16.24,7.76 14.12,14.12 7.76,16.24 9.88,9.88"/>
  </svg>
);

const Globe = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 12.79A9 9 0 1 1 12 3a9 9 0 0 1 9 9 9.71 9.71 0 0 1-.79 4.21M17 21H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5z"/>
  </svg>
);

const ChevronRight = ({ size = 16, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="M9 18l6-6-6-6"/>
  </svg>
);

const Edit = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
    <path d="m18.5 2.5 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
  </svg>
);

const Lock = ({ size = 16 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
    <circle cx="12" cy="16" r="1"></circle>
    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
  </svg>
);

// Format icons
const getFormatIcon = (formatType) => {
  const icons = {
    // Social Media Formats (4)
    x: '🐦',
    linkedin: '💼', 
    instagram: '📸',
    facebook: '👥',
    
    // Creative Formats (4)
    poem: '🎭',
    song: '🎵',
    reel: '📄',
    fairytale: '📚',
    
    // Professional Formats (5)
    article: '📝',
    blog_post: '✍️',
    presentation: '📊',
    newsletter: '📰',
    podcast: '📄',
    
    // Therapeutic Formats (3)
    insights: '💡',
    growth_summary: '🌱',
    journal_entry: '📔',
    
    // Modern Viral Formats
    tiktok_script: '📱',
    instagram_reel: '🎬',
    x_thread: '🧵',
    youtube_short: '▶️',
    instagram_story: '📸',
  };
  return icons[formatType] || '📄';
};

// Main App Component
const SentimentalApp = () => {
  const [currentView, setCurrentView] = useState('chat');
  const [selectedStory, setSelectedStory] = useState(null);
  const [shareModal, setShareModal] = useState(null);
  const [previousView, setPreviousView] = useState('chat');
  const [currentFormat, setCurrentFormat] = useState(null);
  const [formatContent, setFormatContent] = useState('');
  const [loadingFormat, setLoadingFormat] = useState(false);
  const [stories, setStories] = useState([]);
  const [userStories, setUserStories] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(false);
  const [supportedFormats, setSupportedFormats] = useState({});
  
  // Edit story state
  const [editingStory, setEditingStory] = useState(null);
  const [editTitle, setEditTitle] = useState('');
  const [editContent, setEditContent] = useState('');
  const [isUpdatingStory, setIsUpdatingStory] = useState(false);

  // Edit format state
  const [editingFormat, setEditingFormat] = useState(null);
  const [editFormatContent, setEditFormatContent] = useState('');
  const [isUpdatingFormat, setIsUpdatingFormat] = useState(false);

  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const [isSignupMode, setIsSignupMode] = useState(false);
  const [loginForm, setLoginForm] = useState({ name: '', email: '', password: '' });
  const [appInitialized, setAppInitialized] = useState(false);

  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadingAudio, setUploadingAudio] = useState(false);
  const [loadingFormats, setLoadingFormats] = useState(true);
  const [showSpaceModal, setShowSpaceModal] = useState(false);

  // Initialize
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Check if user has access - if not, redirect to landing page
        // const storedAccess = localStorage.getItem('sentimental_access');
        // if (storedAccess !== 'granted') {
        //   window.location.href = '/';
        //   return;
        // }
        
        // Load initial data
        await Promise.all([
          fetchStories(),
          fetchSupportedFormats()
        ]);
        
        // Check for existing user session
        const savedUser = localStorage.getItem('sentimental_user');
        if (savedUser) {
          try {
            const parsedUser = JSON.parse(savedUser);
            console.log('Found saved user:', parsedUser);
            
            // Validate stored user ID
            if (parsedUser.id && 
                parsedUser.id !== 'anonymous' && 
                parsedUser.id !== 'anonymous_user' && 
                parsedUser.id !== '' && 
                parsedUser.id !== 'null' && 
                parsedUser.id !== 'undefined') {
              setUser(parsedUser);
              console.log('Using valid saved user:', parsedUser.id);
            } else {
              console.warn('Saved user has invalid ID, clearing:', parsedUser.id);
              localStorage.removeItem('sentimental_user');
            }
          } catch (e) {
            console.error('Error parsing saved user:', e);
            localStorage.removeItem('sentimental_user');
          }
        }

        // Set up Firebase auth state listener
        const unsubscribe = window.firebaseAuth?.onAuthStateChanged(async (firebaseUser) => {
          if (firebaseUser) {
            // Sync with backend to get proper user ID
            try {
              const syncResponse = await fetch('/api/auth/firebase-sync', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  uid: firebaseUser.uid,
                  email: firebaseUser.email,
                  name: firebaseUser.displayName || firebaseUser.email.split('@')[0],
                  emailVerified: firebaseUser.emailVerified,
                  provider: 'google'
                })
              });
              
              if (syncResponse.ok) {
                const syncData = await syncResponse.json();
                const userData = {
                  id: syncData.user_id, // Use backend user ID
                  email: syncData.email,
                  name: syncData.name,
                  emailVerified: firebaseUser.emailVerified,
                  photoURL: firebaseUser.photoURL
                };
                
                console.log('Firebase user synced with backend:', userData);
                setUser(userData);
                localStorage.setItem('sentimental_user', JSON.stringify(userData));
              } else {
                console.error('Failed to sync Firebase user with backend');
                // Fallback to Firebase data
                const userData = {
                  id: firebaseUser.uid,
                  email: firebaseUser.email,
                  name: firebaseUser.displayName || firebaseUser.email.split('@')[0],
                  emailVerified: firebaseUser.emailVerified,
                  photoURL: firebaseUser.photoURL
                };
                
                setUser(userData);
                localStorage.setItem('sentimental_user', JSON.stringify(userData));
              }
            } catch (error) {
              console.error('Error syncing Firebase user:', error);
              // Fallback to Firebase data
              const userData = {
                id: firebaseUser.uid,
                email: firebaseUser.email,
                name: firebaseUser.displayName || firebaseUser.email.split('@')[0],
                emailVerified: firebaseUser.emailVerified,
                photoURL: firebaseUser.photoURL
              };
              
              setUser(userData);
              localStorage.setItem('sentimental_user', JSON.stringify(userData));
            }
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

  const fetchSupportedFormats = async () => {
    try {
      setLoadingFormats(true);
      const response = await fetch(`/api/formats/supported?t=${Date.now()}`);
      if (response.ok) {
        const data = await response.json();
        setSupportedFormats(data.supported_formats || []);
        console.log('Loaded supported formats:', data.supported_formats);
      } else {
        console.error('Failed to fetch supported formats, using fallback');
        // Fallback to formats that are actually supported by prompts engine
        setSupportedFormats([
          'x', 'linkedin', 'instagram', 'facebook',
          'poem', 'song', 'reel', 'fairytale', 
          'article', 'blog_post', 'presentation', 'newsletter', 'podcast',
          'insights', 'growth_summary', 'journal_entry'
        ]);
      }
    } catch (error) {
      console.error('Error fetching supported formats:', error);
      // Fallback to core formats that definitely work
      setSupportedFormats([
        'x', 'linkedin', 'instagram', 'poem', 'song', 'article', 'insights'
      ]);
    } finally {
      setLoadingFormats(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      if (isSignupMode) {
        // Try Firebase signup first if available
        if (window.firebaseAuth) {
          try {
            const userCredential = await window.firebaseAuth.createUserWithEmailAndPassword(loginForm.email, loginForm.password);
            const firebaseUser = userCredential.user;
            
            // Update display name
            if (loginForm.name) {
              await firebaseUser.updateProfile({
                displayName: loginForm.name
              });
            }
            
            // User will be synced automatically by auth state listener
            setShowLogin(false);
            return;
          } catch (firebaseError) {
            console.log('Firebase signup failed, falling back to local registration:', firebaseError);
            // Fall through to local registration
          }
        }
        
        // Fallback: Register new user locally
        const registerResponse = await fetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            uid: `temp_${Date.now()}`,
            email: loginForm.email,
            name: loginForm.name,
            emailVerified: false,
            provider: 'email'
          })
        });

        const registerData = await registerResponse.json();
        if (registerResponse.ok) {
          const newUser = {
            id: registerData.user_id,
            email: registerData.email,
            name: registerData.name
          };
          
          console.log('User registered successfully:', newUser);
          
          // Validate user ID
          if (!newUser.id || newUser.id === 'anonymous' || newUser.id === 'anonymous_user' || newUser.id === '' || newUser.id === 'null' || newUser.id === 'undefined') {
            console.error('Invalid user ID received:', newUser.id);
            alert('Registration failed: Invalid user ID received. Please try again.');
            return;
          }
          
          setUser(newUser);
          localStorage.setItem('sentimental_user', JSON.stringify(newUser));
          setShowLogin(false);
          await fetchStories();
        } else {
          alert(registerData.message || 'Registration failed. Please try again.');
        }
      } else {
        // Try Firebase signin first if available
        if (window.firebaseAuth) {
          try {
            const userCredential = await window.firebaseAuth.signInWithEmailAndPassword(loginForm.email, loginForm.password);
            // User will be synced automatically by auth state listener
            setShowLogin(false);
            return;
          } catch (firebaseError) {
            console.log('Firebase signin failed, falling back to local login:', firebaseError);
            // Fall through to local login
          }
        }
        
        // Fallback: Login existing user locally
        const loginResponse = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: loginForm.email,
            password: loginForm.password || 'testpassword123'
          })
        });

        const loginData = await loginResponse.json();
        if (loginResponse.ok) {
          const loggedInUser = {
            id: loginData.user_id,
            email: loginData.email,
            name: loginData.name
          };
          
          console.log('User logged in successfully:', loggedInUser);
          
          // Validate user ID
          if (!loggedInUser.id || loggedInUser.id === 'anonymous' || loggedInUser.id === 'anonymous_user' || loggedInUser.id === '' || loggedInUser.id === 'null' || loggedInUser.id === 'undefined') {
            console.error('Invalid user ID received:', loggedInUser.id);
            alert('Login failed: Invalid user ID received. Please try again.');
            return;
          }
          
          setUser(loggedInUser);
          localStorage.setItem('sentimental_user', JSON.stringify(loggedInUser));
          setShowLogin(false);
          await fetchStories();
        } else {
          alert(loginData.message || 'Login failed. Please check your credentials.');
        }
      }
    } catch (error) {
      console.error('Authentication error:', error);
      alert('Authentication failed. Please try again.');
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

  const handleForgotPassword = async () => {
    if (!loginForm.email) {
      alert('Please enter your email address first.');
      return;
    }

    setIsLoading(true);
    try {
      if (window.firebaseAuth) {
        await window.firebaseAuth.sendPasswordResetEmail(loginForm.email);
        alert('Password reset email sent! Please check your email and follow the instructions to reset your password.');
      } else {
        // Fallback for test environment - show instructions
        alert('Password reset: Please contact support at hello@sentimental.app with your email address to reset your password.');
      }
    } catch (error) {
      console.error('Password reset error:', error);
      if (error.code === 'auth/user-not-found') {
        alert('No account found with this email address. Please check your email or create a new account.');
      } else if (error.code === 'auth/invalid-email') {
        alert('Please enter a valid email address.');
      } else {
        alert('Failed to send password reset email. Please try again or contact support.');
      }
    }
    setIsLoading(false);
  };

  const handleLogout = async () => {
    try {
      // Only sign out from Firebase if user has a Firebase UID (not demo users)
      if (window.firebaseAuth && user && !user.id.startsWith('demo_')) {
        await window.firebaseAuth.signOut();
      }
      
      // Clear user state and local storage
      setUser(null);
      setMessages([]);
      setCurrentView('discover');
      localStorage.removeItem('sentimental_user');
      
      console.log('User logged out successfully');
    } catch (error) {
      console.error('Logout error:', error);
      // Force logout even if Firebase fails
      setUser(null);
      setMessages([]);
      setCurrentView('discover');
      localStorage.removeItem('sentimental_user');
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
        headers: { 
          'Content-Type': 'application/json',
          'X-User-ID': user.id
        },
        body: JSON.stringify({
          message: userMessage,
          user_id: user.id,
          conversation_history: messages // Send the conversation history!
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
    
    // Add progress feedback
    setMessages(prev => [...prev, {
      role: 'system',
      content: '✨ Creating your story... This may take a moment.'
    }]);
    
    try {
      const response = await fetch('/api/stories/generate', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-User-ID': user.id // Add authentication header
        },
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
        // Show success feedback with progress
        setMessages(prev => [...prev, {
          role: 'system',
          content: '✨ Your story has been created successfully! You can find it in your Stories tab.'
        }]);
        await fetchStories();
        // Clean up any previous story/format state before switching to stories
        setSelectedStory(null);
        setCurrentFormat(null);
        setFormatContent('');
        setPreviousView('share');
        setCurrentView('stories');
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
    // Require authentication for file uploads
    if (!user || !user.id || user.id === 'anonymous' || user.id === 'anonymous_user' || user.id === '' || user.id === 'null' || user.id === 'undefined') {
      throw new Error('Authentication required for file uploads');
    }
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('story_id', storyId);
    formData.append('format_type', formatType);
    
    const response = await fetch('/api/upload/audio', {
      method: 'POST',
      headers: {
        'X-User-ID': user.id  // Add authentication header
      },
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
        
        // Ensure the createdFormats array includes this format
        if (!story.createdFormats || !story.createdFormats.includes(formatType)) {
          setStories(prev => prev.map(s => 
            s.id === story.id 
              ? { 
                  ...s, 
                  createdFormats: [...(s.createdFormats || []), formatType].filter((format, index, arr) => arr.indexOf(format) === index)
                }
              : s
          ));
          
          // Also update the selectedStory if it's the same story being viewed
          if (selectedStory && selectedStory.id === story.id) {
            setSelectedStory(prev => ({
              ...prev,
              createdFormats: [...(prev.createdFormats || []), formatType].filter((format, index, arr) => arr.indexOf(format) === index)
            }));
          }
        }
        
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
        
        // Update the story in local state to include the fetched format
        setStories(prev => prev.map(s => 
          s.id === story.id 
            ? { 
                ...s, 
                formats: { 
                  ...s.formats, 
                  [formatType]: data.content 
                },
                createdFormats: [...(s.createdFormats || []), formatType].filter((format, index, arr) => arr.indexOf(format) === index)
              }
            : s
        ));
        
        // Also update the selectedStory if it's the same story being viewed
        if (selectedStory && selectedStory.id === story.id) {
          setSelectedStory(prev => ({
            ...prev,
            formats: {
              ...prev.formats,
              [formatType]: data.content
            },
            createdFormats: [...(prev.createdFormats || []), formatType].filter((format, index, arr) => arr.indexOf(format) === index)
          }));
        }
        
        // Extract title for song format
        if (formatType === 'song') {
          const contentText = typeof data.content === 'object' ? data.content.content || '' : data.content || '';
          const title = data.title || extractSongTitle(contentText);
          const audioUrl = data.audio_url || (typeof data.content === 'object' ? data.content.audio_url : null);
          setCurrentFormat(prev => ({...prev, title, audio_url: audioUrl}));
        }
      } else {
        // Format doesn't exist, check authentication before trying to generate it
        if (!user || !user.id || user.id === 'anonymous' || user.id === 'anonymous_user' || user.id === '' || user.id === 'null' || user.id === 'undefined') {
          setFormatContent('This transformation has not been created yet. Please sign in to create new transformations.');
          setLoadingFormat(false);
          return;
        }
        
        console.log('Generating format for user:', user);
        console.log('User ID being sent:', user.id);
        console.log('Format type:', formatType);
        
        const generateResponse = await fetch(`/api/stories/${story.id}/generate-format`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'X-User-ID': user.id || 'undefined' // Add authentication header with fallback
          },
          body: JSON.stringify({ format_type: formatType })
        });
        
        if (generateResponse.ok) {
          const generateData = await generateResponse.json();
          setFormatContent(generateData.content);
          
          // Update the story in local state to include the new format
          setStories(prev => prev.map(s => 
            s.id === story.id 
              ? { 
                  ...s, 
                  formats: { 
                    ...s.formats, 
                    [formatType]: generateData.content 
                  },
                  createdFormats: [...(s.createdFormats || []), formatType].filter((format, index, arr) => arr.indexOf(format) === index) // Add to createdFormats and remove duplicates
                }
              : s
          ));
          
          // Also update the selectedStory if it's the same story being viewed
          if (selectedStory && selectedStory.id === story.id) {
            setSelectedStory(prev => ({
              ...prev,
              formats: {
                ...prev.formats,
                [formatType]: generateData.content
              },
              createdFormats: [...(prev.createdFormats || []), formatType].filter((format, index, arr) => arr.indexOf(format) === index)
            }));
          }
          
          // Extract title for song format
          if (formatType === 'song' && generateData.title) {
            setCurrentFormat(prev => ({...prev, title: generateData.title}));
          }
        } else {
          const errorData = await generateResponse.json().catch(() => ({}));
          console.error('Format generation failed:', {
            status: generateResponse.status,
            statusText: generateResponse.statusText,
            error: errorData,
            user: user,
            userId: user.id
          });
          
          if (generateResponse.status === 401) {
            setFormatContent(`Authentication error: ${errorData.message || 'Please sign in to transform your stories.'}\n\nDebug info: User ID = "${user.id || 'undefined'}"`);
          } else if (generateResponse.status === 403) {
                          setFormatContent(`Access denied: ${errorData.message || 'Only the story author can create additional transformations.'}\n\nThis story belongs to another user.`);
          } else {
            setFormatContent(`Error loading format (${generateResponse.status}): ${errorData.message || 'Please try again.'}`);
          }
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

  // Edit story functionality
  const startEditingStory = (story) => {
    setEditingStory(story);
    setEditTitle(story.title);
    setEditContent(story.content);
  };

  const cancelEditStory = () => {
    setEditingStory(null);
    setEditTitle('');
    setEditContent('');
  };

  const saveStoryEdit = async () => {
    if (!editingStory || !user || !user.id) {
      return;
    }

    if (!editTitle.trim() || !editContent.trim()) {
      alert('Please fill in both title and content');
      return;
    }

    setIsUpdatingStory(true);

    try {
      const response = await fetch(`/api/stories/${editingStory.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-User-ID': user.id
        },
        body: JSON.stringify({
          title: editTitle.trim(),
          content: editContent.trim()
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Update the story in local state
        setStories(prev => prev.map(story => 
          story.id === editingStory.id ? data : story
        ));
        
        // Update userStories if it exists
        setUserStories(prev => prev.map(story => 
          story.id === editingStory.id ? data : story
        ));

        // Update selectedStory if it's the one being edited
        if (selectedStory && selectedStory.id === editingStory.id) {
          setSelectedStory(data);
        }

        // Clear editing state
        cancelEditStory();
        
        alert('Story updated successfully!');
      } else {
        alert(data.message || 'Failed to update story');
      }
    } catch (error) {
      console.error('Error updating story:', error);
      alert('Failed to update story. Please try again.');
    } finally {
      setIsUpdatingStory(false);
    }
  };

  // Format editing functions
  const startEditingFormat = (format, content) => {
    setEditingFormat(format);
    const contentText = typeof content === 'object' ? content.content || content : content;
    setEditFormatContent(contentText || '');
  };

  const cancelEditFormat = () => {
    setEditingFormat(null);
    setEditFormatContent('');
  };

  const saveFormatEdit = async () => {
    if (!editingFormat || !currentFormat) return;

    setIsUpdatingFormat(true);
    try {
      const response = await fetch(`/api/stories/${currentFormat.story.id}/formats/${editingFormat.formatType}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: editFormatContent,
          user_id: user?.id
        })
      });

      if (response.ok) {
        const data = await response.json();
        
        // Update the format content in current view
        setFormatContent(editFormatContent);
        
        // Update the story's formats in local state
        setStories(prev => prev.map(story => 
          story.id === currentFormat.story.id 
            ? { 
                ...story, 
                formats: { 
                  ...story.formats, 
                  [editingFormat.formatType]: editFormatContent 
                }
              }
            : story
        ));
        
        // Update selected story if viewing the same story
        if (selectedStory && selectedStory.id === currentFormat.story.id) {
          setSelectedStory(prev => ({
            ...prev,
            formats: {
              ...prev.formats,
              [editingFormat.formatType]: editFormatContent
            }
          }));
        }
        
        // Clear editing state
        setEditingFormat(null);
        setEditFormatContent('');
      } else {
        const errorData = await response.json();
        console.error('Failed to update format:', errorData);
        alert(`Failed to update format: ${errorData.message || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error updating format:', error);
      alert('Error updating format. Please try again.');
    } finally {
      setIsUpdatingFormat(false);
    }
  };

  // UI Components
  const renderNavbar = () => (
    <nav className="hidden md:block bg-white border-b border-gray-200 px-4 py-2 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-6">
          <button 
            onClick={() => {
              setCurrentView('discover');
              setSelectedStory(null);
              setCurrentFormat(null);
              setFormatContent('');
              setPreviousView('discover');
            }}
            className="text-xl font-bold text-purple-600 no-underline hover:text-purple-700 transition-colors"
          >
            Sentimental
          </button>
          
          <div className="hidden md:flex items-center gap-1">
            {[
              { id: 'discover', label: 'Discover', icon: Search },
              { id: 'share', label: 'Chat', icon: MessageCircle },
              { id: 'stories', label: 'Stories', icon: BookOpen },
              { 
                id: 'inner-space', 
                label: 'Space', 
                icon: () => (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
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
                    // Show modal first, then allow access to concept page
                    setShowSpaceModal(true);
                    setCurrentView('inner-space');
                    setSelectedStory(null);
                    setCurrentFormat(null);
                    setFormatContent('');
                    setPreviousView(tab.id);
                  } else {
                    // Clean up any format/story state when changing tabs
                    setCurrentView(tab.id);
                    setSelectedStory(null);
                    setCurrentFormat(null);
                    setFormatContent('');
                    setPreviousView(tab.id);
                    // Refresh stories when switching to stories or discover tabs
                    if (tab.id === 'stories' || tab.id === 'discover') {
                      fetchStories();
                    }
                  }
                }}
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

          <div className="mt-4 text-center space-y-2">
            <button
              onClick={() => {
                setIsSignupMode(!isSignupMode);
                setLoginForm({ name: '', email: '', password: '' });
              }}
              className="text-purple-600 hover:text-purple-700 text-sm font-medium block w-full"
            >
              {isSignupMode ? 'Already have an account? Sign in' : 'Need an account? Sign up'}
            </button>
            
            {!isSignupMode && (
              <button
                onClick={handleForgotPassword}
                disabled={isLoading}
                className="text-gray-500 hover:text-gray-700 text-sm font-medium disabled:opacity-50"
              >
                Forgot your password?
              </button>
            )}
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
    <div className="h-full flex flex-col">
      {/* Mobile Header - Only show on mobile */}
      <div className="md:hidden bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
        <button 
          onClick={() => {
            setCurrentView('discover');
            setSelectedStory(null);
            setCurrentFormat(null);
            setFormatContent('');
            setPreviousView('discover');
          }}
          className="text-lg font-bold text-purple-600 hover:text-purple-700 transition-colors"
        >
          Sentimental
        </button>
        
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
              <span className="text-sm font-medium text-gray-700 max-w-[80px] truncate">
                {user.name}
              </span>
            </div>
            <button
              onClick={handleLogout}
              className="text-xs text-gray-500 hover:text-gray-700 px-2 py-1 rounded-lg hover:bg-gray-100 transition-colors"
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
      
      {/* Welcome Section */}
      <div className="bg-gradient-to-br from-purple-50 to-indigo-50 border-b border-gray-100 p-6">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-3">
            Discover Your True Self ✨
          </h1>
          <p className="text-lg text-gray-600 mb-6">
            A space for deep conversations about life, emotions, relationships, and everything that matters to you. 
            Reflect, understand, and express your authentic self.
          </p>
          
          {!user ? (
            <div className="bg-white/70 backdrop-blur-sm rounded-xl p-6 mb-6 border border-white/20">
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Start Your Journey</h3>
              <p className="text-gray-600 mb-4">
                Join a community where your thoughts matter and your story becomes something beautiful.
              </p>
              <button
                onClick={() => setShowLogin(true)}
                className="bg-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-purple-700 transition-colors"
              >
                Begin Discovering Yourself
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-2xl mx-auto">
              {[
                { type: 'reflection', icon: '🤔', label: 'Reflection', desc: 'Deep thoughts' },
                { type: 'reel', icon: '🎬', label: 'Reel', desc: 'Short video script' },
                { type: 'poem', icon: '📝', label: 'Poem', desc: 'Poetic expression' },
                { type: 'fairytale', icon: '📚', label: 'Fairytale', desc: 'Magic short story' }
              ].map((format) => (
                <div key={format.type} className="bg-white/70 backdrop-blur-sm rounded-lg p-4 text-center border border-white/20">
                  <div className="text-2xl mb-2">{format.icon}</div>
                  <div className="font-medium text-gray-800">{format.label}</div>
                  <div className="text-xs text-gray-600">{format.desc}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Story Cards */}
      <div className="flex-1 overflow-y-auto p-6">
        {loadingFormat ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
          </div>
        ) : (
          <div className="grid gap-6">
            {stories.filter(story => story.public === true).map(story => (
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
                        <span className="text-sm font-medium text-purple-700">
                          {user && story.user_id === user.id ? 'Your Transformations:' : 'Available Transformations:'}
                        </span>
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
            
            {stories.filter(story => story.public === true).length === 0 && (
              <div className="text-center py-12 bg-white rounded-2xl border border-gray-200">
                <div className="text-6xl mb-4">📚</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">No public stories to discover yet</h3>
                <p className="text-gray-600 mb-6">Be the first to share a public story!</p>
                <button 
                  onClick={() => setCurrentView('share')}
                  className="px-6 py-3 bg-purple-600 text-white rounded-xl hover:bg-purple-700 transition-all font-medium"
                >
                                        Start Chatting
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );

  // Share Page - Chat Interface
  const renderShare = () => (
    <div className="flex flex-col min-h-[calc(100vh-4rem)] md:min-h-[calc(100vh-5rem)]">
      {/* Mobile Header */}
      <div className="md:hidden bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
        <button 
          onClick={() => {
            setCurrentView('discover');
            setSelectedStory(null);
            setCurrentFormat(null);
            setFormatContent('');
            setPreviousView('discover');
          }}
          className="text-lg font-bold text-purple-600 hover:text-purple-700 transition-colors"
        >
          Sentimental
        </button>
        
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
              <span className="text-sm font-medium text-gray-700 max-w-[80px] truncate">
                {user.name}
              </span>
            </div>
            <button
              onClick={handleLogout}
              className="text-xs text-gray-500 hover:text-gray-700 px-2 py-1 rounded-lg hover:bg-gray-100 transition-colors"
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
      
      {/* Desktop Header */}
      <div className="hidden md:block bg-white border-b border-gray-200 p-4 flex-shrink-0">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">Express Your True Self</h1>
            <p className="text-sm text-gray-600">Deep conversations that become beautiful stories, songs & more</p>
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
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Sign In to Start Chatting</h2>
                  <p className="text-gray-600 mb-8 max-w-lg mx-auto">
                    Create an account to start meaningful conversations with your AI companion 
                    and transform your experiences into beautiful content.
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
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">Chat About What's Really On Your Mind ✨</h2>
                  <p className="text-gray-600 mb-4 max-w-lg mx-auto">
                    Have a real conversation about what matters to you. Your AI companion will listen deeply 
                    and help you express your thoughts in ways that feel authentic and beautiful.
                  </p>
                  <p className="text-gray-600 mb-4 max-w-lg mx-auto">
                    Tell me about your dreams, achievements, or wild moments and I'll help you turn them into:
                  </p>
                  <div className="flex flex-wrap justify-center gap-3 mb-6">
                    <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm font-medium">🌟 Reflections</span>
                    <span className="bg-pink-100 text-pink-700 px-3 py-1 rounded-full text-sm font-medium">🎵 Songs</span>
                    <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium">📖 Stories</span>
                    <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm font-medium">✨ Poems</span>
                  </div>
                  <p className="text-gray-600 mb-6 max-w-lg mx-auto text-sm">
                    Tell me what's on your mind - your dreams, challenges, relationships, or anything that matters to you.
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
                placeholder="Type your message... (Say 'turn this into a story' when you want to save our chat)"
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
            <p className="text-lg text-gray-600">Your journey of self-discovery through stories</p>
          </div>
          
          <div className="text-center py-12">
            <div className="text-6xl mb-4">👤</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Sign in to see your personal stories</h3>
            <p className="text-gray-600 mb-6">Sign in to save your stories and continue your journey of personal growth and self-discovery.</p>
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
      <div>
        {/* Mobile Header */}
        <div className="md:hidden bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
          <button 
            onClick={() => {
              setCurrentView('discover');
              setSelectedStory(null);
              setCurrentFormat(null);
              setFormatContent('');
              setPreviousView('discover');
            }}
            className="text-lg font-bold text-purple-600 hover:text-purple-700 transition-colors"
          >
            Sentimental
          </button>
          
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
                <span className="text-sm font-medium text-gray-700 max-w-[80px] truncate">
                  {user.name}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="text-xs text-gray-500 hover:text-gray-700 px-2 py-1 rounded-lg hover:bg-gray-100 transition-colors"
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
        
        <div className="p-6">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">My Stories</h1>
            <p className="text-lg text-gray-600">Your journey of self-discovery through stories</p>
          </div>

        {userStories.length > 0 ? (
          <div className="grid gap-6">
            {userStories.map((story) => (
              <div
                key={story.id}
                className="bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-200 cursor-pointer border border-gray-100 p-6 group"
                onClick={() => {
                  setSelectedStory(story);
                  setPreviousView('stories');
                  setCurrentView('story-detail');
                }}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-purple-700 transition-colors">
                      {story.title}
                    </h3>
                    <div className="flex items-center gap-3 text-sm text-gray-500 mb-3">
                      <span>{formatDate(story.created_at || story.timestamp)}</span>
                      <span>•</span>
                      <span className="capitalize">{story.type || 'Story'}</span>
                      {story.public && (
                        <>
                          <span>•</span>
                          <span className="text-green-600 font-medium">Public</span>
                        </>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    {/* Edit Button - Only show for story owner */}
                    {user && (story.user_id === user.id || story.author_id === user.id) && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          startEditingStory(story);
                        }}
                        className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                        title="Edit story"
                      >
                        <Edit size={16} />
                      </button>
                    )}
                  </div>
                </div>

                {/* Story Preview */}
                <div className="mb-4 p-4 bg-gray-50 rounded-xl group-hover:bg-purple-50 transition-colors">
                  <p className="text-gray-700 text-sm leading-relaxed line-clamp-3">
                    {story.content?.substring(0, 200) + '...' || 'Click to read your full story...'}
                  </p>
                </div>

                {/* Privacy and formats - exact original style */}
                <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                  <div className="flex items-center gap-3 text-sm text-gray-500">
                    <span className="text-gray-600">
                      {story.public ? 'Public' : 'Private'}
                    </span>
                    {user && (story.user_id === user.id || story.author_id === user.id) && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleStoryPrivacy(story.id, story.public);
                        }}
                        className="relative inline-flex items-center h-6 w-11 bg-gray-200 rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
                        style={{
                          backgroundColor: story.public ? '#10B981' : '#D1D5DB'
                        }}
                        title={story.public ? 'Make private' : 'Make public'}
                      >
                        <span
                          className="inline-block w-4 h-4 bg-white rounded-full transition-transform"
                          style={{
                            transform: story.public ? 'translateX(24px)' : 'translateX(4px)'
                          }}
                        />
                      </button>
                    )}
                    
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
                  
                  {/* Read Full Story Button */}
                  <div className="flex items-center gap-2 text-purple-600 group-hover:text-purple-700 font-medium text-sm">
                    <BookOpen size={16} />
                    <span>Read Full Story</span>
                    <ChevronRight size={16} className="group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <BookOpen className="mx-auto mb-4 text-gray-400" size={48} />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No stories yet</h3>
            <p className="text-gray-600 mb-6">Start conversations with your AI companion to explore your inner world and create meaningful stories about your journey.</p>
            <button
              onClick={() => setCurrentView('share')}
              className="bg-purple-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-purple-700 transition-colors"
            >
              Start Chatting
            </button>
          </div>
        )}
        </div>
      </div>
    );
  };

  // Story Detail View
  const renderStoryDetail = () => {
    if (!selectedStory) return null;

    return (
      <div className="p-6">
        {/* Back Button - Top of Content */}
        <div className="mb-6">
          <button
            onClick={() => setCurrentView(previousView || 'discover')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft />
            Back
          </button>
          
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
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
              
              {/* Edit Button - Only show for story owner */}
              {user && (selectedStory.user_id === user.id || selectedStory.author_id === user.id) && (
                <button
                  onClick={() => startEditingStory(selectedStory)}
                  className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                  title="Edit story"
                >
                  <Edit size={16} />
                  <span className="text-sm font-medium">Edit</span>
                </button>
              )}
            </div>

            <h1 className="text-3xl font-bold text-gray-900 mb-6">{selectedStory.title}</h1>
            
            <div className="prose max-w-none">
              <p className="text-gray-700 leading-relaxed text-lg whitespace-pre-wrap">
                {selectedStory.content}
              </p>
            </div>

                         {/* Bottom Back Button - After Story Content */}
             <div className="mt-8 pt-6 border-t border-gray-200 flex justify-center">
               <button
                 onClick={() => setCurrentView(previousView || 'discover')}
                 className="flex items-center gap-2 text-gray-600 hover:text-purple-600 px-4 py-2 rounded-lg font-medium transition-colors hover:bg-gray-50"
               >
                 <ArrowLeft size={16} />
                 Back to {previousView === 'stories' ? 'My Stories' : 'Discover'}
               </button>
             </div>

            {/* Your Transformations */}
            {selectedStory.createdFormats && selectedStory.createdFormats.length > 0 && (
              <div className="mt-8 p-4 bg-purple-50 rounded-xl">
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles />
                  <span className="font-medium text-purple-700">
                  {user && selectedStory.user_id === user.id ? 'Your Transformations:' : 'Available Transformations:'}
                </span>
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

            {/* Transform Into - Only show for story author AND when there are formats available */}
            {user && selectedStory.user_id === user.id && 
             !loadingFormats && 
             supportedFormats.filter(format => !selectedStory.createdFormats?.includes(format)).length > 0 && (
              <div className="mt-8 p-4 bg-green-50 rounded-xl">
                <div className="flex items-center gap-2 mb-3">
                  <Plus />
                  <span className="font-medium text-green-700">Transform Into:</span>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {loadingFormats ? (
                    <div className="col-span-full flex items-center justify-center py-4">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-600"></div>
                      <span className="ml-2 text-sm text-gray-600">Loading formats...</span>
                    </div>
                  ) : (
                                         supportedFormats
                       .filter(format => !selectedStory.createdFormats?.includes(format))
                       .map(format => (
                         <button 
                           key={format} 
                           onClick={() => viewFormat(selectedStory, format)}
                           className="bg-green-100 text-green-700 rounded-lg p-3 text-center hover:bg-green-200 transition-colors cursor-pointer border-none"
                         >
                           <div className="text-2xl mb-1">{getFormatIcon(format)}</div>
                           <div className="text-sm font-medium">{getFormatDisplayName(format)}</div>
                         </button>
                       ))
                   )}
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
      // Match the exact format names from your list
      x: 'X',
      linkedin: 'Linkedin',
      instagram: 'Instagram',
      facebook: 'Facebook',
      poem: 'Poem',
      song: 'Song',
      reel: 'Reel',
      fairytale: 'Fairytale',
      article: 'Article',
      blog_post: 'Blog Post',
      presentation: 'Presentation',
      newsletter: 'Newsletter',
      podcast: 'Podcast',
      insights: 'Therapeutic Feedback',
      growth_summary: 'Growth Summary',
      journal_entry: 'Journal Entry',
      
      // Modern Viral Formats
      tiktok_script: '📱',
      instagram_reel: '🎬',
      x_thread: '🧵',
      youtube_short: '▶️',
      instagram_story: '📸',
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
              
              {/* Upload Button */}
              <button
                onClick={() => setShowUploadModal(true)}
                className="mr-2 px-3 py-1 bg-white/20 rounded-lg text-xs hover:bg-white/30 transition-colors"
              >
                Upload MP3
              </button>
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
                  <button 
                    onClick={() => setShowUploadModal(true)}
                    className="bg-white/20 hover:bg-white/30 px-2 py-1 rounded text-xs transition-colors"
                  >
                    Upload MP3
                  </button>
                </div>
                <div className="w-full bg-white/20 rounded-full h-2">
                  <div className="bg-white/50 h-2 rounded-full w-0"></div>
                </div>
                <div className="text-xs text-center mt-2 opacity-75">Click "Upload MP3" to add audio</div>
              </div>
            )}

            <div className="prose prose-invert max-w-none">
              <pre className="whitespace-pre-wrap font-sans leading-relaxed text-sm">
                {cleanContent || contentText}
              </pre>
            </div>
            
            <div className="mt-4 text-xs opacity-75">
              {hasAudio ? 
                '🎵 Music ready to play!' : 
                '🎧 Upload MP3 file to enable playback'
              }
            </div>
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
              // Keep the selected story but clear format state
            }}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft />
            Back to Story
          </button>
          
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            <div className="p-6 border-b border-gray-200">
              <div className="flex items-center justify-between">
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
                
                {/* Edit Button - Only show for story owner */}
                {user && currentFormat.story.user_id === user.id && (
                  <button
                    onClick={() => startEditingFormat(currentFormat, formatContent)}
                    className="flex items-center gap-2 px-3 py-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                    title="Edit format"
                  >
                    <Edit size={16} />
                    <span className="text-sm font-medium">Edit</span>
                  </button>
                )}
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

  // Inner Space Concept Page
  const renderInnerSpace = () => (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-indigo-50 to-pink-50">
      <div className="p-6 max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="w-20 h-20 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <polygon points="16.24,7.76 14.12,14.12 7.76,16.24 9.88,9.88"/>
            </svg>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Your Inner Space</h1>
          <p className="text-xl text-gray-600 mb-2">Personal AI-powered self-discovery dashboard</p>
          <div className="inline-flex items-center gap-2 bg-amber-100 text-amber-800 px-4 py-2 rounded-full text-sm font-medium">
            <span>🚧</span>
            Coming Soon - Preview Mode
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Ask Yourself Anything */}
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-xl flex items-center justify-center">
                <span className="text-2xl">🤔</span>
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900">Ask Yourself Anything</h3>
                <p className="text-gray-600">Deep questions about your life, patterns & growth</p>
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-800 font-medium mb-2">"What are my core values in relationships?"</p>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span>Answered from 3 stories</span>
                </div>
              </div>
              
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-800 font-medium mb-2">"How do I handle stress and challenges?"</p>
                <div className="flex items-center gap-2 text-sm text-orange-600">
                  <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                  <span>Needs exploration → Chat suggested</span>
                </div>
              </div>
              
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-800 font-medium mb-2">"What patterns do I see in my career choices?"</p>
                <div className="flex items-center gap-2 text-sm text-blue-600">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span>Partial insights → More data needed</span>
                </div>
              </div>
            </div>
          </div>

          {/* Curated Discovery Chats */}
          <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-teal-500 rounded-xl flex items-center justify-center">
                <span className="text-2xl">💭</span>
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900">Guided Discovery</h3>
                <p className="text-gray-600">AI-curated conversations that unlock insights</p>
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-lg p-4 border border-green-200">
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-lg">🎯</span>
                  <h4 className="font-semibold text-gray-900">Values Deep Dive</h4>
                </div>
                <p className="text-gray-700 text-sm mb-3">Explore what truly matters to you through guided reflection</p>
                <div className="flex items-center gap-2 text-xs text-green-700">
                  <span>✨ Becomes story</span>
                  <span>•</span>
                  <span>🧠 Builds your knowledge</span>
                </div>
              </div>
              
              <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-4 border border-purple-200">
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-lg">🚀</span>
                  <h4 className="font-semibold text-gray-900">Growth Moments</h4>
                </div>
                <p className="text-gray-700 text-sm mb-3">Reflect on challenges that shaped you</p>
                <div className="flex items-center gap-2 text-xs text-purple-700">
                  <span>📖 Multiple formats</span>
                  <span>•</span>
                  <span>🔍 Pattern recognition</span>
                </div>
              </div>
              
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-lg">💡</span>
                  <h4 className="font-semibold text-gray-900">Decision Analysis</h4>
                </div>
                <p className="text-gray-700 text-sm mb-3">Understand your decision-making patterns</p>
                <div className="flex items-center gap-2 text-xs text-blue-700">
                  <span>🔄 Continuous learning</span>
                  <span>•</span>
                  <span>📊 Visual insights</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Vision Statement */}
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl p-8 text-white text-center mb-8">
          <h2 className="text-2xl font-bold mb-4">Like Cursor writes code, we guide conversations</h2>
          <p className="text-lg opacity-90 max-w-3xl mx-auto leading-relaxed">
            Just as Cursor understands your intent and writes the perfect code, Inner Space will understand your questions 
            and guide you through the perfect conversations to discover the answers about yourself. Every chat becomes a story, 
            every story builds your personal knowledge base.
          </p>
        </div>

        {/* Future Features Preview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl p-6 border border-gray-100 text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-amber-400 to-orange-500 rounded-xl flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="font-bold text-gray-900 mb-2">Life Patterns</h3>
            <p className="text-gray-600 text-sm">Visual maps of your behavioral patterns, growth cycles, and recurring themes</p>
          </div>
          
          <div className="bg-white rounded-xl p-6 border border-gray-100 text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-xl flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🎭</span>
            </div>
            <h3 className="font-bold text-gray-900 mb-2">Personality Insights</h3>
            <p className="text-gray-600 text-sm">Deep understanding of your unique traits, preferences, and tendencies</p>
          </div>
          
          <div className="bg-white rounded-xl p-6 border border-gray-100 text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-rose-400 to-pink-500 rounded-xl flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🌟</span>
            </div>
            <h3 className="font-bold text-gray-900 mb-2">Growth Tracking</h3>
            <p className="text-gray-600 text-sm">Monitor your personal development journey with meaningful metrics</p>
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center mt-12">
          <p className="text-gray-600 mb-6">Start building your Inner Space today by creating meaningful stories</p>
          <button
            onClick={() => {
              setCurrentView('share');
              setSelectedStory(null);
              setCurrentFormat(null);
              setFormatContent('');
              setPreviousView('inner-space');
            }}
            className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-8 py-4 rounded-xl font-medium hover:from-purple-700 hover:to-pink-700 transition-all transform hover:scale-105"
          >
            Start Your Journey
          </button>
        </div>
      </div>
    </div>
  );

  // Space Coming Soon Modal
  const renderSpaceModal = () => {
    if (!showSpaceModal) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-2xl max-w-lg w-full p-8 text-center">
          <div className="w-20 h-20 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <polygon points="16.24,7.76 14.12,14.12 7.76,16.24 9.88,9.88"/>
            </svg>
          </div>
          
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Welcome to Inner Space!</h2>
          <p className="text-gray-600 mb-6 leading-relaxed">
            Your personal AI-powered self-discovery dashboard is coming soon. Get a preview of what's possible 
            and see how we'll help you understand yourself like never before.
          </p>
          
          <div className="space-y-3">
            <button
              onClick={() => setShowSpaceModal(false)}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-medium hover:from-purple-700 hover:to-pink-700 transition-all"
            >
              Explore the Vision
            </button>
            
            <button
              onClick={() => {
                setShowSpaceModal(false);
                setCurrentView('discover');
                setPreviousView('discover');
              }}
              className="w-full text-gray-500 hover:text-gray-700 py-2 text-sm"
            >
              Back to Discover
            </button>
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
      case 'inner-space': return renderInnerSpace();
      default: return renderDiscover();
    }
  };

  // Mobile Footer Navigation
  const renderMobileFooter = () => (
    <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
      <div className="flex items-center justify-evenly py-2">
        {[
          { 
            id: 'discover', 
            label: 'Discover', 
            icon: () => (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
              </svg>
            )
          },
          { 
            id: 'share', 
            label: 'Chat', 
            icon: () => (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
              </svg>
            )
          },
          { 
            id: 'stories', 
            label: 'Stories', 
            icon: () => (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
              </svg>
            )
          },
          { 
            id: 'inner-space', 
            label: 'Space', 
            icon: () => (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
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
                // Show modal first, then allow access to concept page
                setShowSpaceModal(true);
                setCurrentView('inner-space');
                setSelectedStory(null);
                setCurrentFormat(null);
                setFormatContent('');
                setPreviousView(tab.id);
              } else {
                // Clean up any format/story state when changing tabs
                setCurrentView(tab.id);
                setSelectedStory(null);
                setCurrentFormat(null);
                setFormatContent('');
                setPreviousView(tab.id);
                // Refresh stories when switching to stories or discover tabs
                if (tab.id === 'stories' || tab.id === 'discover') {
                  fetchStories();
                }
              }
            }}
            className={`flex flex-col items-center gap-1 px-1 py-2 transition-colors ${
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

  // Edit Story Modal
  const renderEditStoryModal = () => {
    if (!editingStory) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Edit Story</h2>
              <button
                onClick={cancelEditStory}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <div className="space-y-4">
              {/* Title Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Story Title
                </label>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                  placeholder="Enter story title..."
                />
              </div>

              {/* Content Textarea */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Story Content
                </label>
                <textarea
                  value={editContent}
                  onChange={(e) => setEditContent(e.target.value)}
                  rows={12}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 resize-vertical"
                  placeholder="Write your story content..."
                />
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
                <button
                  onClick={cancelEditStory}
                  className="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                  disabled={isUpdatingStory}
                >
                  Cancel
                </button>
                <button
                  onClick={saveStoryEdit}
                  disabled={isUpdatingStory || !editTitle.trim() || !editContent.trim()}
                  className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                >
                  {isUpdatingStory && (
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                  )}
                  {isUpdatingStory ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Edit Format Modal
  const renderEditFormatModal = () => {
    if (!editingFormat) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                Edit {getFormatDisplayName(editingFormat.formatType)}
              </h2>
              <button
                onClick={cancelEditFormat}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            <div className="space-y-4">
              {/* Format Type Info */}
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center gap-3">
                  <div className="text-2xl">{getFormatIcon(editingFormat.formatType)}</div>
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      {getFormatDisplayName(editingFormat.formatType)}
                    </h3>
                    <p className="text-sm text-gray-600">
                      Based on: {editingFormat.story.title}
                    </p>
                  </div>
                </div>
              </div>

              {/* Content Textarea */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Format Content
                </label>
                <textarea
                  value={editFormatContent}
                  onChange={(e) => setEditFormatContent(e.target.value)}
                  rows={16}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 resize-vertical font-sans text-sm"
                  placeholder={`Edit your ${getFormatDisplayName(editingFormat.formatType).toLowerCase()} content...`}
                />
                <p className="text-xs text-gray-500 mt-1">
                  Make your changes to the generated content above
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
                <button
                  onClick={cancelEditFormat}
                  className="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                  disabled={isUpdatingFormat}
                >
                  Cancel
                </button>
                <button
                  onClick={saveFormatEdit}
                  disabled={isUpdatingFormat || !editFormatContent.trim()}
                  className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                >
                  {isUpdatingFormat && (
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                  )}
                  {isUpdatingFormat ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {renderNavbar()}
      {renderLoginModal()}
      {renderUploadModal()}
      {renderSpaceModal()}
      {editingStory && renderEditStoryModal()}
      {editingFormat && renderEditFormatModal()}
      
      {/* Main Content with bottom padding on mobile for footer */}
      <div className="pb-20 md:pb-0">
        {renderMainContent()}
      </div>

      {/* Mobile Footer Navigation */}
      {renderMobileFooter()}
    </div>
  );
};

// Make it available globally
window.SentimentalApp = SentimentalApp;