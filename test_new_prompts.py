#!/usr/bin/env python3
"""Test the updated, more natural story prompts"""

import requests
import json

BASE_URL = "http://localhost:8080"

def test_natural_story_generation():
    print("🎯 TESTING UPDATED NATURAL STORY PROMPTS")
    print("=" * 50)
    
    # Register a test user
    user_data = {
        "username": "TestUser",
        "email": "test.natural@example.com",
        "password": "testpass123"
    }
    
    # Register
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    if response.status_code in [200, 201]:
        user_info = response.json()
        user_id = user_info['user_id']
        print(f"✅ User registered: {user_id}")
    else:
        # Try login instead
        login_data = {"email": user_data["email"], "password": user_data["password"]}
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            user_info = response.json()
            user_id = user_info['user_id']
            print(f"✅ User logged in: {user_id}")
        else:
            print(f"❌ Failed to create/login user: {response.text}")
            return
    
    # Test conversation: typical young adult scenario about social media
    test_messages = [
        "I've been feeling really weird about social media lately",
        "Like I spend hours scrolling and then feel worse about myself afterward",
        "Everyone seems to have their life figured out and I'm just... here",
        "I know it's all fake but it still gets to me, you know?",
        "Maybe I should just delete Instagram but I'm scared I'll miss out on things",
        "I guess I'm realizing that I need to figure out what makes ME happy, not what looks good online"
    ]
    
    print(f"\n📱 Testing conversation about social media & self-worth")
    print(f"Messages to send: {len(test_messages)}")
    
    conversation_history = []
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n💬 Message {i}: {message}")
        
        # Send message with conversation history
        response = requests.post(f"{BASE_URL}/api/chat/message", 
            json={
                "message": message,
                "conversation_history": conversation_history
            },
            headers={"X-User-ID": user_id}
        )
        
        if response.status_code == 200:
            data = response.json()
            score = data.get('story_readiness_score', 0)
            assistant_response = data.get('message', '')
            
            print(f"   📊 Story readiness: {score:.2f}")
            print(f"   🤖 Response: {assistant_response[:100]}...")
            
            # Add to conversation history
            conversation_history.append({"role": "user", "content": message})
            conversation_history.append({"role": "assistant", "content": assistant_response})
            
            if data.get('story_created'):
                print(f"\n🎉 STORY CREATED!")
                print(f"   📖 Title: {data.get('story_title')}")
                
                # Get the full story details
                story_id = data.get('story_id')
                if story_id:
                    # Fetch the story to see the content
                    stories_response = requests.get(f"{BASE_URL}/api/stories")
                    if stories_response.status_code == 200:
                        stories = stories_response.json()
                        new_story = next((s for s in stories if s.get('id') == story_id), None)
                        if new_story:
                            print(f"\n📝 STORY CONTENT:")
                            print("-" * 30)
                            print(new_story.get('content', 'No content available'))
                            print("-" * 30)
                            
                            # Analyze the language style
                            content = new_story.get('content', '')
                            title = new_story.get('title', '')
                            
                            print(f"\n🔍 LANGUAGE ANALYSIS:")
                            print(f"   Title: '{title}'")
                            print(f"   Title style: {'✅ Natural' if not any(word in title.lower() for word in ['whisper', 'shadow', 'dance', 'thread', 'solace']) else '❌ Too poetic'}")
                            print(f"   First-person: {'✅ Yes' if content.count(' I ') > 2 else '❌ No'}")
                            print(f"   Conversational: {'✅ Yes' if any(phrase in content.lower() for phrase in ['i realized', 'i started', 'i learned', 'looking back', 'the thing is']) else '❌ No'}")
                            print(f"   Natural language: {'✅ Yes' if not any(word in content.lower() for word in ['profound', 'ethereal', 'whisper', 'embrace', 'unfolds']) else '❌ Too fancy'}")
                            
                break
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
    
    print(f"\n✅ Test completed!")

if __name__ == "__main__":
    test_natural_story_generation() 