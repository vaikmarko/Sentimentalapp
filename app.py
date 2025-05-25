from flask import Flask, render_template, jsonify, request, send_from_directory
from datetime import datetime
import json
import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import firebase_admin
from firebase_admin import credentials, firestore
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment detection
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')  # production, demo, test
IS_DEMO = ENVIRONMENT == 'demo'
IS_TEST = ENVIRONMENT == 'test'

logger.info(f"Starting application in {ENVIRONMENT} environment")

app = Flask(__name__)

# Initialize db variable
db = None

# Firebase configuration
try:
    # Check if we're in Cloud Run environment
    if os.getenv('K_SERVICE') or os.getenv('GOOGLE_CLOUD_PROJECT'):
        logger.info("Initializing Firebase in Cloud Run environment")
        # In Cloud Run environment we use automatic authentication
        firebase_admin.initialize_app()
    else:
        logger.info("Initializing Firebase in local environment")
        # In local environment we use credentials file
        if os.path.exists('firebase-credentials.json'):
            cred = credentials.Certificate('firebase-credentials.json')
            firebase_admin.initialize_app(cred)
        else:
            logger.warning("No firebase-credentials.json found, trying default credentials")
            firebase_admin.initialize_app()
    logger.info("Firebase initialized successfully")
    if db is None:
        db = firestore.client()
except Exception as e:
    logger.error(f"Error initializing Firebase: {str(e)}")
    # In demo mode, we can continue without Firebase since we use mock data
    if IS_DEMO:
        logger.info("Demo mode: continuing without Firebase connection")
        db = None
    else:
        raise

# Download NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

def analyze_text(text):
    """Analyzes text and finds themes, emotions and connections"""
    # Tokenize text
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords - use English as fallback if Estonian not available
    try:
        stop_words = set(stopwords.words('estonian'))
    except OSError:
        logger.warning("Estonian stopwords not available, using English stopwords")
        stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    
    # Find most frequent words (themes)
    word_freq = Counter(tokens)
    themes = [word for word, freq in word_freq.most_common(5)]
    
    # Analyze emotions
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    
    emotions = []
    if sentiment['pos'] > 0.5:
        emotions.append('positive')
    if sentiment['neg'] > 0.5:
        emotions.append('negative')
    if sentiment['neu'] > 0.5:
        emotions.append('neutral')
    
    return {
        'themes': themes,
        'emotions': emotions,
        'sentiment_score': sentiment['compound']
    }

def find_connections(story_id):
    """Finds connections between stories"""
    if db is None:
        return []
        
    story_ref = db.collection('stories').document(str(story_id))
    story = story_ref.get()
    
    if not story.exists:
        return []
    
    story_data = story.to_dict()
    connections = []
    
    # Search for all other stories
    other_stories = db.collection('stories').where('id', '!=', story_id).stream()
    
    for other_story in other_stories:
        other_data = other_story.to_dict()
        # Simple connection finding based on similar words
        story_words = set(word_tokenize(story_data['content'].lower()))
        other_words = set(word_tokenize(other_data['content'].lower()))
        common_words = story_words.intersection(other_words)
        
        if len(common_words) > 3:  # If there are more than 3 common words
            connection = {
                'id': other_data['id'],
                'title': other_data['title'],
                'description': f"Similar themes: {', '.join(list(common_words)[:3])}",
                'strength': len(common_words) / 10  # Normalize strength to 0-1 range
            }
            connections.append(connection)
            
            # Save connection to database
            db.collection('connections').add({
                'story_id': story_id,
                'connected_story_id': other_data['id'],
                'common_words': list(common_words),
                'strength': connection['strength'],
                'created_at': firestore.SERVER_TIMESTAMP
            })
    
    return connections

@app.route('/')
def index():
    return render_template('index.html', environment=ENVIRONMENT)

@app.route('/app')
def app_view():
    # Only allow app access in demo and test environments
    if ENVIRONMENT == 'production':
        return render_template('index.html', environment=ENVIRONMENT)
    return render_template('app.html', environment=ENVIRONMENT)

@app.route('/landing')
def landing():
    return render_template('index.html', environment=ENVIRONMENT)

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/cosmos')
def cosmos():
    # Only allow cosmos access in demo and test environments
    if ENVIRONMENT == 'production':
        return render_template('index.html', environment=ENVIRONMENT)
    return render_template('cosmos.html', environment=ENVIRONMENT)

