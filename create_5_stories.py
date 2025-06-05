#!/usr/bin/env python3
"""Create 5 test stories for discover functionality testing"""

import requests
import time
import json

BASE_URL = "http://localhost:8080"

# 5 focused test conversations that will definitely trigger story creation
test_conversations = [
    {
        "name": "Sarah Chen",
        "email": "sarah.chen.test@example.com",
        "messages": [
            "I just got promoted to VP at my company!",
            "I've been working towards this for 3 years and honestly didn't think it would happen",
            "My immigrant parents sacrificed everything for my education and I finally made it",
            "I'm the youngest VP in company history",
            "I literally cried in the CEO's office when she told me"
        ]
    },
    {
        "name": "Marcus Thompson", 
        "email": "marcus.t.test@example.com",
        "messages": [
            "My 8-year-old daughter asked me to put my phone down during dinner",
            "She said 'Daddy, you always look at your phone instead of talking to us'",
            "It hit me like a brick wall - she's absolutely right",
            "I realized I've been missing so many precious moments with my kids",
            "I put the phone in another room and we had the best conversation"
        ]
    },
    {
        "name": "Elena Rodriguez",
        "email": "elena.r.test@example.com", 
        "messages": [
            "I discovered something amazing about myself as an artist today",
            "I've been painting for years but always felt like I was copying others",
            "Today I mixed colors in a way I'd never tried before",
            "The painting that emerged was completely my own voice",
            "For the first time I felt like a real artist, not just someone who paints"
        ]
    },
    {
        "name": "David Kim",
        "email": "david.k.test@example.com",
        "messages": [
            "I quit my law job today to work in environmental conservation",
            "Everyone thinks I'm crazy - lawyers make good money",
            "But I couldn't sleep at night knowing I wasn't making a difference",
            "The moment I handed in my resignation I felt this incredible freedom",
            "I'm scared about the future but finally feel aligned with my values"
        ]
    },
    {
        "name": "Amara Johnson",
        "email": "amara.j.test@example.com",
        "messages": [
            "My best friend and I had a huge fight last month and weren't speaking",
            "Today she showed up at my door with flowers and an apology",
            "We talked for hours about what went wrong in our friendship",
            "I realized how much I missed having her in my life",
            "Our friendship feels stronger now than it ever has before"
        ]
    }
]

def register_and_login_user(name, email):
    """Register and login a test user"""
    # Try registration first
    register_data = {
        "username": name,
        "email": email,
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
    if response.status_code not in [200, 201]:
        print(f"   ℹ️  Registration failed for {name} (user may exist), trying login...")
    else:
        print(f"   ✅ Registered {name}")
    
    # Try login (works for both new and existing users)
    login_data = {
        "email": email,
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data.get('user_id')
        print(f"   ✅ {name} logged in successfully (ID: {user_id})")
        return user_id
    else:
        print(f"   ❌ Login failed for {name}: {response.text}")
        # If login fails, try with a new unique email
        new_email = f"{name.lower().replace(' ', '.')}.{int(time.time())}@test.com"
        print(f"   🔄 Trying with new email: {new_email}")
        
        # Register with new email
        register_data['email'] = new_email
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        if response.status_code in [200, 201]:
            # Login with new email
            login_data['email'] = new_email
            response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
            if response.status_code == 200:
                user_data = response.json()
                user_id = user_data.get('user_id')
                print(f"   ✅ {name} logged in with new email (ID: {user_id})")
                return user_id
        
        print(f"   ❌ Failed to create/login user {name}")
        return None

def send_messages_and_create_story(user_id, name, messages):
    """Send messages to create a story"""
    print(f"\n💬 Starting conversation for {name}...")
    
    for i, message in enumerate(messages, 1):
        print(f"   📝 Message {i}/{len(messages)}: {message[:50]}...")
        
        response = requests.post(f"{BASE_URL}/api/chat/message", 
            json={"message": message},
            headers={"X-User-ID": user_id}
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get('message', '')
            
            if data.get('story_created'):
                story_id = data.get('story_id')
                print(f"   🎉 Story created! ID: {story_id}")
                return story_id
            
            # Wait between messages
            time.sleep(2)
        else:
            print(f"   ❌ Message failed: {response.status_code}")
    
    print(f"   ⚠️  No story created for {name}")
    return None

def main():
    print("🚀 Creating 5 test stories for discover functionality")
    print("=" * 60)
    
    created_stories = []
    
    for conv in test_conversations:
        print(f"\n👤 Processing {conv['name']}...")
        
        # Register and login user
        user_id = register_and_login_user(conv['name'], conv['email'])
        if not user_id:
            continue
        
        # Create story through conversation
        story_id = send_messages_and_create_story(user_id, conv['name'], conv['messages'])
        if story_id:
            created_stories.append({
                'name': conv['name'],
                'story_id': story_id
            })
        
        print(f"   ⏳ Waiting before next user...")
        time.sleep(3)
    
    print(f"\n🎯 SUMMARY")
    print("=" * 60)
    print(f"✅ Created {len(created_stories)} stories:")
    for story in created_stories:
        print(f"   • {story['name']}: {story['story_id']}")
    
    # Verify with API
    print(f"\n🔍 Verifying with stories API...")
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        stories = response.json()
        print(f"📊 API now returns {len(stories)} stories")
        
        if len(stories) >= 5:
            print("🎉 SUCCESS! Discover page should now show 5+ stories")
        else:
            print(f"⚠️  Only {len(stories)} stories visible in API")
    else:
        print(f"❌ API check failed: {response.status_code}")

if __name__ == "__main__":
    main() 