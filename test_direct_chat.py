#!/usr/bin/env python3
"""Direct test of chat endpoint to debug conversation storage and story generation"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_direct_conversation():
    print("🧪 TESTING DIRECT CONVERSATION")
    print("=" * 50)
    
    # Test user
    user_id = "test_user_debug"
    
    # Rich conversation that should trigger story generation
    messages = [
        "I just had the most incredible breakthrough in my life",
        "I've been struggling with self-doubt for years, always feeling like I wasn't good enough",
        "Today my mentor looked me in the eye and said something that changed everything",
        "She told me that my vulnerability isn't weakness - it's actually my greatest strength",
        "I realized I've been hiding the most authentic parts of myself",
        "For the first time in years, I feel like I can breathe and be truly myself"
    ]
    
    conversation_history = []
    
    for i, message in enumerate(messages, 1):
        print(f"\n📝 Sending message {i}: {message[:50]}...")
        
        # Send message to chat endpoint
        response = requests.post(f"{BASE_URL}/api/chat/message", 
            json={
                "message": message,
                "user_id": user_id,
                "conversation_history": conversation_history
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Response: {data.get('message', 'No message')[:50]}...")
            print(f"   📊 Story readiness: {data.get('story_readiness_score', 'Unknown')}")
            print(f"   🎯 Recommendation: {data.get('recommendation', 'Unknown')}")
            
            if data.get('story_created'):
                print(f"   🎉 STORY CREATED! ID: {data.get('story_id')}")
                print(f"   📖 Title: {data.get('story_title')}")
                return data.get('story_id')
            
            # Update conversation history for next message
            conversation_history.append({'role': 'user', 'content': message})
            if 'message' in data:
                conversation_history.append({'role': 'assistant', 'content': data['message']})
                
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
        
        time.sleep(2)  # Wait between messages
    
    print(f"\n❌ No story generated after {len(messages)} messages")
    return None

def check_database_after_test():
    print(f"\n🔍 CHECKING DATABASE AFTER TEST")
    print("=" * 50)
    
    # Check conversations
    response = requests.get(f"{BASE_URL}/api/debug/collections")
    if response.status_code == 200:
        data = response.json()
        conversations_count = data['collections']['conversations']['count']
        stories_count = data['collections']['stories']['count']
        
        print(f"📊 Conversations stored: {conversations_count}")
        print(f"📊 Stories stored: {stories_count}")
        
        if conversations_count > 0:
            print("✅ Conversations are being stored!")
        else:
            print("❌ Conversations are NOT being stored")
            
        if stories_count > 1:  # More than the original 1
            print("✅ New story was created!")
        else:
            print("❌ No new story was created")
    
    # Check specific stories
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        stories = response.json()
        print(f"📖 Stories in API: {len(stories)}")
        for story in stories:
            print(f"   - {story.get('title', 'No title')} by {story.get('author', 'Unknown')}")

if __name__ == "__main__":
    test_direct_conversation()
    check_database_after_test() 