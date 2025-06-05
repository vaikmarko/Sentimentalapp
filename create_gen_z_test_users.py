#!/usr/bin/env python3
"""
Create 10 Gen Z Test Users for Sentimental App
Generates realistic personas, authentic conversations, and stories
"""

import requests
import time
import json
from datetime import datetime, timedelta
import random

BASE_URL = "http://localhost:8080"

# Gen Z Test Users with Realistic Personas (Born 1997-2012, now 12-27 years old)
GEN_Z_USERS = [
    {
        "name": "Zoe Chen",
        "email": "zoe.chen.2001@gmail.com",
        "age": 23,
        "location": "San Francisco",
        "occupation": "UX Designer at startup",
        "personality": "Creative, anxious, socially conscious",
        "interests": ["digital art", "mental health", "climate activism", "K-pop"],
        "conversation_scenario": "struggling_with_imposter_syndrome",
        "conversation_topic": "feeling like a fraud at her new job despite being qualified"
    },
    {
        "name": "Marcus Rodriguez", 
        "email": "marcus.rod.2000@gmail.com",
        "age": 24,
        "location": "Austin",
        "occupation": "Content creator / part-time barista",
        "personality": "Optimistic, creative, financially stressed",
        "interests": ["gaming", "streaming", "music production", "crypto"],
        "conversation_scenario": "creator_burnout",
        "conversation_topic": "exhausted from constantly creating content and chasing algorithm"
    },
    {
        "name": "Aaliyah Johnson",
        "email": "aaliyah.j.1999@gmail.com", 
        "age": 25,
        "location": "Atlanta",
        "occupation": "Graduate student in Psychology",
        "personality": "Empathetic, studious, perfectionist",
        "interests": ["therapy", "reading", "yoga", "social justice"],
        "conversation_scenario": "academic_pressure",
        "conversation_topic": "overwhelmed by thesis work and comparing herself to other grad students"
    },
    {
        "name": "Jake Thompson",
        "email": "jake.t.2002@gmail.com",
        "age": 22,
        "location": "Portland",
        "occupation": "College senior studying Environmental Science",
        "personality": "Idealistic, passionate, sometimes pessimistic about future",
        "interests": ["hiking", "environmental activism", "indie music", "thrifting"],
        "conversation_scenario": "climate_anxiety",
        "conversation_topic": "feeling hopeless about climate change and career choices"
    },
    {
        "name": "Maya Patel",
        "email": "maya.patel.2001@gmail.com",
        "age": 23,
        "location": "New York",
        "occupation": "Software developer",
        "personality": "Logical, introverted, family-oriented",
        "interests": ["coding", "anime", "cooking", "personal finance"],
        "conversation_scenario": "family_expectations",
        "conversation_topic": "pressure from parents about marriage while she wants to focus on career"
    },
    {
        "name": "Tyler Brooks",
        "email": "tyler.b.1998@gmail.com",
        "age": 26,
        "location": "Denver",
        "occupation": "Marketing coordinator",
        "personality": "Social, ambitious, health-conscious",
        "interests": ["fitness", "travel", "networking", "photography"],
        "conversation_scenario": "quarter_life_crisis",
        "conversation_topic": "feeling stuck in routine and questioning life choices at 26"
    },
    {
        "name": "Luna Morales",
        "email": "luna.m.2003@gmail.com",
        "age": 21,
        "location": "Los Angeles", 
        "occupation": "College junior studying Film",
        "personality": "Artistic, sensitive, politically aware",
        "interests": ["filmmaking", "poetry", "social media", "vintage fashion"],
        "conversation_scenario": "creative_identity",
        "conversation_topic": "struggling to find her unique voice as an artist in saturated market"
    },
    {
        "name": "Ethan Kim",
        "email": "ethan.kim.2000@gmail.com",
        "age": 24,
        "location": "Seattle",
        "occupation": "Data analyst",
        "personality": "Analytical, quiet, thoughtful",
        "interests": ["tech", "board games", "philosophy", "coffee"],
        "conversation_scenario": "social_anxiety",
        "conversation_topic": "wanting deeper friendships but struggling with social connections post-college"
    },
    {
        "name": "Sage Williams",
        "email": "sage.w.2001@gmail.com", 
        "age": 23,
        "location": "Chicago",
        "occupation": "Non-profit program coordinator",
        "personality": "Compassionate, driven, idealistic",
        "interests": ["social work", "plant care", "meditation", "community organizing"],
        "conversation_scenario": "burnout_helping_others",
        "conversation_topic": "emotionally drained from constantly helping others, needs to help herself"
    },
    {
        "name": "River Jackson",
        "email": "river.j.1999@gmail.com",
        "age": 25,
        "location": "Nashville",
        "occupation": "Freelance graphic designer & musician",
        "personality": "Free-spirited, creative, financially unstable",
        "interests": ["music", "art", "spirituality", "nature"],
        "conversation_scenario": "gig_economy_stress",
        "conversation_topic": "tired of unstable income and wondering if they should get a 'real job'"
    }
]

