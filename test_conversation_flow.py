#!/usr/bin/env python3
"""
Test script to simulate 5 different users with engaging conversations
and test the automatic story generation system.
"""

import requests
import json
import time
import uuid
from datetime import datetime

BASE_URL = "http://localhost:8080"

# 5 Different Test Users with Different Personality Types
TEST_USERS = [
    {
        "name": "Sarah Chen",
        "email": "sarah.test@example.com", 
        "personality": "ambitious_professional",
        "conversation_topic": "career_breakthrough"
    },
    {
        "name": "Marcus Thompson", 
        "email": "marcus.test@example.com",
        "personality": "reflective_parent",
        "conversation_topic": "parenting_moment"
    },
    {
        "name": "Elena Rodriguez",
        "email": "elena.test@example.com", 
        "personality": "creative_artist",
        "conversation_topic": "artistic_discovery"
    },
    {
        "name": "David Kim",
        "email": "david.test@example.com",
        "personality": "introspective_student", 
        "conversation_topic": "life_transition"
    },
    {
        "name": "Amara Johnson",
        "email": "amara.test@example.com",
        "personality": "empathetic_helper",
        "conversation_topic": "relationship_growth"
    }
]

# Engaging conversation scenarios for each user
CONVERSATION_SCENARIOS = {
    "career_breakthrough": [
        "I just had the most incredible meeting with my CEO today...",
        "I've been working on this project for 8 months, and honestly, there were times I wanted to give up",
        "Today she called me into her office and I thought I was in trouble", 
        "But she said the board was so impressed with my innovation strategy that they want to fast-track my promotion",
        "I literally started crying right there in her office",
        "Three years ago I was just an entry-level analyst feeling completely lost",
        "And now I'm going to be the youngest VP in the company's history",
        "I keep thinking about my immigrant parents who worked three jobs to put me through college",
        "They always believed in me even when I didn't believe in myself",
        "I can't wait to call them tonight and tell them their sacrifices weren't in vain"
    ],
    
    "parenting_moment": [
        "My 7-year-old daughter asked me something today that completely stopped me in my tracks",
        "We were walking to school and she suddenly said 'Daddy, why do you always look sad when you check your phone?'",
        "I realized she'd been watching me this whole time, seeing how I react to work emails and social media",
        "In that moment I saw myself through her eyes - constantly distracted, always somewhere else mentally", 
        "I knelt down right there on the sidewalk and put my phone in my backpack",
        "I told her 'You're right, and I'm going to do better'",
        "The rest of the walk we talked about clouds and her favorite butterflies",
        "I saw how her whole face lit up when she had my complete attention",
        "It made me realize how much presence matters more than productivity",
        "She's teaching me to be human again, one conversation at a time"
    ],
    
    "artistic_discovery": [
        "I've been painting for 15 years but today something magical happened",
        "I was working on what I thought would be just another landscape piece",
        "But as I mixed these colors - this deep turquoise with golden ochre - something shifted",
        "I started painting not what I saw, but what I felt",
        "The brush moved like it had its own consciousness", 
        "Three hours disappeared and when I stepped back, I barely recognized the canvas",
        "It wasn't a landscape anymore - it was pure emotion, pure energy",
        "I started crying because for the first time, I felt like a real artist",
        "Not someone trying to be an artist, but someone who IS an artist",
        "All those years of doubt and comparison just melted away in that moment"
    ],
    
    "life_transition": [
        "I'm 28 and I just realized I've been living someone else's life",
        "Everyone always told me I was 'so smart' so I became a lawyer like they expected",
        "But sitting in my corner office today, billing my 70th hour this week, I felt completely empty",
        "I keep thinking about this quote: 'The graveyard is full of unrealized dreams'",
        "I've been secretly taking online courses in environmental science for months",
        "What I really want is to work in conservation, maybe in Costa Rica or Kenya",
        "My parents invested so much in my education, and I'm terrified of disappointing them",
        "But I'm also terrified of being 40 and regretting that I never tried",
        "Today I submitted my first application to a wildlife research program",
        "I don't know if it's brave or foolish, but for the first time in years, I feel alive"
    ],
    
    "relationship_growth": [
        "My best friend and I had a fight six months ago and we hadn't spoken since",
        "It was one of those stupid arguments that spiraled into hurt feelings and stubborn pride",
        "Today I saw her at the coffee shop where we used to meet every Friday",
        "We made eye contact and I could see she was hurting just as much as I was",
        "Without thinking, I walked over and just said 'I miss you'",
        "She started crying and said 'I miss you too, I'm so sorry'",
        "We talked for three hours about everything - the fight, our fears, our growth",
        "I realized we were both so afraid of being vulnerable that we almost lost something precious",
        "She's been going through her own struggles and I wasn't there for her",
        "But maybe this break taught us both how to love each other better"
    ]
}

