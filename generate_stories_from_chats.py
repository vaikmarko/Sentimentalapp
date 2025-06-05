#!/usr/bin/env python3
"""Send the stored conversations through chat API to trigger story generation"""

import requests
import time

BASE_URL = "http://localhost:8080"

# User IDs from the previous script
USERS = [
    {"user_id": "user_51843", "name": "Alex Rivera", "scenario": "First Job Anxiety & Imposter Syndrome"},
    {"user_id": "user_35946", "name": "Jordan Chen", "scenario": "Social Media vs Real Life Authenticity"},
    {"user_id": "user_42869", "name": "Sam Taylor", "scenario": "Modern Dating & Vulnerability"},
    {"user_id": "user_66639", "name": "Riley Kim", "scenario": "Anxiety & Self-Discovery"},
    {"user_id": "user_36196", "name": "Casey Morgan", "scenario": "Family Expectations vs Personal Dreams"}
]

# The conversations we created
CONVERSATIONS = [
    [
        "I start my first 'real' job tomorrow and I'm literally shaking",
        "Everyone there has years of experience and I barely graduated 3 months ago",
        "I applied thinking I'd never get it, like it was practice... and somehow they said yes?",
        "I keep thinking they made a mistake or I lied on my resume somehow",
        "My mom keeps saying 'fake it till you make it' but I'm tired of feeling fake",
        "Maybe... asking questions instead of pretending I know everything?"
    ],
    [
        "I deleted Instagram today and I feel like I'm having withdrawals",
        "I spent 3 hours last night scrolling through everyone's perfect lives",
        "Honestly? Proof that I'm not the only one struggling to figure life out",
        "Engagement photos, dream jobs, perfect bodies, 'living my best life' captions",
        "Like I'm failing at being 23. Like everyone got a manual I never received",
        "I just want to be real but 'real' doesn't get likes, you know?",
        "Messy hair, failed attempts, small victories... actual human moments"
    ],
    [
        "I think I sabotaged another potentially good relationship",
        "They said they really liked me and wanted to be exclusive",
        "I panicked and said I need space to think about it",
        "What if they actually get to know me and realize I'm not that interesting?",
        "God, when you say it like that... yes. I do this every time",
        "From being seen and then abandoned. My dad left when I was 12",
        "But this person... they text back fast, they remember what I say",
        "Terrifying. But maybe... worth the risk?"
    ],
    [
        "I had my first panic attack in public yesterday",
        "I was in the grocery store checkout line and suddenly couldn't breathe",
        "The cashier was really slow and people were lining up behind me",
        "I've been having these weird moments where I feel like everyone's watching me",
        "Probably since starting college... everything feels so intense and fast",
        "Pretending I have it together when I feel like I'm drowning",
        "Maybe telling my roommate I'm struggling instead of hiding in my room",
        "I never thought anxiety could teach me about connection"
    ],
    [
        "I told my parents I want to drop pre-med for art therapy",
        "My mom literally said 'we didn't sacrifice everything for you to throw it away'",
        "Like I'm ungrateful for everything they've done for me",
        "I want to help people heal from trauma... isn't that still helping people?",
        "I was in therapy after my brother's accident and art saved my life",
        "My parents see stability and prestige. I see meaning",
        "Maybe showing them research about art therapy outcomes... proving it's real",
        "They've never heard me talk about the accident like that"
    ]
]

def send_conversation_gradually(user_id, user_name, scenario, messages):
    """Send conversation messages gradually to build up story readiness"""
    print(f"\n🎭 {scenario}")
    print(f"👤 {user_name} ({user_id})")
    
    story_created = False
    
    for i, message in enumerate(messages, 1):
        print(f"   💬 Message {i}: {message[:50]}...")
        
        response = requests.post(f"{BASE_URL}/api/chat/message", 
            json={"message": message},
            headers={"X-User-ID": user_id}
        )
        
        if response.status_code == 200:
            data = response.json()
            score = data.get('story_readiness_score', 0)
            print(f"      📊 Story readiness: {score}")
            
            if data.get('story_created'):
                print(f"      🎉 STORY CREATED: {data.get('story_title')}")
                story_created = True
                break
        else:
            print(f"      ❌ Error: {response.status_code}")
        
        time.sleep(2)  # Wait between messages
    
    if not story_created:
        # Send a final emotional message to trigger story creation
        final_message = "This conversation has helped me understand myself so much better. I feel like I'm finally ready to embrace who I really am."
        print(f"   💬 Final trigger: {final_message[:50]}...")
        
        response = requests.post(f"{BASE_URL}/api/chat/message", 
            json={"message": final_message},
            headers={"X-User-ID": user_id}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('story_created'):
                print(f"      🎉 STORY CREATED: {data.get('story_title')}")
                story_created = True
            else:
                print(f"      📊 Final score: {data.get('story_readiness_score', 0)}")
    
    return story_created

def main():
    print("🚀 GENERATING STORIES FROM ENGAGING CONVERSATIONS")
    print("=" * 60)
    
    created_count = 0
    
    for i, (user, conversation) in enumerate(zip(USERS, CONVERSATIONS)):
        story_created = send_conversation_gradually(
            user['user_id'], 
            user['name'], 
            user['scenario'], 
            conversation
        )
        
        if story_created:
            created_count += 1
        
        if i < len(USERS) - 1:  # Don't wait after the last user
            print("   ⏳ Cooling down...")
            time.sleep(5)
    
    print(f"\n🎊 FINAL RESULTS")
    print("=" * 30)
    print(f"✅ Stories created: {created_count}/5")
    
    # Check final story count
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        stories = response.json()
        print(f"📚 Total stories in database: {len(stories)}")
        for story in stories[-5:]:  # Show last 5 stories
            print(f"   📖 \"{story.get('title', 'Untitled')}\" by {story.get('author', 'Unknown')}")

if __name__ == "__main__":
    main() 