@app.route('/chat')
def chat():
    # Only allow chat access in demo and test environments
    if ENVIRONMENT == 'production':
        return render_template('index.html', environment=ENVIRONMENT)
    return render_template('chat.html', environment=ENVIRONMENT)

@app.route('/deck')
def deck():
    # Only allow deck access in demo and test environments
    if ENVIRONMENT == 'production':
        return render_template('index.html', environment=ENVIRONMENT)
    return render_template('deck.html', environment=ENVIRONMENT)

@app.route('/story')
def story():
    # Only allow story access in demo and test environments
    if ENVIRONMENT == 'production':
        return render_template('index.html', environment=ENVIRONMENT)
    return render_template('story.html', environment=ENVIRONMENT)

@app.route('/api/stories', methods=['GET'])
def get_stories():
    if IS_DEMO:
        # Use mock data in demo environment
        stories = get_mock_stories()
        logger.info(f"Returning {len(stories)} mock stories for demo environment")
        return jsonify(stories)
    
    # Regular database query
    if db is None:
        return jsonify([])
        
    stories = []
    for story in db.collection('stories').stream():
        story_data = story.to_dict()
        # Ensure compatibility with React component
        story_data['author'] = story_data.get('author', 'Anonymous')
        story_data['content'] = story_data.get('content', story_data.get('text', ''))
        story_data['timestamp'] = story_data.get('timestamp', '1h ago')
        story_data['format'] = story_data.get('format', 'text')
        story_data['public'] = story_data.get('public', True)
        story_data['reactions'] = story_data.get('reactions', 0)
        story_data['inCosmos'] = story_data.get('inCosmos', False)
        story_data['createdFormats'] = story_data.get('createdFormats', [])
        story_data['cosmic_insights'] = story_data.get('analysis', {}).get('themes', [])
        stories.append(story_data)
    return jsonify(stories)

@app.route('/api/stories', methods=['POST'])
def add_story():
    if IS_DEMO:
        # Don't allow adding new stories in demo environment
        return jsonify({
            'error': 'Cannot add new stories in demo environment',
            'message': 'This is a demo version. Use the full version to add new stories.'
        }), 403
    
    # In test environment, require authentication
    if IS_TEST:
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please register or login to create stories in test environment.'
            }), 401
        
        # Verify user exists
        try:
            user_doc = db.collection('test_users').document(user_id).get()
            if not user_doc.exists:
                return jsonify({'error': 'Invalid user'}), 401
        except Exception as e:
            return jsonify({'error': 'Authentication failed'}), 401
    
    if db is None:
        return jsonify({'error': 'Database not available'}), 500
        
    story = request.json
    story['id'] = str(len(list(db.collection('stories').stream())) + 1)
    story['timestamp'] = datetime.now().isoformat()
    story['author'] = story.get('author', 'You')
    story['public'] = story.get('public', True)
    story['reactions'] = 0
    story['inCosmos'] = False
    story['createdFormats'] = []
    
    # Analüüsi lugu
    analysis = analyze_text(story['content'])
    story['emotional_intensity'] = abs(analysis['sentiment_score'])
    story['analysis'] = analysis
    
    # Salvesta andmebaasi
    db.collection('stories').document(story['id']).set(story)
    
    # Update user statistics in test environment
    if IS_TEST and 'user_id' in locals():
        try:
            user_ref = db.collection('test_users').document(user_id)
            user_ref.update({'stories_created': firestore.Increment(1)})
        except Exception as e:
            logger.warning(f"Failed to update user statistics: {str(e)}")
    
    # Loo seosed teiste lugudega
    connections = find_connections(story['id'])
    
    return jsonify(story), 201

@app.route('/api/connections/<string:story_id>', methods=['GET'])
def get_connections(story_id):
    if IS_DEMO:
        # Use mock connections in demo environment
        mock_connections = get_mock_connections()
        connections = [conn for conn in mock_connections if conn['story_id'] == story_id]
        logger.info(f"Returning {len(connections)} mock connections for story {story_id}")
        return jsonify(connections)
    
    # Regular database query
    if db is None:
        return jsonify([])
        
    connections = []
    for conn in db.collection('connections').where('story_id', '==', story_id).stream():
        connections.append(conn.to_dict())
    return jsonify(connections)

