#!/usr/bin/env python3
"""
Test script for the new Intelligent Conversation Engine
Tests the OpenAI-powered conversation system vs the old manual responses
"""

import os
import sys
import requests
import json
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8080"
TEST_USER_EMAIL = "intelligent-conversation-test@example.com"
TEST_USER_NAME = "Alex Test"

def test_conversation_quality():
    """Test the quality of conversations with the new intelligent engine"""
    
    print("🧠 Testing Intelligent Conversation Engine")
    print("=" * 50)
    
    # Register a test user
    print("📝 Registering test user...")
    register_response = requests.post(f"{BASE_URL}/api/auth/register", json={
        "email": TEST_USER_EMAIL,
        "password": "testpassword123",
        "name": TEST_USER_NAME
    })
    
    if register_response.status_code != 201:
        print(f"❌ Failed to register user: {register_response.status_code}")
        return False
    
    user_id = register_response.json()['user_id']
    print(f"✅ User registered: {user_id}")
    
    # Test different types of conversations
    test_conversations = [
        {
            "name": "Simple Greeting",
            "messages": ["Hi there, how are you doing today?"],
            "expected_quality": "Should be warm and engaging, not robotic"
        },
        {
            "name": "Work Stress",
            "messages": [
                "I've been really stressed at work lately",
                "My boss keeps giving me impossible deadlines and I feel overwhelmed"
            ],
            "expected_quality": "Should show empathy and ask thoughtful follow-up questions"
        },
        {
            "name": "Personal Growth",
            "messages": [
                "I've been thinking a lot about my life direction",
                "I feel like I'm at a crossroads and need to make some big decisions"
            ],
            "expected_quality": "Should encourage reflection and deeper exploration"
        },
        {
            "name": "Story-Worthy Experience",
            "messages": [
                "Something incredible happened to me yesterday",
                "I was walking home from work when I saw an elderly man fall down. I helped him up and we started talking. Turns out he was a Holocaust survivor with the most amazing stories. We talked for two hours and he invited me for dinner next week. It made me realize how much wisdom is all around us if we just take time to connect."
            ],
            "expected_quality": "Should recognize story potential and help explore the deeper meaning"
        }
    ]
    
    conversation_history = []
    
    for i, test_case in enumerate(test_conversations, 1):
        print(f"\n🎭 Test {i}: {test_case['name']}")
        print(f"Expected: {test_case['expected_quality']}")
        print("-" * 40)
        
        for message in test_case['messages']:
            print(f"👤 User: {message}")
            
            # Add to conversation history
            conversation_history.append({"role": "user", "content": message})
            
            # Send to chat API
            response = requests.post(f"{BASE_URL}/api/chat/message", json={
                "message": message,
                "user_id": user_id,
                "conversation_history": conversation_history[:-1]  # Exclude current message
            })
            
            if response.status_code in [200, 201]:
                result = response.json()
                bot_message = result.get('message', '')
                
                print(f"🤖 Bot: {bot_message}")
                
                # Add bot response to history
                conversation_history.append({"role": "assistant", "content": bot_message})
                
                # Check if story was created
                if result.get('story_created'):
                    print(f"📚 Story Created: {result.get('story_id')}")
                    print(f"   Score: {result.get('story_readiness_score', 'N/A')}")
                
                # Analyze response quality
                analyze_response_quality(bot_message, test_case['expected_quality'])
                
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return False
    
    print("\n" + "=" * 50)
    print("✅ Intelligent Conversation Engine Test Complete!")
    return True

def analyze_response_quality(response, expected_quality):
    """Analyze the quality of the bot response"""
    
    quality_indicators = {
        "empathy": ["feel", "understand", "sounds", "hear", "appreciate"],
        "curiosity": ["what", "how", "why", "tell me", "curious", "wonder"],
        "engagement": ["interesting", "fascinating", "love", "appreciate", "thank you"],
        "reflection": ["think", "reflect", "consider", "explore", "discover"],
        "natural": len(response.split()) > 5 and not response.startswith("I'm here to")
    }
    
    scores = {}
    for indicator, keywords in quality_indicators.items():
        if indicator == "natural":
            scores[indicator] = keywords
        else:
            score = sum(1 for keyword in keywords if keyword.lower() in response.lower())
            scores[indicator] = score > 0
    
    print(f"   Quality Analysis:")
    print(f"   - Empathy: {'✅' if scores['empathy'] else '❌'}")
    print(f"   - Curiosity: {'✅' if scores['curiosity'] else '❌'}")
    print(f"   - Engagement: {'✅' if scores['engagement'] else '❌'}")
    print(f"   - Reflection: {'✅' if scores['reflection'] else '❌'}")
    print(f"   - Natural: {'✅' if scores['natural'] else '❌'}")

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY not set - will test fallback responses")
    else:
        print("✅ OPENAI_API_KEY found - testing full OpenAI integration")
    
    try:
        test_conversation_quality()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"❌ Test failed with error: {e}") 