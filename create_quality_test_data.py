#!/usr/bin/env python3
"""
Create high-quality test data for Smart Story Engine testing
"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

# High-quality test conversations with real names
test_conversations = [
    {
        "user_name": "Sarah Chen",
        "user_id": "sarah_chen_001",
        "conversations": [
            # Story-worthy conversation - should generate story
            {
                "messages": [
                    {"role": "user", "content": "I need to tell someone about what happened last week with my grandmother."},
                    {"role": "assistant", "content": "I'm here to listen. What happened with your grandmother?"},
                    {"role": "user", "content": "She's 89 and has been living alone since grandpa passed. Last Tuesday, I went to visit her and found her sitting in the dark, just staring at old photo albums. When I asked if she was okay, she started crying and told me she felt like she was disappearing - that no one remembered the stories behind the photos anymore. It broke my heart."},
                    {"role": "assistant", "content": "That sounds like such a profound and emotional moment. How did you respond to her?"},
                    {"role": "user", "content": "I sat with her for hours, going through every single photo. She told me stories I'd never heard - about her childhood during the war, how she met grandpa at a dance, the struggles of raising five kids on a farm. By the end, she was laughing and her eyes were bright again. I realized that day that our elders aren't just people who need care - they're living libraries of wisdom and experience. I promised to visit every week to record her stories."}
                ]
            },
            # Simple conversation - should NOT generate story
            {
                "messages": [
                    {"role": "user", "content": "How are you doing today?"},
                    {"role": "assistant", "content": "I'm doing well, thank you for asking! How are you feeling today?"},
                    {"role": "user", "content": "Pretty good, just wondering what the weather will be like this weekend."},
                    {"role": "assistant", "content": "I hope you have nice weather for your weekend plans! What are you hoping to do?"}
                ]
            }
        ]
    },
    {
        "user_name": "Marcus Rodriguez",
        "user_id": "marcus_rodriguez_001", 
        "conversations": [
            # Story-worthy conversation - career breakthrough
            {
                "messages": [
                    {"role": "user", "content": "I've been thinking about this moment that changed everything for me professionally."},
                    {"role": "assistant", "content": "That sounds significant. What moment was that?"},
                    {"role": "user", "content": "Three years ago, I was working as a junior developer at a startup. We had this massive client presentation, and our lead developer got food poisoning the night before. I was terrified, but I had to step up and present our entire platform architecture to the CEO of a Fortune 500 company."},
                    {"role": "assistant", "content": "That must have been incredibly nerve-wracking. How did it go?"},
                    {"role": "user", "content": "I was shaking so badly I could barely hold my laptop. But something clicked when I started talking about the code I'd written. I realized I actually understood our system better than I thought. The CEO asked tough technical questions, and I answered every single one. Not only did we get the contract, but he offered me a job on the spot. That moment taught me that imposter syndrome was holding me back more than any lack of skill. Sometimes you have to be thrown into the deep end to realize you can swim."}
                ]
            }
        ]
    },
    {
        "user_name": "Emma Thompson",
        "user_id": "emma_thompson_001",
        "conversations": [
            # Moderate potential - should guide to story
            {
                "messages": [
                    {"role": "user", "content": "I've been reflecting on my relationship with my sister lately."},
                    {"role": "assistant", "content": "What's been on your mind about your relationship with her?"},
                    {"role": "user", "content": "We used to be so close as kids, but we grew apart in our twenties. Different life choices, different values. But recently we've been talking more."},
                    {"role": "assistant", "content": "It sounds like there might be a meaningful story there. What brought you two back together recently?"}
                ]
            }
        ]
    },
    {
        "user_name": "David Kim",
        "user_id": "david_kim_001",
        "conversations": [
            # Deep personal story - should definitely generate story
            {
                "messages": [
                    {"role": "user", "content": "I want to share something I've never told anyone before."},
                    {"role": "assistant", "content": "I'm honored that you feel comfortable sharing with me. What's on your heart?"},
                    {"role": "user", "content": "When I was 16, my dad lost his job and we almost lost our house. I watched him, this man who had always been my hero, break down crying at the kitchen table. I felt so helpless and angry at the world. That night, I made a decision that would shape my entire life."},
                    {"role": "assistant", "content": "That sounds like such a pivotal moment. What decision did you make?"},
                    {"role": "user", "content": "I decided I would never let my family struggle like that again. I started working part-time jobs, saved every penny, and threw myself into my studies. I became obsessed with financial security. It drove me to succeed, but it also made me afraid to take risks or enjoy life. It took me years to realize that while that moment gave me drive, it also gave me anxiety that I carried into every relationship and career decision. Learning to balance security with living fully has been my life's work."}
                ]
            }
        ]
    },
    {
        "user_name": "Zoe Williams",
        "user_id": "zoe_williams_001",
        "conversations": [
            # Advice-seeking conversation - should continue conversation
            {
                "messages": [
                    {"role": "user", "content": "I'm struggling with a decision about my career and could use some perspective."},
                    {"role": "assistant", "content": "I'd be happy to help you think through it. What's the decision you're facing?"},
                    {"role": "user", "content": "I have a job offer that pays 40% more, but it would mean moving across the country and leaving my support network. What do you think I should consider?"},
                    {"role": "assistant", "content": "That's a significant decision with many factors to weigh. What aspects of this choice feel most important to you right now?"}
                ]
            }
        ]
    }
]

def create_user(user_id, user_name):
    """Create a user in the system and return the actual user ID"""
    print(f"Creating user: {user_name} ({user_id})")
    
    payload = {
        'email': f"{user_id}@test.com",
        'password': 'testpassword123',
        'name': user_name,
        'user_id': user_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", 
                               json=payload, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code in [200, 201]:
            result = response.json()
            actual_user_id = result.get('user_id')
            print(f"✅ User {user_name} created successfully with ID: {actual_user_id}")
            return actual_user_id
        elif response.status_code == 409:
            # User already exists, try to login to get their ID
            print(f"⚠️  User {user_name} already exists, logging in...")
            login_payload = {
                'email': f"{user_id}@test.com"
            }
            
            login_response = requests.post(f"{BASE_URL}/api/auth/login", 
                                         json=login_payload, 
                                         headers={'Content-Type': 'application/json'})
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                actual_user_id = login_result.get('user_id')
                print(f"✅ User {user_name} logged in successfully with ID: {actual_user_id}")
                return actual_user_id
            else:
                print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
                return None
        else:
            print(f"⚠️  User creation response: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception creating user: {e}")
        return None

def send_conversation(actual_user_id, user_name, messages):
    """Send a conversation to the chat API"""
    if not actual_user_id:
        print(f"❌ Skipping conversation for {user_name} - no valid user ID")
        return
        
    print(f"\n--- Testing conversation for {user_name} (ID: {actual_user_id}) ---")
    
    conversation_history = []
    
    for i, message in enumerate(messages):
        print(f"Message {i+1}: {message['content'][:50]}...")
        
        # Add message to conversation history
        conversation_history.append(message)
        
        if message['role'] == 'user':
            # Send user message to API
            payload = {
                'message': message['content'],
                'user_id': actual_user_id,
                'conversation_history': conversation_history
            }
            
            try:
                response = requests.post(f"{BASE_URL}/api/chat/message", 
                                       json=payload, 
                                       headers={'Content-Type': 'application/json'})
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Response: {result.get('message', '')[:50]}...")
                    
                    # Check if story was created
                    if result.get('story_created'):
                        print(f"🎉 STORY CREATED: {result.get('story_title', 'Untitled')}")
                        print(f"   Story ID: {result.get('story_id')}")
                    else:
                        print(f"💬 Continuing conversation (Score: {result.get('story_readiness_score', 'N/A')})")
                    
                    # Add assistant response to conversation history
                    conversation_history.append({
                        'role': 'assistant',
                        'content': result.get('message', '')
                    })
                    
                elif response.status_code == 201:
                    result = response.json()
                    print(f"✅ Story created: {result.get('message', '')[:50]}...")
                    
                    # Check if story was created
                    if result.get('story_created'):
                        print(f"🎉 STORY CREATED: {result.get('story_title', 'Untitled')}")
                        print(f"   Story ID: {result.get('story_id')}")
                    
                    # Add assistant response to conversation history
                    conversation_history.append({
                        'role': 'assistant',
                        'content': result.get('message', '')
                    })
                    
                else:
                    print(f"❌ Error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"❌ Exception: {e}")
        
        # Small delay between messages
        time.sleep(0.5)
    
    print(f"--- Completed conversation for {user_name} ---\n")

def main():
    print("🚀 Creating high-quality test data for Smart Story Engine...")
    print("=" * 60)
    
    # First, create all users and store their actual IDs
    print("\n👥 Creating test users...")
    user_id_mapping = {}
    
    for user_data in test_conversations:
        user_name = user_data['user_name']
        user_id = user_data['user_id']
        actual_user_id = create_user(user_id, user_name)
        user_id_mapping[user_id] = actual_user_id
        time.sleep(0.5)  # Small delay between user creations
    
    print("\n" + "=" * 60)
    print("📝 Starting conversations...")
    
    # Then, process conversations using actual user IDs
    for user_data in test_conversations:
        user_name = user_data['user_name']
        user_id = user_data['user_id']
        actual_user_id = user_id_mapping.get(user_id)
        
        print(f"\n👤 Processing conversations for {user_name}")
        
        for i, conversation in enumerate(user_data['conversations']):
            print(f"\n  📝 Conversation {i+1}")
            send_conversation(actual_user_id, user_name, conversation['messages'])
            
            # Pause between conversations
            time.sleep(1)
    
    print("\n" + "=" * 60)
    print("✅ Test data creation complete!")
    print("\nYou can now:")
    print("1. Check the stories at: http://localhost:8080/app")
    print("2. Test more conversations at: http://localhost:8080/chat")
    print("3. Generate story formats from the created stories")

if __name__ == "__main__":
    main() 