@app.route('/api/insights/<string:story_id>', methods=['GET'])
def get_insights(story_id):
    story_ref = db.collection('stories').document(story_id)
    story = story_ref.get()
    
    if not story.exists:
        return jsonify({'error': 'Story not found'}), 404
    
    story_data = story.to_dict()
    connections = find_connections(story_id)
    
    insights = {
        'themes': story_data['analysis']['themes'],
        'emotions': story_data['analysis']['emotions'],
        'connections': [f"Connection with story '{conn['title']}'" for conn in connections]
    }
    return jsonify(insights)

@app.route('/api/stories/<string:story_id>/formats', methods=['POST'])
def generate_story_format(story_id):
    """Generate a new format for an existing story"""
    # In test environment, require authentication
    if IS_TEST:
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please register or login to generate formats in test environment.'
            }), 401
        
        # Verify user exists
        try:
            user_doc = db.collection('test_users').document(user_id).get()
            if not user_doc.exists:
                return jsonify({'error': 'Invalid user'}), 401
        except Exception as e:
            return jsonify({'error': 'Authentication failed'}), 401
    
    data = request.json
    format_type = data.get('format_type', 'article')
    
    # Get the original story
    story_ref = db.collection('stories').document(story_id)
    story = story_ref.get()
    
    if not story.exists:
        return jsonify({'error': 'Story not found'}), 404
    
    story_data = story.to_dict()
    
    # Generate format based on type (placeholder - you can enhance this with actual AI)
    generated_content = generate_format_content(story_data['content'], format_type)
    
    # Update story with new format
    if 'createdFormats' not in story_data:
        story_data['createdFormats'] = []
    
    if format_type not in story_data['createdFormats']:
        story_data['createdFormats'].append(format_type)
        story_ref.update({'createdFormats': story_data['createdFormats']})
    
    # Update user statistics in test environment
    if IS_TEST and 'user_id' in locals():
        try:
            user_ref = db.collection('test_users').document(user_id)
            user_ref.update({'formats_generated': firestore.Increment(1)})
        except Exception as e:
            logger.warning(f"Failed to update user statistics: {str(e)}")
    
    return jsonify({
        'format_type': format_type,
        'content': generated_content,
        'message': f'{format_type.title()} format generated successfully'
    })

