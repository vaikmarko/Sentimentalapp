#!/usr/bin/env python3
"""Test natural story generation with updated prompts through real API"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_natural_story_flow():
    print("🎯 TESTING NATURAL STORY GENERATION FLOW")
    print("=" * 50)
    
    # 1. Register a test user
    timestamp = str(int(time.time()))
    user_data = {
        "username": f"TestNatural{timestamp}",
        "email": f"test.natural{timestamp}@example.com",
        "password": "testpass123"
    }
    
    print("1️⃣ Registering user...")
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    if response.status_code in [200, 201]:
        user_info = response.json()
        user_id = user_info['user_id']
        print(f"✅ User registered: {user_id}")
    else:
        print(f"❌ Registration failed: {response.status_code}")
        return
    
    # 2. Simulate a natural conversation that should generate a story
    conversation_history = []
    messages = [
        "I had my first day at my new job today and I'm feeling really overwhelmed",
        "Everyone there seems so experienced and confident, and I feel like I don't belong",
        "I kept thinking they made a mistake hiring me",
        "But then my manager pulled me aside and said she was impressed with my questions",
        "She said asking good questions shows I'm thinking critically and want to learn",
        "Maybe I'm not as out of place as I thought"
    ]
    
    print(f"\n2️⃣ Sending {len(messages)} messages to build conversation...")
    
    for i, message in enumerate(messages, 1):
        print(f"   📝 Message {i}: {message[:50]}...")
        
        chat_data = {
            "message": message,
            "user_id": user_id,
            "conversation_history": conversation_history
        }
        
        response = requests.post(f"{BASE_URL}/api/chat/message", json=chat_data)
        
        if response.status_code == 200:
            result = response.json()
            
            # Add user message to history
            conversation_history.append({"role": "user", "content": message})
            
            # Add assistant response to history
            if result.get('message'):
                conversation_history.append({"role": "assistant", "content": result['message']})
            
            print(f"   ✅ Response: {result.get('message', 'No message')[:50]}...")
            print(f"   📊 Story readiness: {result.get('story_readiness_score', 0):.2f}")
            
            # Check if story was created
            if result.get('story_created'):
                print(f"\n🎉 STORY CREATED!")
                print(f"   📖 Title: '{result.get('story_title', 'Unknown')}'")
                print(f"   🆔 Story ID: {result.get('story_id', 'Unknown')}")
                
                # Get the actual story content
                story_id = result.get('story_id')
                if story_id:
                    story_response = requests.get(f"{BASE_URL}/api/stories")
                    if story_response.status_code == 200:
                        stories_data = story_response.json()
                        # Handle both direct list and nested structure
                        stories = stories_data if isinstance(stories_data, list) else stories_data.get('stories', [])
                        created_story = next((s for s in stories if s['id'] == story_id), None)
                        
                        if created_story:
                            print(f"\n📄 GENERATED STORY CONTENT:")
                            print("-" * 60)
                            print(created_story['content'])
                            print("-" * 60)
                            
                            # Analyze the language quality
                            analyze_story_language(created_story['title'], created_story['content'])
                        else:
                            print("   ⚠️ Story not found in database")
                
                break
            
        else:
            print(f"   ❌ Chat failed: {response.status_code}")
            
        time.sleep(0.5)  # Small delay between messages
    
    print(f"\n✅ Test completed!")

def analyze_story_language(title, content):
    """Analyze if the story uses natural, authentic language"""
    print(f"\n🔍 LANGUAGE ANALYSIS:")
    print(f"Title: '{title}'")
    
    # Title analysis
    poetic_words = ['whisper', 'shadow', 'dance', 'thread', 'solace', 'embrace', 'ethereal', 'profound', 'tapestry']
    title_natural = not any(word.lower() in title.lower() for word in poetic_words)
    print(f"   📋 Title Style: {'✅ Natural' if title_natural else '❌ Too poetic'}")
    
    # Content analysis
    first_person = content.count(' I ') >= 3 or content.lower().startswith('i ')
    print(f"   👤 First Person: {'✅ Yes' if first_person else '❌ No'}")
    
    conversational_phrases = ['i realized', 'i started', 'i learned', 'looking back', 'the thing is', 'i guess', 'i never thought', 'it\'s funny', 'i remember']
    conversational = any(phrase in content.lower() for phrase in conversational_phrases)
    print(f"   💬 Conversational: {'✅ Yes' if conversational else '❌ No'}")
    
    overly_fancy = ['profound', 'ethereal', 'whisper', 'embrace', 'unfolds', 'tapestry', 'essence', 'illuminated', 'symphony', 'resonance']
    natural_language = not any(word in content.lower() for word in overly_fancy)
    print(f"   🗣️  Natural Language: {'✅ Yes' if natural_language else '❌ Too fancy'}")
    
    # Word count
    word_count = len(content.split())
    print(f"   📊 Word Count: {word_count} ({'✅ Good' if 200 <= word_count <= 600 else '⚠️ Check length'})")
    
    # Overall score
    scores = [title_natural, first_person, conversational, natural_language]
    overall_score = sum(scores) / len(scores)
    print(f"   🏆 Overall Authenticity: {overall_score:.1%} ({'✅ Great' if overall_score >= 0.75 else '⚠️ Needs work' if overall_score >= 0.5 else '❌ Too formal'})")

if __name__ == "__main__":
    try:
        test_natural_story_flow()
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}") 