# Realistic Gen Z Conversation Templates
CONVERSATION_SCENARIOS = {
    "struggling_with_imposter_syndrome": [
        "I got promoted to senior UX designer at my startup and honestly? I feel like I'm going to be found out as a total fraud any day now.",
        "Everyone else seems so confident in meetings and I'm just sitting there like... do they actually know I have no idea what I'm doing half the time?",
        "My manager keeps praising my work but I can't shake this feeling that I just got lucky and soon they'll realize I don't belong here.",
        "I literally Google basic design principles that I should definitely know by now. What if they find out?",
        "The worst part is I worked so hard to get here, but now that I'm here I just feel like an imposter wearing a designer costume."
    ],
    
    "creator_burnout": [
        "I started my YouTube channel because I loved making content, but now it feels like a second job I can't escape.",
        "The algorithm is so unpredictable - one video gets 50K views, the next gets 200. It's like gambling with my mental health.",
        "I feel like I have to be 'on' all the time. Even when I'm just living my life, I'm thinking about what would make good content.",
        "My friends think being a content creator is just playing games and making easy money, but honestly? It's exhausting.",
        "I want to take a break but if I stop posting for even a week, my engagement drops and I lose followers. It's like being trapped."
    ],
    
    "academic_pressure": [
        "I'm supposed to be writing my thesis but every time I sit down to work on it, I just stare at the blank page and panic.",
        "Everyone in my program seems to have their research figured out and I'm still questioning if my topic is even worth studying.",
        "My advisor keeps asking for updates and I just keep making excuses because I'm too embarrassed to admit I'm completely stuck.",
        "I see other grad students publishing papers and presenting at conferences and I feel like I'm so behind.",
        "Sometimes I wonder if I'm even smart enough for this or if I just got into grad school by accident."
    ],
    
    "climate_anxiety": [
        "I'm studying environmental science but the more I learn, the more hopeless I feel about the future of our planet.",
        "How am I supposed to plan a career when it feels like the world might be uninhabitable in 20 years?",
        "Everyone my age is making plans for their future and I'm like... what future? Are we all just pretending everything is fine?",
        "I want to make a difference but individual actions feel so pointless compared to what corporations are doing.",
        "Sometimes I think I should just give up on environmental work and make money while I can, but that feels like selling out."
    ],
    
    "family_expectations": [
        "My parents keep asking when I'm going to 'settle down' and get married, but I'm 23 and barely figured out my career.",
        "They see my friends getting engaged and they're like 'when is it your turn?' Um, never maybe? I have goals that don't involve a husband.",
        "I love my family but they have this whole timeline mapped out for my life and none of it is what I actually want.",
        "They worked so hard to give me opportunities they never had, but now they want me to choose the safe traditional path anyway.",
        "How do I explain that I want to be financially independent and travel and maybe never have kids without breaking their hearts?"
    ],
    
    "quarter_life_crisis": [
        "I'm 26 and I feel like I should have my life figured out by now, but I wake up every day wondering if this is really what I want.",
        "My job pays well but I'm just going through the motions. Wake up, work, Netflix, sleep, repeat. Is this really adult life?",
        "All my friends seem to have found their 'thing' - their passion, their purpose. I'm still searching and it's getting embarrassing.",
        "I keep thinking I should make a big change but what if I give up something stable for something that doesn't work out?",
        "My teenage self had so many dreams and ambitions. Current me just wants to figure out what makes me happy."
    ],
    
    "creative_identity": [
        "I want to be a filmmaker but literally everyone in LA wants to be a filmmaker. How do I stand out when there are millions of people with the same dream?",
        "I see all these young creators on TikTok who are already famous and successful and I'm like... am I too late? Am I already behind?",
        "My professors keep telling us to 'find our voice' but what if my voice isn't unique or interesting enough?",
        "I love creating but the industry is so brutal and competitive. Sometimes I wonder if I should have chosen something more practical.",
        "I want to make art that matters, but I also need to pay rent. How do you balance artistic integrity with actually making money?"
    ],
    
    "social_anxiety": [
        "College was easy because I was surrounded by people my age all the time, but now I work remotely and I barely talk to anyone.",
        "I want deeper friendships but I never know how to take relationships past small talk without feeling weird about it.",
        "Everyone seems to have their friend groups already established and I'm the awkward person trying to break in at 24.",
        "I see people on social media hanging out with big groups of friends and I'm like... how do you even organize that? How do you become that social?",
        "I'm good at my job and fine in professional settings, but casual social stuff makes me want to hide in my apartment forever."
    ],
    
    "burnout_helping_others": [
        "I work at a non-profit helping vulnerable populations and I love the mission, but I'm emotionally drained all the time.",
        "I feel guilty taking time for myself when there are people who need help, but I'm running on empty.",
        "My friends and family always come to me with their problems because I'm 'good at listening' but who do I talk to?",
        "I chose this work because I want to make a difference, but how can I help others when I can barely help myself?",
        "Everyone always says 'you can't pour from an empty cup' but somehow I keep trying to anyway."
    ],
    
    "gig_economy_stress": [
        "I love being a freelancer because I have creative freedom, but the financial instability is killing me.",
        "Some months I make great money, other months I can barely pay rent. How do you plan a future with that kind of uncertainty?",
        "My parents keep asking when I'm going to get a 'real job' and honestly? Sometimes I wonder the same thing.",
        "I see my friends with steady salaries and benefits and I'm jealous, but I also can't imagine sitting in an office all day.",
        "I want to be an artist but I also want to feel financially secure. Why does it feel like I have to choose between passion and stability?"
    ]
}

