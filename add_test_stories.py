import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Test stories data
stories = [
    {
        'title': 'Moving to San Francisco',
        'content': 'Today I finally made the move to San Francisco, and honestly, my emotions are all over the place. Three months ago, this felt like the right decision - a fresh start, new opportunities, distance from everything familiar. But now, standing in my empty apartment with just two suitcases and a potted plant, I am questioning everything. The apartment smells like fresh paint and possibility.\n\nI walked to the corner store earlier and the cashier spoke to me in English. When I responded, she smiled and said the best time to visit the Golden Gate is early morning when the fog hasn\'t rolled in yet. Tonight I\'ll order takeout from a restaurant I\'ve never heard of, probably get lost walking back, and fall asleep to unfamiliar sounds outside my window. And somehow, that feels like exactly where I need to be.',
        'author': 'Anna',
        'public': True,
        'createdFormats': ['linkedin_post', 'blog_post'],
        'availableFormats': [
            {
                'type': 'linkedin_post',
                'content': 'Big news: I\'ve officially made the move to San Francisco! 🌉\n\nThree months ago, this felt like the right decision. Today, standing in my empty apartment with just two suitcases and a potted plant, I\'m questioning everything... and somehow that feels exactly right.\n\nThe apartment smells like fresh paint and possibility. Tonight I\'ll order takeout from a restaurant I\'ve never heard of, probably get lost walking back, and fall asleep to unfamiliar sounds.\n\nSometimes the scariest decisions lead to the most beautiful beginnings. Here\'s to new chapters and unknown adventures! ✨\n\n#NewBeginnings #SanFrancisco #CareerMove #GrowthMindset #TakingRisks',
                'display': 'LinkedIn Post'
            },
            {
                'type': 'blog_post',
                'content': 'Moving to San Francisco: The Beautiful Terror of Starting Over\n\nThree months ago, when I accepted the job offer and started planning this move, everything felt clear. New city, new opportunities, fresh start. The decision made perfect sense on paper.\n\nToday, standing in my empty San Francisco apartment with nothing but two suitcases and a potted plant I somehow managed not to kill during the move, I\'m questioning everything. And you know what? That feels exactly right.\n\nThe apartment smells like fresh paint and possibility. It\'s smaller than my old place, more expensive, and the neighbors are strangers. But there\'s something electric about being somewhere completely new, where nobody knows your story yet.\n\nI walked to the corner store earlier - a simple errand that felt like an adventure. The cashier was friendly, told me the best time to see the Golden Gate Bridge is early morning before the fog rolls in. These small interactions feel precious when you\'re starting from scratch.\n\nTonight I\'ll order takeout from a restaurant I\'ve never heard of. I\'ll probably get lost walking back. I\'ll fall asleep to unfamiliar sounds outside my window. And somehow, all of that feels like exactly where I need to be.\n\nMoving across the country isn\'t just about changing your address. It\'s about giving yourself permission to become someone new, to write a different story. The uncertainty is terrifying and beautiful in equal measure.\n\nHere\'s to new beginnings and the courage to embrace the unknown.',
                'display': 'Blog Post'
            }
        ],
        'reactions': 42,
        'views': 156,
        'inInnerSpace': True,
        'inner_space_insights': ['New beginnings', 'Uncertainty and growth']
    },
    {
        'title': 'Why I Procrastinate Everything',
        'content': 'Again, I left an important project to the last minute. This pattern keeps repeating in my life, and I am starting to understand that it is not about time management but about fear. Fear of not being good enough, fear of failure, fear of perfectionism taking over my creativity.\n\nHere I am at 11:47 PM, staring at a project that was due three weeks ago. The familiar pit in my stomach, the racing thoughts, the desperate bargaining with time itself. Maybe the real issue isn\'t time management. Maybe it\'s fear - fear of not being good enough, of failing, of being seen as less than I pretend to be.',
        'author': 'Alex',
        'public': True,
        'createdFormats': [],
        'reactions': 28,
        'views': 93,
        'inInnerSpace': True,
        'inner_space_insights': ['Procrastination pattern', 'Fear of perfectionism']
    },
    {
        'title': 'A Perfect Sunday with Parents',
        'content': 'Today we walked together and talked about everything and nothing. My parents are getting older, and I notice the small changes - dad walks a bit slower, mom forgets small things. But their love remains constant, a warm embrace that makes everything feel safe.\n\nSome moments you know are special while they\'re happening. This morning was one of those. We sat on the back porch - all three of us squeezed onto the old swing Dad built twenty years ago. Normal, beautiful, forgettable conversation. But there was something in the golden morning light that made time feel suspended, precious.',
        'author': 'Sarah',
        'public': True,
        'createdFormats': [],
        'reactions': 67,
        'views': 234,
        'inInnerSpace': False,
        'inner_space_insights': ['Family bonds', 'Gratitude']
    },
    {
        'title': 'Breaking Up After Three Years',
        'content': 'We decided to go separate ways and it feels like the end of everything I knew, but also like a door opening to something I cannot see yet. Three years of shared dreams, inside jokes, and quiet Sunday mornings. Now I am learning to be myself again.\n\nWe sat on the couch where we\'d watched a thousand movies together, and somehow both knew what was coming. There were no dramatic fights, no betrayals, no villains in this story. Just two people who loved each other enough to let go. Grief is strange when there\'s no one to blame.',
        'author': 'Jordan',
        'public': True,
        'createdFormats': ['tweet', 'song', 'diary_entry'],
        'availableFormats': [
            {
                'type': 'tweet',
                'content': 'Three years of shared dreams, inside jokes, and quiet Sunday mornings. Today we said goodbye. 💔\n\nNo dramatic fights. No betrayals. No villains in this story. Just two people who loved each other enough to let go.\n\nGrief is strange when there\'s no one to blame.\n\n#Heartbreak #Growth #LettingGo',
                'display': 'Tweet'
            },
            {
                'type': 'song',
                'content': '🎵 Three Years (Letting Go)\n\n(Verse 1)\nWe sat on that old couch again\nWhere we\'d watched a thousand films\nBoth knowing what was coming\nBoth feeling time stand still\n\n(Chorus)\nThree years of Sunday mornings\nThree years of inside jokes\nNow I\'m learning to be me again\nSometimes love means letting go\n\n(Verse 2)\nNo fights, no betrayals here\nJust two hearts that grew apart\nGrief is strange when no one\'s wrong\nWhen breaking up\'s the kindest art\n\n(Chorus)\nThree years of Sunday mornings\nThree years of inside jokes\nNow I\'m learning to be me again\nSometimes love means letting go 🎵',
                'display': 'Song'
            },
            {
                'type': 'diary_entry',
                'content': 'Dear Diary,\n\nToday we officially ended three years together. I keep expecting to feel angry or betrayed, but there\'s just this strange, hollow sadness. We sat on our couch - the one we picked out together at IKEA, the one where we\'d spent countless Sunday mornings with coffee and crosswords.\n\n\"I think we both know,\" they said, and I did. We both did.\n\nIt\'s weird how you can love someone completely and still know it\'s time to let go. There are no villains in this story, no dramatic betrayals to point to. Just two people who grew in different directions.\n\nI\'m scared of learning to be myself again. For three years, I\'ve been half of \"us.\" Who am I when I\'m just... me?\n\nBut maybe that\'s the point. Maybe this is exactly what I need to find out.\n\nGrief is so much stranger when there\'s no one to blame.\n\n- Jordan',
                'display': 'Diary Entry'
            }
        ],
        'reactions': 91,
        'views': 387,
        'inInnerSpace': True,
        'inner_space_insights': ['Relationship endings', 'Personal growth', 'New beginnings']
    },
    {
        'title': 'My First Therapy Session',
        'content': 'I finally made that appointment I had been putting off for months. Sitting in that chair, I realized how much I had been carrying alone. The therapist asked simple questions that opened doors I did not even know existed. It is okay to not be okay.\n\nThe waiting room was nothing like I expected. Just soft lighting, plants that were actually thriving, and magazines that weren\'t from 2015. \'I\'m tired of being scared of my own life,\' I heard myself say. Walking out, I felt lighter but also raw, like I\'d just worked muscles I forgot I had.',
        'author': 'Marcus',
        'public': True,
        'createdFormats': ['fb_post', 'article', 'video'],
        'availableFormats': [
            {
                'type': 'fb_post',
                'content': 'Week 1 of therapy ✨\n\nTook me months to finally walk through those doors. Best decision I\'ve made in ages 🙌\n\nTurns out it\'s not about fixing what\'s \'wrong\' with you - it\'s about understanding the patterns you didn\'t even know existed.\n\nMy therapist asked one simple question that floored me: \'What would it feel like to focus on what you can control?\'\n\nMind. Blown. 🤯\n\n#TherapyWorks #MentalHealthMatters #SelfCare #GrowthMindset',
                'display': 'Facebook Post'
            },
            {
                'type': 'article',
                'content': 'Why I Finally Started Therapy at 30 (And Why I Wish I\'d Done It Sooner)\n\nFor months, I kept putting off that appointment. The familiar excuses: too busy, too expensive, maybe I can handle this on my own. But sitting in that therapist\'s chair for the first time, I realized how much I\'d been carrying alone.\n\nThe waiting room wasn\'t what I expected. No intimidating diplomas or leather couches. Just soft lighting, thriving plants, and magazines that weren\'t from 2015. When Dr. Kim asked, \'What brings you here today?\' all my prepared speeches evaporated.\n\n\'I\'m tired of being scared of my own life,\' I heard myself say.\n\nWe talked about patterns I didn\'t even know I had. The way I apologize for taking up space. How I plan conversations three moves ahead like chess games. The exhausting mental math I do before expressing any opinion.\n\n\'Anxiety often comes from trying to control outcomes we have no power over,\' she said. \'What would it feel like to focus on what you can control?\'\n\nWalking out, I felt lighter but also raw, like I\'d just worked muscles I forgot I had. Best investment I\'ve made in years.',
                'display': 'Article'
            },
            {
                'type': 'video',
                'content': 'VIDEO: \'My First Therapy Session - What I Wish I\'d Known\'\n\n[Scene: Comfortable setting, natural lighting]\n\n\'For months, I kept saying I should try therapy. Months. Of putting it off because... I don\'t know, I thought I could handle everything myself?\'\n\n[Cut to different angle]\n\n\'But last week, I finally walked into Dr. Kim\'s office and said the scariest words: I think I need help.\'\n\n[Text overlay: \'It\'s okay to ask for help\']\n\n\'The waiting room wasn\'t intimidating at all. Just... peaceful. And when she asked what brought me there, all my rehearsed explanations disappeared.\'\n\n[Close-up]\n\n\'I\'m tired of being scared of my own life,\' I said. And that\'s when I knew I was exactly where I needed to be.\'\n\n[End screen: \'Therapy isn\'t about being broken. It\'s about being human.\']',
                'display': 'Video Script'
            }
        ],
        'reactions': 123,
        'views': 527,
        'inInnerSpace': True,
        'inner_space_insights': ['Mental health awareness', 'Self-care journey']
    },
    {
        'title': 'Grandmothers Wisdom',
        'content': 'Before she passed, grandmother told me: "Life is like a garden. Some seasons are for planting, some for growing, some for harvesting, and some for resting. The secret is knowing which season you are in." Today, I finally understand what she meant.\n\nI was holding her hand in the hospital room, both of us knowing this was goodbye. \'Stop waiting for permission,\' she said. \'To live your life the way you want to.\' She died two days later, and I\'ve been thinking about those words ever since. This week I signed up for pottery classes, bought the expensive coffee, told my boss I disagreed with his decision.',
        'author': 'Emma',
        'public': True,
        'createdFormats': [],
        'reactions': 156,
        'views': 492,
        'inInnerSpace': False,
        'inner_space_insights': ['Wisdom', 'Life cycles', 'Family legacy']
    }
]

# Add stories to Firestore
for story in stories:
    story['timestamp'] = datetime.now()
    story['status'] = 'published'
    story['format'] = 'text'
    story['formatsGenerated'] = {}
    story['email'] = None
    story['userId'] = None
    
    doc_ref = db.collection('stories').add(story)
    print(f'Added story: {story["title"]}')

print('All test stories added successfully!') 