def register_user(user_data):
    """Register a new test user"""
    print(f"\n🔐 Registering user: {user_data['name']}")
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json={
        "email": user_data["email"],
        "password": "testpass123",
        "name": user_data["name"]
    })
    
    if response.status_code == 201:
        user_info = response.json()
        print(f"   ✅ User registered successfully: {user_info['user_id']}")
        return user_info['user_id']
    else:
        print(f"   ❌ Registration failed: {response.status_code} - {response.text}")
        return None

def send_message(user_id, message):
    """Send a chat message and return AI response"""
    print(f"   💬 User: {message}")
    
    response = requests.post(f"{BASE_URL}/api/chat/message", 
        json={
            "message": message,
            "user_id": user_id  # Also include in JSON body
        },
        headers={
            "X-User-ID": user_id,
            "Content-Type": "application/json"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        ai_response = data.get('message', '')
        
        # Wait a moment for processing
        time.sleep(2)
        
        if ai_response and ai_response != 'No response':
            print(f"   🤖 AI: {ai_response}")
            
            # Check if story generation was triggered
            if data.get('story_created'):
                print(f"   🎯 STORY GENERATED! ID: {data.get('story_id')}")
                return ai_response, data.get('story_id')
            else:
                analysis = data.get('recommendation', 'continue_conversation')
                print(f"   📊 Analysis: {analysis}")
                return ai_response, None
        else:
            print(f"   ⚠️  AI response was empty or not ready")
            return None, None
    else:
        print(f"   ❌ Message failed: {response.status_code} - {response.text}")
        return None, None

def get_user_stories(user_id):
    """Get all stories for a user"""
    response = requests.get(f"{BASE_URL}/api/stories", 
        headers={"X-User-ID": user_id}
    )
    
    if response.status_code == 200:
        return response.json()
    return []

def generate_format(story_id, format_type, user_id):
    """Generate a new format for a story"""
    print(f"   🎨 Generating {format_type} format for story {story_id}")
    
    response = requests.post(f"{BASE_URL}/api/stories/{story_id}/formats",
        json={"format_type": format_type},
        headers={"X-User-ID": user_id}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ {format_type.title()} format generated successfully")
        return data.get('content')
    else:
        print(f"   ❌ Format generation failed: {response.status_code}")
        return None

def test_user_conversation(user_data):
    """Test complete conversation flow for one user"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING USER: {user_data['name']} ({user_data['personality']})")
    print(f"📖 Scenario: {user_data['conversation_topic']}")
    print(f"{'='*60}")
    
    # Register user
    user_id = register_user(user_data)
    if not user_id:
        return None
    
    # Get conversation messages
    messages = CONVERSATION_SCENARIOS[user_data['conversation_topic']]
    story_id = None
    
    print(f"\n💭 Starting conversation...")
    
    # Send messages one by one with realistic delays
    for i, message in enumerate(messages, 1):
        print(f"\n📅 Message {i}/{len(messages)}:")
        ai_response, generated_story_id = send_message(user_id, message)
        
        if generated_story_id:
            story_id = generated_story_id
            print(f"   🎉 Story automatically generated after {i} messages!")
            break
        
        if ai_response is None:
            print(f"   ⚠️  No response received, waiting longer...")
            time.sleep(5)  # Wait longer if no response
            continue
        
        # Wait longer between messages to simulate real conversation
        if i < len(messages):
            print(f"   ⏳ Waiting for natural conversation flow...")
            time.sleep(8)  # Longer delay between messages
    
    # Check if story was generated
    if not story_id:
        print(f"\n📊 Conversation complete. Checking for stories...")
        stories = get_user_stories(user_id)
        if stories:
            story_id = stories[0]['id']
            print(f"   ✅ Found story: {story_id}")
        else:
            print(f"   ⚠️  No story generated yet")
    
    # Test format generation if story exists
    if story_id:
        print(f"\n🎨 Testing format generation...")
        formats_to_test = ['poem', 'instagram', 'article', 'video']
        
        for format_type in formats_to_test:
            content = generate_format(story_id, format_type, user_id)
            if content:
                print(f"   📝 {format_type.title()}: {content[:100]}...")
            time.sleep(0.5)
    
    return {
        'user_id': user_id,
        'story_id': story_id,
        'name': user_data['name'],
        'conversation_length': len(messages)
    }

def test_anonymous_access():
    """Test that anonymous users can read stories but not generate formats"""
    print(f"\n{'='*60}")
    print(f"🔒 TESTING ANONYMOUS ACCESS")
    print(f"{'='*60}")
    
    # Try to get stories without authentication
    print(f"\n📖 Testing story reading without auth...")
    response = requests.get(f"{BASE_URL}/api/stories")
    
    if response.status_code == 200:
        stories = response.json()
        print(f"   ✅ Anonymous users can read {len(stories)} stories")
        
        if stories:
            story_id = stories[0]['id']
            print(f"\n🎨 Testing format generation without auth...")
            
            # Try to generate format without authentication
            response = requests.post(f"{BASE_URL}/api/stories/{story_id}/formats",
                json={"format_type": "poem"}
            )
            
            if response.status_code == 401:
                print(f"   ✅ Anonymous format generation properly blocked (401)")
            else:
                print(f"   ❌ Anonymous format generation not blocked! Status: {response.status_code}")
    else:
        print(f"   ❌ Story reading failed: {response.status_code}")

def test_story_analysis():
    """Test story analysis on a sample conversation to debug scoring"""
    print("\n🔍 DEBUGGING STORY ANALYSIS")
    print("=" * 50)
    
    # Test with a rich conversation
    test_conversation = [
        {"role": "user", "content": "I just had the most incredible meeting with my CEO today..."},
        {"role": "assistant", "content": "That sounds significant! Tell me more."},
        {"role": "user", "content": "I've been working on this project for 8 months, and honestly, there were times I wanted to give up"},
        {"role": "assistant", "content": "That must have been challenging. What kept you going?"},
        {"role": "user", "content": "Today she called me into her office and I thought I was in trouble"},
        {"role": "assistant", "content": "That must have been nerve-wracking. What happened?"},
        {"role": "user", "content": "But she said the board was so impressed with my innovation strategy that they want to fast-track my promotion"},
        {"role": "assistant", "content": "What wonderful news! How did that make you feel?"},
        {"role": "user", "content": "I literally started crying right there in her office"},
        {"role": "assistant", "content": "That's such a powerful emotional response. What was going through your mind?"},
        {"role": "user", "content": "Three years ago I was just an entry-level analyst feeling completely lost"},
        {"role": "assistant", "content": "What a journey you've been on. How does it feel to reflect on that growth?"},
        {"role": "user", "content": "And now I'm going to be the youngest VP in the company's history"},
        {"role": "assistant", "content": "That's an extraordinary accomplishment! What does this mean to you?"},
        {"role": "user", "content": "I keep thinking about my immigrant parents who worked three jobs to put me through college"},
        {"role": "assistant", "content": "Their sacrifices must make this moment even more meaningful."},
        {"role": "user", "content": "They always believed in me even when I didn't believe in myself"},
        {"role": "assistant", "content": "That kind of unwavering support is so powerful."},
        {"role": "user", "content": "I can't wait to call them tonight and tell them their sacrifices weren't in vain"}
    ]
    
    # Test the analysis
    response = requests.post(f"{BASE_URL}/api/chat/message", 
        json={
            "message": "I can't wait to call them tonight and tell them their sacrifices weren't in vain",
            "user_id": "test_user_debug",
            "conversation_history": test_conversation[:-1]  # All but the last message
        },
        headers={
            "X-User-ID": "test_user_debug",
            "Content-Type": "application/json"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"📊 Story Readiness Score: {data.get('story_readiness_score', 'N/A')}")
        print(f"🎯 Recommendation: {data.get('recommendation', 'N/A')}")
        print(f"📝 AI Response: {data.get('message', 'N/A')[:100]}...")
        print(f"✨ Story Created: {data.get('story_created', False)}")
        
        if data.get('knowledge_insights'):
            insights = data['knowledge_insights']
            print(f"🧠 Domains: {insights.get('primary_domains', [])}")
            print(f"🎭 Themes: {insights.get('themes_detected', [])}")
            print(f"💭 Emotional Markers: {insights.get('emotional_markers', [])}")
    else:
        print(f"❌ Analysis failed: {response.status_code} - {response.text}")

def main():
    """Run complete conversation flow test"""
    print(f"🚀 STARTING COMPREHENSIVE CONVERSATION FLOW TEST")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Test each user
    for user_data in TEST_USERS:
        result = test_user_conversation(user_data)
        if result:
            results.append(result)
        print(f"\n⏳ Waiting before testing next user...")
        time.sleep(10)  # Longer pause between users
    
    # Test anonymous access
    test_anonymous_access()
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    print(f"👥 Users tested: {len(results)}")
    stories_generated = len([r for r in results if r['story_id']])
    print(f"📚 Stories generated: {stories_generated}/{len(results)}")
    
    print(f"\n📝 DETAILED RESULTS:")
    for result in results:
        status = "✅ Story generated" if result['story_id'] else "⚠️  No story"
        print(f"   {result['name']}: {status}")
    
    # Final check - get all stories
    print(f"\n🔍 Final verification...")
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        all_stories = response.json()
        print(f"   📊 Total stories in database: {len(all_stories)}")
        
        for story in all_stories:
            print(f"   📖 '{story.get('title', 'Untitled')}' by {story.get('author', 'Unknown')}")
            formats = story.get('createdFormats', {})
            if formats:
                format_list = [f for f, available in formats.items() if available]
                print(f"      🎨 Available formats: {', '.join(format_list)}")
    
    print(f"\n✅ TEST COMPLETE!")

if __name__ == "__main__":
    # Run the debug test first
    test_story_analysis()
    
    # Then run the main test
    main() 