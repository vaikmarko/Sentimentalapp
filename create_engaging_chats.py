#!/usr/bin/env python3
"""Create 5 engaging conversations for 16-30 year olds and generate stories from them"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8080"

# 5 engaging conversation scenarios for 16-30 year olds
ENGAGING_CHATS = [
    {
        "user_name": "Alex Rivera",
        "user_email": "alex.rivera.gen@example.com", 
        "scenario": "First Job Anxiety & Imposter Syndrome",
        "conversation": [
            {"role": "user", "content": "I start my first 'real' job tomorrow and I'm literally shaking"},
            {"role": "assistant", "content": "That's such a big moment! What's going through your mind right now?"},
            {"role": "user", "content": "Everyone there has years of experience and I barely graduated 3 months ago"},
            {"role": "assistant", "content": "It sounds like you're worried about fitting in. What drew you to this job in the first place?"},
            {"role": "user", "content": "I applied thinking I'd never get it, like it was practice... and somehow they said yes?"},
            {"role": "assistant", "content": "Wait, so they chose YOU out of all their candidates. What does that tell you?"},
            {"role": "user", "content": "I keep thinking they made a mistake or I lied on my resume somehow"},
            {"role": "assistant", "content": "That feeling has a name - imposter syndrome. But here's the thing..."},
            {"role": "user", "content": "My mom keeps saying 'fake it till you make it' but I'm tired of feeling fake"},
            {"role": "assistant", "content": "What if instead of faking confidence, you embraced being new? What would that look like?"},
            {"role": "user", "content": "Maybe... asking questions instead of pretending I know everything?"},
            {"role": "assistant", "content": "Exactly. Your questions might be exactly what they need to hear."}
        ]
    },
    
    {
        "user_name": "Jordan Chen", 
        "user_email": "jordan.socialanxiety@example.com",
        "scenario": "Social Media vs Real Life Authenticity",
        "conversation": [
            {"role": "user", "content": "I deleted Instagram today and I feel like I'm having withdrawals"},
            {"role": "assistant", "content": "What led you to delete it?"},
            {"role": "user", "content": "I spent 3 hours last night scrolling through everyone's perfect lives"},
            {"role": "assistant", "content": "Three hours... what were you looking for in those moments?"},
            {"role": "user", "content": "Honestly? Proof that I'm not the only one struggling to figure life out"},
            {"role": "assistant", "content": "But instead you found...?"},
            {"role": "user", "content": "Engagement photos, dream jobs, perfect bodies, 'living my best life' captions"},
            {"role": "assistant", "content": "How did that make you feel about your own life?"},
            {"role": "user", "content": "Like I'm failing at being 23. Like everyone got a manual I never received"},
            {"role": "assistant", "content": "What if I told you that feeling is more common than those posts suggest?"},
            {"role": "user", "content": "I just want to be real but 'real' doesn't get likes, you know?"},
            {"role": "assistant", "content": "What would 'real' look like for you if likes didn't matter?"},
            {"role": "user", "content": "Messy hair, failed attempts, small victories... actual human moments"},
            {"role": "assistant", "content": "Those sound like the moments that actually matter."}
        ]
    },
    
    {
        "user_name": "Sam Taylor",
        "user_email": "sam.dating.struggles@example.com", 
        "scenario": "Modern Dating & Vulnerability",
        "conversation": [
            {"role": "user", "content": "I think I sabotaged another potentially good relationship"},
            {"role": "assistant", "content": "What happened?"},
            {"role": "user", "content": "They said they really liked me and wanted to be exclusive"},
            {"role": "assistant", "content": "That sounds like good news. How did you respond?"},
            {"role": "user", "content": "I panicked and said I need space to think about it"},
            {"role": "assistant", "content": "What was scary about hearing that they liked you?"},
            {"role": "user", "content": "What if they actually get to know me and realize I'm not that interesting?"},
            {"role": "assistant", "content": "So you pushed them away before they could leave?"},
            {"role": "user", "content": "God, when you say it like that... yes. I do this every time"},
            {"role": "assistant", "content": "It sounds like you're protecting yourself. From what?"},
            {"role": "user", "content": "From being seen and then abandoned. My dad left when I was 12"},
            {"role": "assistant", "content": "That must have taught you that people leave, even when you care about them."},
            {"role": "user", "content": "But this person... they text back fast, they remember what I say"},
            {"role": "assistant", "content": "They're showing up. What would it mean to let them?"},
            {"role": "user", "content": "Terrifying. But maybe... worth the risk?"}
        ]
    },
    
    {
        "user_name": "Riley Kim",
        "user_email": "riley.mental.health@example.com",
        "scenario": "Anxiety & Self-Discovery", 
        "conversation": [
            {"role": "user", "content": "I had my first panic attack in public yesterday"},
            {"role": "assistant", "content": "That must have been really frightening. Are you okay now?"},
            {"role": "user", "content": "I was in the grocery store checkout line and suddenly couldn't breathe"},
            {"role": "assistant", "content": "What do you think triggered it?"},
            {"role": "user", "content": "The cashier was really slow and people were lining up behind me"},
            {"role": "assistant", "content": "It sounds like feeling trapped or judged might be difficult for you."},
            {"role": "user", "content": "I've been having these weird moments where I feel like everyone's watching me"},
            {"role": "assistant", "content": "When did you first start noticing these feelings?"},
            {"role": "user", "content": "Probably since starting college... everything feels so intense and fast"},
            {"role": "assistant", "content": "College is a huge transition. What's been the hardest part?"},
            {"role": "user", "content": "Pretending I have it together when I feel like I'm drowning"},
            {"role": "assistant", "content": "What would it look like to not have to pretend?"},
            {"role": "user", "content": "Maybe telling my roommate I'm struggling instead of hiding in my room"},
            {"role": "assistant", "content": "That vulnerability could be exactly what you both need."},
            {"role": "user", "content": "I never thought anxiety could teach me about connection"}
        ]
    },
    
    {
        "user_name": "Casey Morgan",
        "user_email": "casey.family.dreams@example.com",
        "scenario": "Family Expectations vs Personal Dreams",
        "conversation": [
            {"role": "user", "content": "I told my parents I want to drop pre-med for art therapy"},
            {"role": "assistant", "content": "That's a big conversation. How did they react?"},
            {"role": "user", "content": "My mom literally said 'we didn't sacrifice everything for you to throw it away'"},
            {"role": "assistant", "content": "That must have been painful to hear. How did those words land?"},
            {"role": "user", "content": "Like I'm ungrateful for everything they've done for me"},
            {"role": "assistant", "content": "But you're not throwing anything away, are you? You're choosing something."},
            {"role": "user", "content": "I want to help people heal from trauma... isn't that still helping people?"},
            {"role": "assistant", "content": "It sounds like you have a clear vision. What draws you to that specifically?"},
            {"role": "user", "content": "I was in therapy after my brother's accident and art saved my life"},
            {"role": "assistant", "content": "So this isn't just a career change - it's about purpose."},
            {"role": "user", "content": "My parents see stability and prestige. I see meaning"},
            {"role": "assistant", "content": "Both matter. How might you honor their concerns while staying true to your calling?"},
            {"role": "user", "content": "Maybe showing them research about art therapy outcomes... proving it's real"},
            {"role": "assistant", "content": "And what if you also told them the story about how art therapy saved you?"},
            {"role": "user", "content": "They've never heard me talk about the accident like that"}
        ]
    }
]

def create_user_and_conversation(chat_data):
    """Create a user and store their conversation directly in the database"""
    print(f"\n🎭 Creating scenario: {chat_data['scenario']}")
    print(f"👤 User: {chat_data['user_name']}")
    
    # 1. Register user
    register_data = {
        "username": chat_data['user_name'],
        "email": chat_data['user_email'],
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    if response.status_code not in [200, 201]:
        print(f"   ⚠️  Registration issue, trying login...")
    
    # 2. Login user
    login_data = {
        "email": chat_data['user_email'],
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"   ❌ Login failed: {response.text}")
        return None
        
    user_data = response.json()
    user_id = user_data['user_id']
    print(f"   ✅ User logged in: {user_id}")
    
    # 3. Store conversation directly via API
    conversation_data = {
        "user_id": user_id,
        "messages": chat_data['conversation'],
        "scenario": chat_data['scenario'],
        "created_at": datetime.now().isoformat()
    }
    
    # Store via a direct database insert endpoint (we'll need to create this)
    store_response = requests.post(f"{BASE_URL}/api/debug/store-conversation", 
        json=conversation_data
    )
    
    if store_response.status_code == 200:
        print(f"   💾 Conversation stored successfully")
    else:
        print(f"   ⚠️  Storing via chat messages instead...")
        # Fallback: use regular chat endpoint but faster
        for msg in chat_data['conversation']:
            if msg['role'] == 'user':
                requests.post(f"{BASE_URL}/api/chat/message", 
                    json={"message": msg['content']},
                    headers={"X-User-ID": user_id}
                )
                time.sleep(0.5)  # Quick succession
    
    return user_id

def trigger_story_generation(user_id, conversation):
    """Trigger story generation from the stored conversation"""
    print(f"   🎯 Triggering story generation...")
    
    # Send a final message that should trigger story creation
    final_message = "This has been such an important realization for me."
    
    response = requests.post(f"{BASE_URL}/api/chat/message", 
        json={"message": final_message},
        headers={"X-User-ID": user_id}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('story_created'):
            print(f"   🎉 Story created: {data.get('story_title')}")
            return data.get('story_id')
        else:
            print(f"   📊 Story readiness: {data.get('story_readiness_score', 'Unknown')}")
    
    return None

def main():
    print("🎨 CREATING 5 ENGAGING CONVERSATIONS FOR GEN-Z")
    print("=" * 60)
    
    created_stories = []
    
    for chat_data in ENGAGING_CHATS:
        user_id = create_user_and_conversation(chat_data)
        if user_id:
            story_id = trigger_story_generation(user_id, chat_data['conversation'])
            if story_id:
                created_stories.append({
                    'user': chat_data['user_name'],
                    'scenario': chat_data['scenario'],
                    'story_id': story_id
                })
        
        print("   ⏳ Cooling down...")
        time.sleep(3)  # Brief pause between users
    
    print(f"\n🎊 SUMMARY")
    print("=" * 30)
    print(f"✅ Created {len(created_stories)} engaging stories:")
    for story in created_stories:
        print(f"   📖 {story['scenario']} - {story['user']}")
    
    # Check final database state
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        stories = response.json()
        print(f"\n📊 Total stories now in database: {len(stories)}")

if __name__ == "__main__":
    main() 