def generate_format_content(original_content, format_type):
    """Generate content in different formats - enhanced with realistic content"""
    # Extract key themes from original content
    words = original_content.lower().split()
    content_preview = original_content[:100] + "..." if len(original_content) > 100 else original_content
    title_words = original_content.split()[:6]
    title_hint = " ".join(title_words) + ("..." if len(title_words) >= 6 else "")
    
    formats = {
        'song': f"""♪ Generated Song: "{title_hint}"

Verse 1:
{content_preview[:50]}...
When the world feels heavy on my soul
I find the strength to make me whole

Chorus:
Every story has its meaning
Every moment worth believing
Through the darkness comes the light
Everything will be alright

(Generated from your personal experience)""",
        
        'video': f"""🎬 VIDEO SCRIPT: "{title_hint}"

[SCENE 1: OPENING]
*Soft background music*
*Close-up shot of thoughtful expression*

NARRATOR (V.O.):
"{content_preview[:80]}..."

[SCENE 2: MAIN STORY]
*Visual montage matching the emotional tone*

TEXT OVERLAY: Key insights from your experience

[SCENE 3: REFLECTION]
*Return to narrator*

NARRATOR:
"Sometimes our most challenging moments become our greatest teachers..."

[END SCREEN]
*Call to action: "Share your story"*

Duration: 2:30
Generated from your personal narrative""",
        
        'article': f"""📝 ARTICLE: "{title_hint}"

{original_content}

**Reflection & Analysis**

This personal narrative reveals several important themes about human resilience and emotional growth. The experience described offers valuable insights into how we process challenging situations and find meaning in our everyday moments.

**Key Takeaways:**
• Personal growth often comes through unexpected experiences
• Emotional awareness leads to better decision-making  
• Sharing our stories helps others feel less alone
• Every experience contributes to our personal narrative

*This article was generated from a personal story to help preserve and share meaningful experiences.*""",
        
        'tweet': f"""🐦 TWITTER THREAD: "{title_hint}"

1/ {content_preview[:120]}

2/ Sometimes the moments that challenge us most become the ones that teach us the deepest lessons about ourselves 🌱

3/ Sharing our real experiences - the messy, beautiful, complicated ones - helps others feel less alone in their journey ✨

4/ What's one moment that changed your perspective recently? Drop it below 👇

#PersonalGrowth #Storytelling #RealTalk #EmotionalIntelligence""",
        
        'linkedin_post': f"""💼 LINKEDIN POST: Professional Reflection

{title_hint}

Recently, I've been reflecting on how personal experiences shape our professional perspectives...

{content_preview[:150]}...

This experience taught me valuable lessons about:
• Emotional intelligence in decision-making
• The importance of authentic communication  
• How personal growth translates to professional development
• Building resilience in challenging situations

Sometimes our most personal moments offer the greatest professional insights.

What personal experience has most influenced your professional growth?

#PersonalDevelopment #ProfessionalGrowth #Leadership #EmotionalIntelligence #Reflection""",
        
        'fb_post': f"""👥 FACEBOOK POST: 

{title_hint} 💭

{content_preview[:180]}...

You know those moments that just stick with you? This was one of them. 

Sometimes I think we don't share enough of the real stuff - the moments that actually shape us, not just the highlight reel. Life is messy and beautiful and complicated, and that's exactly what makes it worth sharing.

Anyone else have one of those experiences that just changed how you see things? Would love to hear your stories in the comments 💕

#RealLife #PersonalGrowth #Storytelling #Community""",
        
        'book_chapter': f"""📚 BOOK CHAPTER: "{title_hint}"

Chapter {generate_chapter_number()}: {title_hint}

{original_content}

---

**Author's Note:**

Writing this chapter brought back the full weight of that experience. As I sit here now, months later, I can see how this moment fit into the larger tapestry of my personal growth journey. 

What struck me most while revisiting this story was how our perception of events can shift over time. What felt overwhelming in the moment now appears as a crucial turning point - a necessary catalyst for the person I was becoming.

This is the power of storytelling: it allows us to make meaning from chaos, to find patterns in what initially seems random, and to discover the deeper currents that run beneath the surface of our daily lives.

**Reflection Questions:**
• What experiences in your life felt difficult at the time but now seem necessary?
• How do you make sense of challenging moments in your personal narrative?
• What stories from your life are waiting to be told?

*[Chapter continues with deeper analysis and connecting themes...]*""",
        
        'diary_entry': f"""📖 PERSONAL DIARY ENTRY

Dear Diary,

{original_content}

Looking back on this as I write, I'm struck by how much this moment taught me about myself. There's something powerful about putting experiences into words - it helps me process emotions I didn't even know I was carrying.

I keep thinking about how these small moments end up shaping who we become. Like, this wasn't some huge life event, but somehow it feels significant. Maybe that's what growing up really is - learning to pay attention to these quiet revelations.

I want to remember this feeling, this insight. Sometimes I think that's why I write - not just to record what happened, but to capture how it felt, what it meant, how it changed me.

Until next time,
Me

*Personal reflection generated from life experience*"""
    }
    
    return formats.get(format_type, f"Generated {format_type}: {original_content}")

def generate_chapter_number():
    """Generate a random chapter number for book format"""
    import random
    return random.randint(1, 20)