def register_user(user_data):
    """Register a single user and return user_id"""
    print(f"👤 Registering {user_data['name']} ({user_data['age']}, {user_data['location']})...")
    
    payload = {
        'email': user_data['email'],
        'password': 'testpass123',
        'name': user_data['name']
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", 
                               json=payload, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 201:
            data = response.json()
            user_id = data['user_id']
            print(f"   ✅ {user_data['name']} registered successfully (ID: {user_id})")
            return user_id
        elif response.status_code == 409:
            # User exists, try to login
            print(f"   ⚠️  User {user_data['name']} already exists, logging in...")
            login_response = requests.post(f"{BASE_URL}/api/auth/login", 
                                         json={'email': user_data['email'], 'password': 'testpass123'})
            if login_response.status_code == 200:
                login_data = login_response.json()
                user_id = login_data['user_id']
                print(f"   ✅ {user_data['name']} logged in (ID: {user_id})")
                return user_id
        else:
            print(f"   ❌ Failed to register {user_data['name']}: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error registering {user_data['name']}: {e}")
        return None

def create_conversation(user_id, user_data):
    """Create a realistic conversation for the user"""
    print(f"   💬 Creating conversation for {user_data['name']}...")
    
    scenario = user_data['conversation_scenario']
    messages = CONVERSATION_SCENARIOS.get(scenario, [])
    
    if not messages:
        print(f"   ❌ No conversation template for scenario: {scenario}")
        return None
    
    # Build conversation with AI responses
    conversation = []
    
    # Add AI greeting
    conversation.append({
        'role': 'assistant',
        'content': f"Hi {user_data['name'].split()[0]}! I'm here to listen. What's on your mind today?",
        'timestamp': datetime.now().isoformat()
    })
    
    # Add user messages with realistic AI responses
    for i, user_message in enumerate(messages):
        # Add user message
        conversation.append({
            'role': 'user',
            'content': user_message,
            'timestamp': (datetime.now() + timedelta(minutes=i*2)).isoformat()
        })
        
        # Generate contextual AI response
        ai_response = generate_empathetic_response(user_message, scenario, i, len(messages))
        conversation.append({
            'role': 'assistant', 
            'content': ai_response,
            'timestamp': (datetime.now() + timedelta(minutes=i*2+1)).isoformat()
        })
    
    # Store conversation in database
    conversation_data = {
        'user_id': user_id,
        'messages': conversation,
        'scenario': scenario,
        'topic': user_data['conversation_topic'],
        'user_persona': {
            'age': user_data['age'],
            'location': user_data['location'],
            'occupation': user_data['occupation'],
            'personality': user_data['personality'],
            'interests': user_data['interests']
        },
        'created_at': datetime.now().isoformat()
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/debug/store-conversation", 
                               json=conversation_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            print(f"   ✅ Conversation stored for {user_data['name']} ({len(messages)} user messages)")
            return conversation
        else:
            print(f"   ❌ Failed to store conversation: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error storing conversation: {e}")
        return None

def generate_empathetic_response(user_message, scenario, message_index, total_messages):
    """Generate contextual AI responses based on scenario and conversation progress"""
    
    # Different response styles based on conversation progress
    if message_index == 0:  # First response - validating
        responses = {
            "struggling_with_imposter_syndrome": "That promotion is a huge accomplishment! It sounds like you're dealing with imposter syndrome, which is actually really common among high achievers. Can you tell me more about what specifically makes you feel like a fraud?",
            "creator_burnout": "It sounds like something you once loved has become a source of stress. That transition from passion to pressure is really difficult. What part of content creation used to bring you the most joy?",
            "academic_pressure": "Thesis writing can feel overwhelming, especially when it seems like everyone else has it figured out. That blank page can be intimidating. What drew you to your research topic originally?",
            "climate_anxiety": "It's understandable to feel overwhelmed when you're studying something that reveals such challenging realities. That knowledge can be a heavy burden. What made you choose environmental science despite knowing it would be difficult?",
            "family_expectations": "That pressure around timelines can be really frustrating, especially when your goals don't align with traditional expectations. It sounds like you have a clear vision for your life. What are those goals that feel most important to you?",
            "quarter_life_crisis": "That feeling of going through the motions is more common than you might think. It's actually a sign that you're growing and questioning what fulfillment means to you. What did bring you joy before this routine set in?",
            "creative_identity": "Finding your unique voice in a saturated field is challenging, but the fact that you're thinking about it shows you care about authenticity. What kind of stories do you find yourself naturally drawn to tell?",
            "social_anxiety": "The transition from college social structures to adult friendships is really hard. Many people struggle with this but don't talk about it openly. What kind of connections are you hoping to build?",
            "burnout_helping_others": "It takes a lot of emotional strength to work in helping professions. That feeling of running on empty while caring for others is a real challenge. When did you first notice yourself feeling drained?",
            "gig_economy_stress": "The uncertainty of freelance work can be really stressful, even when you love the freedom it provides. That tension between passion and stability is tough to navigate. What aspects of freelancing do you value most?"
        }
        return responses.get(scenario, "I hear you. That sounds really challenging. Can you tell me more about what you're experiencing?")
    
    elif message_index == 1:  # Second response - exploring deeper
        responses = {
            "struggling_with_imposter_syndrome": "It's interesting that you mention googling basic concepts - that actually shows you're committed to doing good work! Sometimes our inner critic is much harsher than reality. Have there been any moments where you felt confident in your abilities?",
            "creator_burnout": "The algorithm pressure is real - it's like trying to please a system that's constantly changing. That feeling of being 'on' all the time sounds exhausting. Do you remember what creating content felt like before it became about numbers?",
            "academic_pressure": "Comparing ourselves to other grad students is so natural but usually not very accurate. We see their highlights, not their struggles. What would feel like a small, manageable step forward with your thesis?",
            "climate_anxiety": "That feeling of hopelessness in the face of such a massive problem makes complete sense. It shows how much you care. Are there any small-scale environmental efforts that have given you hope?",
            "family_expectations": "It sounds like you really love your family but need them to understand your perspective. Those conversations about different life paths can be difficult. Have you been able to share any of your goals with them?",
            "quarter_life_crisis": "Those dreams and ambitions from your teenage self are still part of you. Sometimes we just need to reconnect with what excited us. What were some of those things you were passionate about before?",
            "creative_identity": "The pressure to be original can actually block creativity sometimes. What if finding your voice is less about being completely unique and more about being authentically you? What themes naturally appear in your work?",
            "social_anxiety": "Professional confidence and social confidence are different skills, and it's totally normal to be strong in one area. Small talk to deeper connection is a transition many people struggle with. What feels most natural to you in conversations?",
            "burnout_helping_others": "Being the person others turn to is both a gift and a burden. It shows your compassion but can leave you depleted. Who are the people in your life who pour back into you?",
            "gig_economy_stress": "That monthly income roller coaster would stress anyone out. Planning for the future feels impossible with that kind of uncertainty. Have you found any strategies that help with the financial unpredictability?"
        }
        return responses.get(scenario, "That's a really insightful observation. It sounds like you're really self-aware about what you're experiencing. How has this been affecting other areas of your life?")
    
    elif message_index >= total_messages - 2:  # Near end - towards resolution/growth
        responses = {
            "struggling_with_imposter_syndrome": "What you're describing sounds like growth, not fraud. You're in a position where you're learning and being challenged - that's exactly where growth happens. Your promotion wasn't an accident; someone saw your potential and your work.",
            "creator_burnout": "It sounds like taking a step back to remember why you started might be important. Your worth isn't determined by algorithm metrics, and real creativity often needs space to breathe. What would feel sustainable?",
            "academic_pressure": "Every researcher has felt stuck and questioned their work - it's part of the process, not a sign of failure. Your topic matters because it matters to you. What's one small thing you could do today to move forward?",
            "climate_anxiety": "Your feelings about the environment show how much you care, and that caring is exactly what the world needs. Meaningful change often starts with people who feel deeply about problems. How might you channel that care into action?",
            "family_expectations": "Your path doesn't have to look like anyone else's timeline. Living authentically, even when it's different from expectations, often leads to the most fulfilling life. What would feel true to you?",
            "quarter_life_crisis": "Questioning your path at 26 isn't falling behind - it's wisdom. Many people who seem to 'have it figured out' are also still exploring. What feels like the next small step toward something that excites you?",
            "creative_identity": "Your unique perspective is exactly what makes your art valuable. The market isn't as saturated with YOUR voice as you might think. What story do you want to tell that only you can tell?",
            "social_anxiety": "Connection is a skill that gets easier with practice, and many people feel the same way you do. What if you focused on one genuine connection rather than trying to build a whole social circle at once?",
            "burnout_helping_others": "Taking care of yourself isn't selfish - it's necessary for you to continue caring for others effectively. What would help you feel supported and restored?",
            "gig_economy_stress": "There might be ways to combine the freedom you love with more stability. What if the choice isn't all-or-nothing between passion and security? What would a hybrid approach look like?"
        }
        return responses.get(scenario, "You've shared something really meaningful here. It sounds like you're at a point where you're ready to think about what comes next. What feels like the most important insight from our conversation?")
    
    else:  # Middle responses - supportive and exploratory
        supportive_responses = [
            "That makes so much sense given what you're dealing with. You're really being honest with yourself about this.",
            "I can hear how much this matters to you. It's clear you care deeply about doing the right thing.",
            "What you're experiencing is really valid. Many people struggle with this but don't talk about it openly.",
            "It sounds like you're at a crossroads and trying to figure out what direction feels right.",
            "You're showing a lot of self-awareness by recognizing these patterns. That's actually a strength."
        ]
        return random.choice(supportive_responses)

def trigger_story_generation(user_id, user_data, conversation):
    """Attempt to trigger story generation from the conversation"""
    print(f"   📖 Attempting story generation for {user_data['name']}...")
    
    # Find the most story-worthy user messages
    user_messages = [msg for msg in conversation if msg['role'] == 'user']
    
    if len(user_messages) >= 3:
        # Take the most substantial message content
        story_content = " ".join([msg['content'] for msg in user_messages])
        
        try:
            # Use the chat endpoint to trigger story detection
            final_message = f"I think I'm ready to turn this into something I can keep and reflect on. This conversation has helped me understand {user_data['conversation_topic']} better."
            
            response = requests.post(f"{BASE_URL}/api/chat/message", 
                                   json={
                                       'message': final_message,
                                       'user_id': user_id,
                                       'conversation_history': conversation[:-1]  # Exclude last message
                                   },
                                   headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                result = response.json()
                if 'story_created' in result or 'story' in result:
                    print(f"   ✅ Story generated for {user_data['name']}")
                    return result
                else:
                    print(f"   📝 Response generated, checking for stories manually...")
                    return result
            else:
                print(f"   ❌ Story generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error in story generation: {e}")
            return None
    
    return None

def main():
    print("🚀 Creating 10 Gen Z Test Users for Sentimental App")
    print("=" * 60)
    print("🎯 Focus: Authentic Gen Z experiences with realistic scenarios")
    print("📱 Age range: 21-26 (core Gen Z)")
    print("💭 Scenarios: Real struggles, growth moments, and self-discovery")
    print("=" * 60)
    
    created_users = []
    successful_conversations = []
    generated_stories = []
    
    for i, user_data in enumerate(GEN_Z_USERS, 1):
        print(f"\n👤 [{i}/10] Processing {user_data['name']}...")
        print(f"   📍 {user_data['age']} years old, {user_data['occupation']} in {user_data['location']}")
        print(f"   🎭 Scenario: {user_data['conversation_scenario'].replace('_', ' ').title()}")
        
        # Register user
        user_id = register_user(user_data)
        if not user_id:
            continue
            
        created_users.append({
            'name': user_data['name'],
            'user_id': user_id,
            'email': user_data['email']
        })
        
        # Create conversation
        conversation = create_conversation(user_id, user_data)
        if conversation:
            successful_conversations.append({
                'name': user_data['name'],
                'user_id': user_id,
                'conversation_length': len([msg for msg in conversation if msg['role'] == 'user']),
                'scenario': user_data['conversation_scenario']
            })
            
            # Try to generate story
            story_result = trigger_story_generation(user_id, user_data, conversation)
            if story_result:
                generated_stories.append({
                    'name': user_data['name'],
                    'user_id': user_id,
                    'story_result': story_result
                })
        
        # Brief pause between users
        time.sleep(2)
    
    # Summary
    print(f"\n🎯 GENERATION SUMMARY")
    print("=" * 60)
    print(f"✅ Created users: {len(created_users)}/10")
    print(f"💬 Successful conversations: {len(successful_conversations)}/10")
    print(f"📖 Stories generated: {len(generated_stories)}/10")
    
    if created_users:
        print(f"\n👥 Created Users:")
        for user in created_users:
            print(f"   • {user['name']} ({user['email']}) - ID: {user['user_id']}")
    
    if successful_conversations:
        print(f"\n💭 Conversation Scenarios:")
        for conv in successful_conversations:
            print(f"   • {conv['name']}: {conv['scenario'].replace('_', ' ').title()} ({conv['conversation_length']} messages)")
    
    # Test API to see stories
    print(f"\n🔍 Checking stories API...")
    try:
        response = requests.get(f"{BASE_URL}/api/stories")
        if response.status_code == 200:
            stories = response.json()
            print(f"📊 API now returns {len(stories)} total stories")
            
            # Show recently created stories
            recent_stories = [s for s in stories if any(user['name'].split()[0] in s.get('author', '') for user in created_users)]
            if recent_stories:
                print(f"📚 Recent stories from our users:")
                for story in recent_stories[-5:]:  # Show last 5
                    print(f"   • {story.get('author', 'Unknown')}: {story.get('title', 'Untitled')}")
        else:
            print(f"❌ API check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking API: {e}")
    
    print(f"\n🎉 Gen Z test user creation complete!")
    print(f"💡 Next steps:")
    print(f"   1. Visit http://localhost:8080/app to see the users and conversations")
    print(f"   2. Test story generation and format creation")
    print(f"   3. Test the Discover feed with authentic Gen Z content")

if __name__ == "__main__":
    main() 