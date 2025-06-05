import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Video-focused stories data
video_stories = [
    {
        'title': 'My Morning Routine That Changed Everything',
        'content': 'Six months ago, I was hitting snooze five times every morning, rushing to work with coffee-stained shirts and perpetual anxiety. Today, I woke up at 5:30 AM naturally, did 20 minutes of yoga, journaled for 10 minutes, and made a proper breakfast. The difference isn\'t just in my schedule - it\'s in how I feel about myself.\n\nIt started small. Instead of scrolling my phone the moment I woke up, I decided to keep it in another room. That one change created space for everything else. The yoga came next, then the journaling. Each habit built on the last one, creating this beautiful morning ritual that sets the tone for my entire day.\n\nPeople ask me how I stay motivated. The truth is, some mornings I don\'t want to get up. But I\'ve learned that motivation follows action, not the other way around. You start, and then you feel motivated to continue.',
        'author': 'Maya',
        'public': True,
        'createdFormats': ['video', 'article', 'instagram_reel', 'tiktok'],
        'reactions': 234,
        'views': 1247,
        'inInnerSpace': True,
        'cosmic_insights': ['Self-discipline', 'Habit formation', 'Personal transformation'],
        'video_metadata': {
            'duration': '3:45',
            'thumbnail': 'morning_routine_thumb.jpg',
            'video_type': 'lifestyle_vlog',
            'scenes': ['Bedroom wake-up', 'Yoga sequence', 'Kitchen breakfast prep', 'Journaling close-up'],
            'music': 'Uplifting acoustic guitar',
            'style': 'Cinematic handheld'
        }
    },
    {
        'title': 'The Day I Quit My Corporate Job',
        'content': 'This morning I walked into my corner office for the last time. Five years of 60-hour weeks, missed family dinners, and dreams deferred. As I cleaned out my desk, I found a sticky note from my first day: "Make them proud." I realized I\'d been trying to make everyone proud except myself.\n\nThe decision wasn\'t sudden. It was a slow burn that started when my nephew asked why I was always "too busy" to play with him. That question haunted me for months. I began asking myself: What am I building here? What legacy am I creating? The answers weren\'t pretty.\n\nTonight, I\'m cooking dinner for my family for the first time in months. Tomorrow, I start my freelance photography business. I\'m terrified and exhilarated in equal measure. But for the first time in years, I feel alive.',
        'author': 'David',
        'public': True,
        'createdFormats': ['video', 'linkedin_post', 'blog_post', 'podcast_script'],
        'reactions': 456,
        'views': 2134,
        'inInnerSpace': True,
        'cosmic_insights': ['Career transition', 'Work-life balance', 'Following dreams', 'Family priorities'],
        'video_metadata': {
            'duration': '5:22',
            'thumbnail': 'office_departure_thumb.jpg',
            'video_type': 'documentary_style',
            'scenes': ['Empty office', 'Desk cleanup', 'Elevator goodbye', 'Home cooking scene'],
            'music': 'Emotional piano melody',
            'style': 'Documentary handheld'
        }
    },
    {
        'title': 'Learning to Love My Body After 30',
        'content': 'I spent my twenties at war with my body. Counting calories, avoiding mirrors, wearing oversized clothes to hide. Yesterday, I wore a fitted dress to dinner and felt beautiful. Not because my body changed dramatically, but because my relationship with it transformed completely.\n\nThe shift happened gradually through therapy, self-compassion practice, and surrounding myself with people who love me for who I am, not how I look. I started focusing on what my body can do rather than what it looks like. This body carried me through marathons, hugged my friends through heartbreak, and danced at my sister\'s wedding.\n\nI\'m not saying I wake up loving everything about myself every day. But I\'ve learned to speak to myself with kindness, to nourish my body with good food and movement that feels joyful, and to appreciate the miracle of simply being alive in this skin.',
        'author': 'Sofia',
        'public': True,
        'createdFormats': ['video', 'instagram_story', 'blog_post', 'youtube_short'],
        'reactions': 789,
        'views': 3456,
        'inInnerSpace': True,
        'cosmic_insights': ['Body positivity', 'Self-acceptance', 'Mental health journey', 'Personal growth'],
        'video_metadata': {
            'duration': '4:18',
            'thumbnail': 'mirror_reflection_thumb.jpg',
            'video_type': 'personal_story',
            'scenes': ['Morning mirror', 'Wardrobe selection', 'Dinner preparation', 'Evening reflection'],
            'music': 'Soft indie folk',
            'style': 'Intimate close-ups'
        }
    },
    {
        'title': 'The Phone Call That Changed My Perspective',
        'content': 'At 2:47 AM, my phone rang. My college roommate, calling from a hospital in another state. Her mom had a stroke. As I listened to her broken voice, something shifted inside me. All my daily worries - the work deadline, the apartment mess, the text I hadn\'t returned - suddenly felt insignificant.\n\nI booked a flight that morning and spent three days in a hospital waiting room, watching my friend navigate the scariest moment of her life. Her mom recovered, thankfully, but those three days taught me more about what matters than the previous three years combined.\n\nNow when I catch myself spiraling about small things, I remember that waiting room. The way strangers became family. How "I love you" became the most important words in any language. How grateful I felt for every ordinary moment I\'d previously taken for granted.',
        'author': 'Alex',
        'public': True,
        'createdFormats': ['video', 'voice_note', 'article', 'podcast_episode'],
        'reactions': 567,
        'views': 2890,
        'inInnerSpace': True,
        'cosmic_insights': ['Perspective shift', 'Friendship bonds', 'Life priorities', 'Gratitude'],
        'video_metadata': {
            'duration': '6:33',
            'thumbnail': 'phone_call_thumb.jpg',
            'video_type': 'emotional_narrative',
            'scenes': ['Late night phone', 'Airport rush', 'Hospital corridor', 'Friend embrace'],
            'music': 'Minimal piano',
            'style': 'Cinematic storytelling'
        }
    },
    {
        'title': 'Teaching My Daughter to Ride a Bike',
        'content': 'For weeks, she\'d been asking, and for weeks, I\'d been saying "maybe tomorrow." Work was busy, the weather wasn\'t perfect, the bike needed adjusting. Today I realized I was the one who wasn\'t ready - not her.\n\nWe went to the park at sunset, just the two of us. She was fearless in the way only six-year-olds can be, determined to conquer this milestone. I held the back of her seat, running alongside as she pedaled, my heart bursting with pride and terror in equal measure.\n\nThen came the moment every parent knows is coming but isn\'t prepared for: I let go. She didn\'t notice at first, too focused on the path ahead. When she realized she was riding solo, her squeal of delight echoed across the park. In that moment, I understood what letting go really means - not abandonment, but trust in what you\'ve taught them.',
        'author': 'Michael',
        'public': True,
        'createdFormats': ['video', 'instagram_reel', 'facebook_post', 'family_blog'],
        'reactions': 892,
        'views': 4567,
        'inInnerSpace': False,
        'cosmic_insights': ['Parenting moments', 'Letting go', 'Childhood milestones', 'Father-daughter bond'],
        'video_metadata': {
            'duration': '3:28',
            'thumbnail': 'bike_lesson_thumb.jpg',
            'video_type': 'family_moment',
            'scenes': ['Park arrival', 'First attempts', 'The breakthrough', 'Celebration hug'],
            'music': 'Heartwarming strings',
            'style': 'Warm golden hour'
        }
    },
    {
        'title': 'My First Solo Trip at 45',
        'content': 'I\'ve never eaten alone in a restaurant. Never gone to a movie by myself. Never traveled anywhere without a companion. At 45, I realized I\'d never learned to enjoy my own company. So I booked a week in Iceland. Alone.\n\nThe first day was awkward. I felt self-conscious ordering dinner for one, taking selfies instead of asking strangers for photos. But by day three, something magical happened. I started talking to locals, exploring places that interested only me, eating when I was hungry instead of when someone else was.\n\nI hiked to a waterfall and sat in silence for an hour, something I\'d never done in my entire life. I watched the Northern Lights dance across the sky without needing to share the moment with anyone but myself. For the first time, I understood the difference between being alone and being lonely.',
        'author': 'Rachel',
        'public': True,
        'createdFormats': ['video', 'travel_vlog', 'blog_series', 'instagram_story'],
        'reactions': 345,
        'views': 1876,
        'inInnerSpace': True,
        'cosmic_insights': ['Solo travel', 'Self-discovery', 'Independence', 'Personal confidence'],
        'video_metadata': {
            'duration': '7:12',
            'thumbnail': 'iceland_aurora_thumb.jpg',
            'video_type': 'travel_documentary',
            'scenes': ['Airport departure', 'Restaurant solo dining', 'Waterfall hike', 'Northern Lights'],
            'music': 'Ambient Icelandic sounds',
            'style': 'Cinematic landscape'
        }
    }
]

# Add video stories to Firestore
for story in video_stories:
    story['timestamp'] = datetime.now()
    story['status'] = 'published'
    story['format'] = 'video'
    story['formatsGenerated'] = {}
    story['email'] = None
    story['userId'] = None
    
    doc_ref = db.collection('stories').add(story)
    print(f'Added video story: {story["title"]}')

print('All video stories added successfully!') 