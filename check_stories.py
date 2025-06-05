#!/usr/bin/env python3

import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
if not firebase_admin._apps:
    if os.path.exists('service-account-key.json'):
        cred = credentials.Certificate('service-account-key.json')
        firebase_admin.initialize_app(cred)
    else:
        # Use local emulator or default credentials
        firebase_admin.initialize_app()

try:
    db = firestore.client()
    
    # Get all stories
    stories_ref = db.collection('stories')
    stories = list(stories_ref.stream())
    
    print(f"📊 Total stories in database: {len(stories)}")
    print("=" * 50)
    
    if stories:
        for i, story in enumerate(stories, 1):
            data = story.to_dict()
            print(f"{i}. Story ID: {story.id}")
            print(f"   Title: {data.get('title', 'No title')}")
            print(f"   Author: {data.get('author_name', 'Unknown')}")
            print(f"   User ID: {data.get('user_id', 'Unknown')}")
            print(f"   Public: {data.get('is_public', False)}")
            print(f"   Created: {data.get('timestamp', data.get('created_at', 'Unknown'))}")
            print(f"   Summary: {data.get('summary', 'No summary')[:100]}...")
            print()
    else:
        print("No stories found in database!")
        
except Exception as e:
    print(f"Error accessing database: {e}") 