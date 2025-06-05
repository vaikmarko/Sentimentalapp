#!/usr/bin/env python3
"""Debug script to check database contents and identify story visibility issues"""

import os
import sys
import logging
import firebase_admin
from firebase_admin import credentials, firestore

# Add the current directory to Python path
sys.path.append('.')

try:
    # Initialize Firebase (same as in app.py)
    if not firebase_admin._apps:
        # Try service account first
        if os.path.exists('service-account-key.json'):
            cred = credentials.Certificate('service-account-key.json')
            firebase_admin.initialize_app(cred)
            print("✅ Firebase initialized with service account")
        else:
            # Fallback to default credentials
            firebase_admin.initialize_app()
            print("✅ Firebase initialized with default credentials")
    
    db = firestore.client()
    
    print("\n🔍 DEBUGGING DATABASE CONTENTS")
    print("=" * 60)
    
    # Get all stories from stories collection
    print("\n1. Querying 'stories' collection...")
    stories_collection = db.collection('stories')
    stories = list(stories_collection.stream())
    
    print(f"📊 Total documents in 'stories' collection: {len(stories)}")
    
    if stories:
        print("\n📋 Story details:")
        for i, story in enumerate(stories, 1):
            data = story.to_dict()
            print(f"\n{i}. Document ID: {story.id}")
            print(f"   Title: {data.get('title', 'No title')}")
            print(f"   Author: {data.get('author', 'No author')}")
            print(f"   User ID: {data.get('user_id', 'No user_id')}")
            print(f"   Public: {data.get('public', 'Not set')}")
            print(f"   Is Public: {data.get('is_public', 'Not set')}")
            print(f"   Timestamp: {data.get('timestamp', 'No timestamp')}")
            print(f"   Content length: {len(data.get('content', ''))}")
            
            # Check if this is a conversation-generated story
            if 'conversation' in data:
                print(f"   Has conversation: {len(data['conversation'])} messages")
            if 'analysis' in data:
                print(f"   Has analysis: {bool(data['analysis'])}")
    
    # Check other collections that might contain stories
    print(f"\n2. Checking other potential collections...")
    
    # Check for test collections
    collections = ['test_stories', 'user_stories', 'generated_stories']
    for collection_name in collections:
        try:
            coll = db.collection(collection_name)
            docs = list(coll.stream())
            if docs:
                print(f"   📁 {collection_name}: {len(docs)} documents")
        except Exception as e:
            print(f"   ❌ {collection_name}: Not accessible ({e})")
    
    # Check test_users to see recent activity
    print(f"\n3. Checking test_users for recent story creation...")
    try:
        users_collection = db.collection('test_users')
        users = list(users_collection.stream())
        print(f"📊 Total test users: {len(users)}")
        
        if users:
            for user in users[-3:]:  # Last 3 users
                data = user.to_dict()
                print(f"   User: {data.get('email', data.get('username', 'Unknown'))}")
                print(f"   Stories created: {data.get('stories_created', 0)}")
                print(f"   Last activity: {data.get('last_activity', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ test_users: {e}")
    
    # Test the same query that the API uses
    print(f"\n4. Testing API query simulation...")
    try:
        api_stories = []
        for story in db.collection('stories').stream():
            story_data = story.to_dict()
            # Add the Firestore document ID as the story ID
            story_data['id'] = story.id
            # Ensure compatibility with React component
            story_data['author'] = story_data.get('author', 'Anonymous')
            story_data['content'] = story_data.get('content', story_data.get('text', ''))
            story_data['timestamp'] = story_data.get('timestamp', '1h ago')
            story_data['format'] = story_data.get('format', 'text')
            story_data['public'] = story_data.get('public', True)
            story_data['reactions'] = story_data.get('reactions', 0)
            story_data['inCosmos'] = story_data.get('inCosmos', False)
            story_data['createdFormats'] = story_data.get('createdFormats', {})
            story_data['cosmic_insights'] = story_data.get('analysis', {}).get('themes', [])
            api_stories.append(story_data)
        
        print(f"📊 API simulation would return: {len(api_stories)} stories")
        
        # Check if there are any differences
        if len(api_stories) != len(stories):
            print("❌ Mismatch between raw query and API simulation!")
        else:
            print("✅ API simulation matches raw query")
            
    except Exception as e:
        print(f"❌ API simulation failed: {e}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 