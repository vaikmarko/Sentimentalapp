#!/usr/bin/env python3
"""Comprehensive database check to find all users, conversations, and chat data"""

import requests
import json

BASE_URL = "http://localhost:8080"

def check_database():
    print("🔍 COMPREHENSIVE DATABASE CHECK")
    print("=" * 60)
    
    # Check debug stories endpoint
    print("\n1. Stories in database:")
    response = requests.get(f"{BASE_URL}/api/debug/stories")
    if response.status_code == 200:
        data = response.json()
        print(f"   📊 Total stories: {data.get('total_stories', 0)}")
        print(f"   👥 Test users: {data.get('test_users_count', 0)}")
        
        for story in data.get('stories_list', []):
            print(f"\n   📖 Story: {story.get('title', 'No title')}")
            print(f"      ID: {story.get('document_id', 'No ID')}")
            print(f"      Author: {story.get('author', 'No author')}")
            print(f"      User ID: {story.get('user_id', 'No user_id')}")
            print(f"      Conversation: {story.get('has_conversation', False)}")
            print(f"      Content length: {story.get('content_length', 0)}")
    
    # Check users endpoint if it exists
    print(f"\n2. Checking for user data...")
    try:
        response = requests.get(f"{BASE_URL}/api/users")
        if response.status_code == 200:
            users = response.json()
            print(f"   👥 Users found: {len(users)}")
            for user in users[:5]:  # Show first 5
                print(f"      - {user.get('email', user.get('username', 'Unknown'))}")
    except:
        print("   ❌ No users endpoint or error accessing users")
    
    # Check conversations endpoint if it exists
    print(f"\n3. Checking for conversation data...")
    try:
        response = requests.get(f"{BASE_URL}/api/conversations")
        if response.status_code == 200:
            conversations = response.json()
            print(f"   💬 Conversations found: {len(conversations)}")
    except:
        print("   ❌ No conversations endpoint")
    
    # Check chat messages endpoint if it exists
    print(f"\n4. Checking for chat messages...")
    try:
        response = requests.get(f"{BASE_URL}/api/chat/messages")
        if response.status_code == 200:
            messages = response.json()
            print(f"   📝 Chat messages found: {len(messages)}")
    except:
        print("   ❌ No chat messages endpoint")
    
    # Look for our specific test users
    print(f"\n5. Looking for our test users...")
    test_emails = [
        "sarah.chen.test@example.com",
        "marcus.thompson.test@example.com", 
        "elena.rodriguez.test@example.com",
        "david.kim.test@example.com",
        "amara.johnson.test@example.com"
    ]
    
    for email in test_emails:
        try:
            # Try to login with test credentials
            login_data = {"email": email, "password": "testpass123"}
            response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
            if response.status_code == 200:
                user_data = response.json()
                print(f"   ✅ Found user: {email}")
                print(f"      User ID: {user_data.get('user_id', 'No ID')}")
                
                # Check if they have conversations
                user_id = user_data.get('user_id')
                if user_id:
                    # Try to get their chat history (if endpoint exists)
                    try:
                        chat_response = requests.get(f"{BASE_URL}/api/chat/history", 
                            headers={"X-User-ID": user_id})
                        if chat_response.status_code == 200:
                            chat_data = chat_response.json()
                            print(f"      Chat messages: {len(chat_data.get('messages', []))}")
                    except:
                        pass
            else:
                print(f"   ❌ User not found: {email}")
        except Exception as e:
            print(f"   ❌ Error checking {email}: {e}")

if __name__ == "__main__":
    check_database() 