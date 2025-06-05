#!/usr/bin/env python3
"""Create stories properly by building conversation context correctly"""

import requests
import time
import json

BASE_URL = "http://localhost:8080"

# User data from our previous script
USERS = [
    {"user_id": "user_51843", "name": "Alex Rivera", "scenario": "First Job Anxiety & Imposter Syndrome"},
    {"user_id": "user_35946", "name": "Jordan Chen", "scenario": "Social Media vs Real Life Authenticity"},
    {"user_id": "user_42869", "name": "Sam Taylor", "scenario": "Modern Dating & Vulnerability"},
    {"user_id": "user_66639", "name": "Riley Kim", "scenario": "Anxiety & Self-Discovery"},
    {"user_id": "user_36196", "name": "Casey Morgan", "scenario": "Family Expectations vs Personal Dreams"}
]

# High-impact emotional messages designed to trigger story creation
CONVERSATION_SEQUENCES = [
    # Alex Rivera - Job Anxiety
    [
        "I start my first 'real' job tomorrow and I'm literally shaking",
        "Everyone there has years of experience and I barely graduated 3 months ago", 
        "I applied thinking I'd never get it, like it was practice... and somehow they said yes?",
        "I keep thinking they made a mistake or I lied on my resume somehow",
        "My mom keeps saying 'fake it till you make it' but I'm tired of feeling fake",
        "What if I just ask questions instead of pretending I know everything?",
        "Actually, maybe they hired me because I can learn, not because I already know everything",
        "This whole experience is teaching me that vulnerability might actually be strength"
    ],
    
    # Jordan Chen - Social Media
    [
        "I deleted Instagram today and I feel like I'm having withdrawals",
        "I spent 3 hours last night scrolling through everyone's perfect lives",
        "I was looking for proof that I'm not the only one struggling to figure life out",
        "But all I found were engagement photos, dream jobs, perfect bodies",
        "I feel like I'm failing at being 23, like everyone got a manual I never received",
        "I just want to be real but 'real' doesn't get likes, you know?",
        "Maybe authentic moments matter more than perfect posts",
        "For the first time, I'm choosing my real messy life over the highlight reel"
    ],
    
    # Sam Taylor - Dating & Vulnerability  
    [
        "I think I sabotaged another potentially good relationship",
        "They said they really liked me and wanted to be exclusive",
        "I panicked and said I need space to think about it",
        "What if they actually get to know me and realize I'm not that interesting?",
        "I always do this - I push people away before they can leave",
        "My dad left when I was 12 and I guess I learned that people leave",
        "But this person... they text back fast, they remember what I say",
        "Maybe it's terrifying but also worth the risk to let someone actually see me",
        "I think I'm ready to try being vulnerable instead of just protecting myself"
    ],
    
    # Riley Kim - Anxiety
    [
        "I had my first panic attack in public yesterday",
        "I was in the grocery store checkout line and suddenly couldn't breathe",
        "The cashier was slow and people were lining up behind me judging me",
        "I've been having these moments where I feel like everyone's watching me",
        "It started when I began college - everything feels so intense and fast", 
        "I'm exhausted from pretending I have it together when I'm drowning",
        "Maybe I should tell my roommate I'm struggling instead of hiding",
        "I'm realizing that anxiety isn't weakness - it's my mind trying to protect me",
        "What if vulnerability could actually connect me to people instead of isolating me?"
    ],
    
    # Casey Morgan - Family Dreams
    [
        "I told my parents I want to drop pre-med for art therapy",
        "My mom literally said 'we didn't sacrifice everything for you to throw it away'",
        "I felt like I'm ungrateful for everything they've done for me",
        "But I want to help people heal from trauma... isn't that still helping people?", 
        "I was in therapy after my brother's accident and art saved my life",
        "My parents see stability and prestige, but I see meaning and purpose",
        "Maybe I can show them research about art therapy outcomes",
        "I need to tell them the full story about how art therapy saved me",
        "This isn't about rejecting their dreams - it's about honoring my calling"
    ]
]

def send_conversation_with_context(user_id, user_name, scenario, messages):
    """Send conversation while building proper context"""
    print(f"\n🎭 {scenario}")
    print(f"👤 {user_name} ({user_id})")
    
    conversation_history = []
    story_created = False
    
    for i, message in enumerate(messages, 1):
        print(f"   💬 Message {i}: {message[:60]}...")
        
        # Send with full conversation context
        response = requests.post(f"{BASE_URL}/api/chat/message", 
            json={
                "message": message,
                "user_id": user_id,
                "conversation_history": conversation_history  # Include full history
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get('message', '')
            score = data.get('story_readiness_score', 0)
            recommendation = data.get('recommendation', 'unknown')
            
            print(f"      📊 Score: {score:.2f} | Rec: {recommendation}")
            
            # Update conversation history with both messages
            conversation_history.append({"role": "user", "content": message})
            if ai_response:
                conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Check if story was created
            if data.get('story_created'):
                print(f"      🎉 STORY CREATED: {data.get('story_title')}")
                story_created = True
                break
                
            # If we're at a high score but no story yet, send emotional trigger
            if i == len(messages) and score > 0.4 and not story_created:
                print(f"   💥 Final emotional trigger...")
                trigger_message = "This conversation has been life-changing. I feel like I finally understand myself and I'm ready to embrace who I really am."
                
                response = requests.post(f"{BASE_URL}/api/chat/message", 
                    json={
                        "message": trigger_message,
                        "user_id": user_id,
                        "conversation_history": conversation_history
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('story_created'):
                        print(f"      🎉 STORY CREATED: {data.get('story_title')}")
                        story_created = True
                    else:
                        print(f"      📊 Final score: {data.get('story_readiness_score', 0):.2f}")
        else:
            print(f"      ❌ Error: {response.status_code}")
        
        time.sleep(1.5)  # Brief pause between messages
    
    return story_created

def main():
    print("🚀 CREATING ENGAGING STORIES WITH PROPER CONTEXT")
    print("=" * 65)
    
    created_count = 0
    
    for i, (user, conversation) in enumerate(zip(USERS, CONVERSATION_SEQUENCES)):
        story_created = send_conversation_with_context(
            user['user_id'], 
            user['name'], 
            user['scenario'], 
            conversation
        )
        
        if story_created:
            created_count += 1
        
        if i < len(USERS) - 1:
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
        
        # Show newest stories
        print(f"\n📖 Latest stories:")
        for story in stories[-created_count:] if created_count > 0 else stories[-3:]:
            title = story.get('title', 'Untitled')
            author = story.get('author', 'Unknown')
            print(f"   • \"{title}\" by {author}")

if __name__ == "__main__":
    main() 