@app.route('/api/auth/register', methods=['POST'])
def register_user():
    """Register a new user in test environment"""
    if not IS_TEST:
        return jsonify({'error': 'Registration only available in test environment'}), 403
    
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        name = data.get('name', '').strip()
        
        if not email or not name:
            return jsonify({'error': 'Email and name are required'}), 400
        
        # Basic email validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Check if user already exists
        existing = db.collection('test_users').where('email', '==', email).limit(1).get()
        if len(list(existing)) > 0:
            return jsonify({'error': 'User already exists'}), 409
        
        # Create user
        user_data = {
            'email': email,
            'name': name,
            'created_at': firestore.SERVER_TIMESTAMP,
            'stories_created': 0,
            'formats_generated': 0
        }
        
        user_ref = db.collection('test_users').add(user_data)
        user_id = user_ref[1].id
        
        logger.info(f"Test user registered: {email}")
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id,
            'email': email,
            'name': name
        }), 201
        
    except Exception as e:
        logger.error(f"Error in user registration: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login_user():
    """Login user in test environment"""
    if not IS_TEST:
        return jsonify({'error': 'Login only available in test environment'}), 403
    
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Find user
        users = db.collection('test_users').where('email', '==', email).limit(1).get()
        if len(list(users)) == 0:
            return jsonify({'error': 'User not found'}), 404
        
        user_doc = list(users)[0]
        user_data = user_doc.to_dict()
        
        return jsonify({
            'message': 'Login successful',
            'user_id': user_doc.id,
            'email': user_data['email'],
            'name': user_data['name'],
            'stories_created': user_data.get('stories_created', 0),
            'formats_generated': user_data.get('formats_generated', 0)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in user login: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/waitlist', methods=['POST'])
def join_waitlist():
    """Add email to waitlist"""
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Basic email validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Store in database if available
        if db is not None:
            try:
                # Check if email already exists
                existing = db.collection('waitlist').where('email', '==', email).limit(1).get()
                if len(list(existing)) > 0:
                    return jsonify({'message': 'Email already on waitlist'}), 200
                
                # Add to waitlist
                db.collection('waitlist').add({
                    'email': email,
                    'timestamp': firestore.SERVER_TIMESTAMP,
                    'source': 'landing_page'
                })
                logger.info(f"Added {email} to waitlist")
            except Exception as e:
                logger.error(f"Error saving to database: {str(e)}")
                # Continue anyway - we'll log it
        
        # Send email notification to join@sentimentalapp.com
        try:
            # In a real implementation, you'd use a service like SendGrid, Mailgun, etc.
            # For now, we'll just log it
            logger.info(f"New waitlist signup: {email} - should notify join@sentimentalapp.com")
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
        
        return jsonify({'message': 'Successfully joined waitlist'}), 200
        
    except Exception as e:
        logger.error(f"Error in waitlist endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/cosmos-data', methods=['GET'])
def get_cosmos_data():
    """Get data for cosmos visualization"""
    if IS_DEMO:
        # Use mock data in demo environment
        mock_stories = get_mock_stories()
        stories = []
        for story_data in mock_stories:
            stories.append({
                'id': story_data.get('id'),
                'title': story_data.get('title'),
                'themes': story_data.get('analysis', {}).get('themes', []),
                'emotional_intensity': story_data.get('emotional_intensity', 0.5),
                'timestamp': story_data.get('timestamp')
            })
        
        mock_connections = get_mock_connections()
        connections = []
        for conn_data in mock_connections:
            connections.append({
                'source': conn_data.get('story_id'),
                'target': conn_data.get('connected_story_id'),
                'strength': conn_data.get('strength', 0.5)
            })
        
        return jsonify({
            'stories': stories,
            'connections': connections,
            'insights': {
                'total_stories': len(stories),
                'total_connections': len(connections),
                'most_common_themes': get_common_themes(mock_stories)
            }
        })
    
    # Regular database query
    stories = []
    for story in db.collection('stories').stream():
        story_data = story.to_dict()
        stories.append({
            'id': story_data.get('id'),
            'title': story_data.get('title'),
            'themes': story_data.get('analysis', {}).get('themes', []),
            'emotional_intensity': story_data.get('emotional_intensity', 0.5),
            'timestamp': story_data.get('timestamp')
        })
    
    connections = []
    for conn in db.collection('connections').stream():
        conn_data = conn.to_dict()
        connections.append({
            'source': conn_data.get('story_id'),
            'target': conn_data.get('connected_story_id'),
            'strength': conn_data.get('strength', 0.5)
        })
    
    return jsonify({
        'stories': stories,
        'connections': connections,
        'insights': {
            'total_stories': len(stories),
            'total_connections': len(connections),
            'most_common_themes': get_common_themes(stories)
        }
    })

def get_common_themes(stories):
    """Finds common themes across stories"""
    all_themes = []
    for story in stories:
        if 'analysis' in story and 'themes' in story['analysis']:
            all_themes.extend(story['analysis']['themes'])
    
    theme_counts = Counter(all_themes)
    return [theme for theme, count in theme_counts.most_common(10)]

def get_mock_stories():
    """Returns mock data for demo environment"""
    return [
        {
            "id": "demo1",
            "title": "First step into a new life",
            "content": "Today I made a decision that changes everything. After long consideration, I finally decided to accept my dream job. Fear and excitement mix together, but I feel this is the right step.",
            "author": "Maria K.",
            "timestamp": "2h ago",
            "format": "text",
            "public": True,
            "reactions": 15,
            "inCosmos": True,
            "createdFormats": ["poem", "letter"],
            "emotional_intensity": 0.8,
            "analysis": {
                "themes": ["change", "decision", "dream", "work", "fear"],
                "emotions": ["positive", "neutral"],
                "sentiment_score": 0.6
            },
            "cosmic_insights": ["change", "decision", "dream"]
        },
        {
            "id": "demo2", 
            "title": "Grandmother's memories",
            "content": "I found letters in grandmother's old chest that she once wrote to grandfather. Every line was full of love and longing. These words helped me understand that true love lasts forever.",
            "author": "John P.",
            "timestamp": "5h ago",
            "format": "text", 
            "public": True,
            "reactions": 23,
            "inCosmos": True,
            "createdFormats": ["story"],
            "emotional_intensity": 0.9,
            "analysis": {
                "themes": ["love", "memories", "family", "letters", "longing"],
                "emotions": ["positive", "neutral"],
                "sentiment_score": 0.7
            },
            "cosmic_insights": ["love", "memories", "family"]
        },
        {
            "id": "demo3",
            "title": "Night walk",
            "content": "Couldn't sleep so I went for a walk in the city. Empty streets, quiet night and only my footsteps echoing. I thought about life and realized that sometimes we need silence to hear our inner voice.",
            "author": "Lisa M.",
            "timestamp": "1d ago",
            "format": "text",
            "public": True, 
            "reactions": 8,
            "inCosmos": False,
            "createdFormats": [],
            "emotional_intensity": 0.5,
            "analysis": {
                "themes": ["silence", "reflection", "night", "walk", "inner_voice"],
                "emotions": ["neutral", "positive"],
                "sentiment_score": 0.3
            },
            "cosmic_insights": ["silence", "reflection"]
        },
        {
            "id": "demo4",
            "title": "Taste of childhood",
            "content": "Today I baked cookies following grandmother's recipe. The first bite took me back to childhood, where everything was simple and safe. Sometimes it's the small things that bring the most joy.",
            "author": "Kate L.",
            "timestamp": "2d ago", 
            "format": "text",
            "public": True,
            "reactions": 31,
            "inCosmos": True,
            "createdFormats": ["recipe", "memory"],
            "emotional_intensity": 0.8,
            "analysis": {
                "themes": ["childhood", "memories", "grandmother", "cookies", "joy"],
                "emotions": ["positive", "neutral"],
                "sentiment_score": 0.8
            },
            "cosmic_insights": ["childhood", "memories", "joy"]
        },
        {
            "id": "demo5",
            "title": "First snowfall",
            "content": "I looked out the window and saw the first snow of this winter. The world became quiet and pure. I feel that my soul also needs such cleansing - a chance to start with a clean slate.",
            "author": "Mark R.",
            "timestamp": "3d ago",
            "format": "text", 
            "public": True,
            "reactions": 12,
            "inCosmos": False,
            "createdFormats": [],
            "emotional_intensity": 0.6,
            "analysis": {
                "themes": ["snow", "purity", "new_beginning", "silence", "soul"],
                "emotions": ["positive", "neutral"],
                "sentiment_score": 0.5
            },
            "cosmic_insights": ["purity", "new_beginning"]
        }
    ]

def get_mock_connections():
    """Returns mock connections for demo environment"""
    return [
        {
            "story_id": "demo1",
            "connected_story_id": "demo4", 
            "common_words": ["change", "life", "decision"],
            "strength": 0.7,
            "description": "Both stories talk about life changes"
        },
        {
            "story_id": "demo2",
            "connected_story_id": "demo4",
            "common_words": ["grandmother", "memories", "love"],
            "strength": 0.8,
            "description": "Grandmother's memories connect these stories"
        },
        {
            "story_id": "demo3", 
            "connected_story_id": "demo5",
            "common_words": ["silence", "peaceful", "reflection"],
            "strength": 0.6,
            "description": "Both seek peace and silence"
        }
    ]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 