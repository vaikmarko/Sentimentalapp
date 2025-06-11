#!/usr/bin/env python3
"""
Firebase Data Audit Script for Sentimental App
Analyzes data quality and helps create cleanup strategy
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import json

# Initialize Firebase
try:
    if os.path.exists('firebase-credentials.json'):
        cred = credentials.Certificate('firebase-credentials.json')
        firebase_admin.initialize_app(cred)
    else:
        firebase_admin.initialize_app()
    
    db = firestore.client()
    print("✅ Firebase connected successfully")
except Exception as e:
    print(f"❌ Firebase connection failed: {e}")
    exit(1)

def analyze_collection(collection_name):
    """Analyze a specific collection"""
    print(f"\n📊 Analyzing {collection_name} collection...")
    
    try:
        docs = list(db.collection(collection_name).stream())
        if not docs:
            print(f"   Empty collection")
            return {}
        
        doc_count = len(docs)
        print(f"   Total documents: {doc_count}")
        
        # Sample analysis
        sample_doc = docs[0].to_dict()
        print(f"   Sample fields: {list(sample_doc.keys())}")
        
        # Return summary
        return {
            'count': doc_count,
            'sample_fields': list(sample_doc.keys()),
            'sample_data': sample_doc
        }
        
    except Exception as e:
        print(f"   ❌ Error analyzing {collection_name}: {e}")
        return {}

def analyze_users():
    """Detailed user analysis"""
    print(f"\n👥 USER ANALYSIS")
    print("=" * 50)
    
    # Check both collections
    collections_to_check = ['test_users', 'users']
    all_users = []
    
    for collection_name in collections_to_check:
        try:
            users = list(db.collection(collection_name).stream())
            for user_doc in users:
                user_data = user_doc.to_dict()
                user_data['doc_id'] = user_doc.id
                user_data['collection'] = collection_name
                all_users.append(user_data)
            print(f"   {collection_name}: {len(users)} users")
        except Exception as e:
            print(f"   ❌ Error with {collection_name}: {e}")
    
    print(f"\n   📈 TOTAL USERS: {len(all_users)}")
    
    # Find quality users
    quality_users = []
    marcus_users = []
    
    for user in all_users:
        email = user.get('email', '')
        name = user.get('name', '')
        
        # Look for Marcus Rodriguez
        if 'marcus' in name.lower() or 'rodriguez' in name.lower():
            marcus_users.append(user)
            print(f"   🎯 MARCUS FOUND: {name} ({email}) - ID: {user['doc_id']}")
        
        # Quality indicators
        if (user.get('stories_created', 0) > 0 or 
            len(user.get('email', '')) > 5 and '@' in user.get('email', '')):
            quality_users.append(user)
    
    print(f"\n   📊 Users with activity: {len(quality_users)}")
    print(f"   🔍 Marcus accounts found: {len(marcus_users)}")
    
    # Show top users by activity
    active_users = sorted(all_users, 
                         key=lambda x: x.get('stories_created', 0), 
                         reverse=True)[:10]
    
    print(f"\n   🏆 TOP 10 MOST ACTIVE USERS:")
    for i, user in enumerate(active_users, 1):
        stories = user.get('stories_created', 0)
        name = user.get('name', 'Unknown')[:20]
        email = user.get('email', 'No email')[:30]
        print(f"      {i:2d}. {name:20} | {email:30} | {stories:3d} stories | {user['doc_id']}")
    
    return {
        'total_users': len(all_users),
        'quality_users': quality_users,
        'marcus_users': marcus_users,
        'active_users': active_users[:10]
    }

def analyze_stories():
    """Detailed story analysis"""
    print(f"\n📚 STORY ANALYSIS")
    print("=" * 50)
    
    try:
        stories = list(db.collection('stories').stream())
        print(f"   Total stories: {len(stories)}")
        
        if not stories:
            return {}
        
        # Analyze story quality
        quality_stories = []
        public_stories = []
        stories_with_formats = []
        marcus_stories = []
        
        for story_doc in stories:
            story = story_doc.to_dict()
            story['doc_id'] = story_doc.id
            
            content_length = len(story.get('content', ''))
            
            # Quality indicators
            if content_length > 200:  # Substantial content
                quality_stories.append(story)
            
            if story.get('public', False):
                public_stories.append(story)
            
            if story.get('createdFormats') or story.get('formats'):
                stories_with_formats.append(story)
            
            # Check for Marcus stories
            author = story.get('author', '').lower()
            if 'marcus' in author or 'rodriguez' in author:
                marcus_stories.append(story)
                print(f"   🎯 MARCUS STORY: '{story.get('title', 'No title')[:50]}...' - ID: {story['doc_id']}")
        
        print(f"   📊 Quality stories (>200 chars): {len(quality_stories)}")
        print(f"   🌍 Public stories: {len(public_stories)}")
        print(f"   ✨ Stories with formats: {len(stories_with_formats)}")
        print(f"   🔍 Marcus stories: {len(marcus_stories)}")
        
        # Show some quality stories
        print(f"\n   📖 SAMPLE QUALITY STORIES:")
        for i, story in enumerate(quality_stories[:5], 1):
            title = story.get('title', 'No title')[:40]
            author = story.get('author', 'Unknown')[:15]
            length = len(story.get('content', ''))
            formats = len(story.get('createdFormats', []))
            print(f"      {i}. '{title}...' by {author} | {length:4d} chars | {formats} formats | {story['doc_id']}")
        
        return {
            'total_stories': len(stories),
            'quality_stories': quality_stories,
            'public_stories': public_stories,
            'stories_with_formats': stories_with_formats,
            'marcus_stories': marcus_stories
        }
        
    except Exception as e:
        print(f"   ❌ Error analyzing stories: {e}")
        return {}

def create_cleanup_plan(user_analysis, story_analysis):
    """Create a smart cleanup plan"""
    print(f"\n🧹 CLEANUP PLAN")
    print("=" * 50)
    
    # Identify users to keep
    users_to_keep = set()
    
    # Always keep Marcus
    for marcus_user in user_analysis.get('marcus_users', []):
        users_to_keep.add(marcus_user['doc_id'])
        print(f"   ✅ KEEP Marcus: {marcus_user.get('name')} ({marcus_user['doc_id']})")
    
    # Keep users with quality stories
    quality_threshold = 1  # Users with at least 1 story
    for user in user_analysis.get('quality_users', []):
        if user.get('stories_created', 0) >= quality_threshold:
            users_to_keep.add(user['doc_id'])
    
    # Keep users who authored quality stories
    for story in story_analysis.get('quality_stories', []):
        user_id = story.get('user_id')
        if user_id:
            users_to_keep.add(user_id)
    
    print(f"   📊 Users to keep: {len(users_to_keep)}")
    print(f"   🗑️  Users to remove: {user_analysis.get('total_users', 0) - len(users_to_keep)}")
    
    # Stories to keep
    stories_to_keep = []
    for story in story_analysis.get('quality_stories', []):
        # Keep if it's quality content or from a user we're keeping
        if (len(story.get('content', '')) > 200 or 
            story.get('user_id') in users_to_keep or
            story.get('public', False) or
            story.get('createdFormats')):
            stories_to_keep.append(story['doc_id'])
    
    print(f"   📚 Stories to keep: {len(stories_to_keep)}")
    print(f"   🗑️  Stories to remove: {story_analysis.get('total_stories', 0) - len(stories_to_keep)}")
    
    return {
        'users_to_keep': list(users_to_keep),
        'stories_to_keep': stories_to_keep
    }

def main():
    """Main audit function"""
    print("🔍 SENTIMENTAL APP FIREBASE DATA AUDIT")
    print("=" * 60)
    
    # Quick overview of all collections
    collections = ['test_users', 'users', 'stories', 'conversations', 
                  'chat_messages', 'story_formats', 'connections']
    
    print("\n📋 COLLECTION OVERVIEW:")
    for collection in collections:
        analyze_collection(collection)
    
    # Detailed analysis
    user_analysis = analyze_users()
    story_analysis = analyze_stories()
    
    # Create cleanup plan
    cleanup_plan = create_cleanup_plan(user_analysis, story_analysis)
    
    # Save results to JSON
    audit_results = {
        'timestamp': datetime.now().isoformat(),
        'user_analysis': user_analysis,
        'story_analysis': story_analysis,
        'cleanup_plan': cleanup_plan
    }
    
    with open('firebase_audit_results.json', 'w') as f:
        json.dump(audit_results, f, indent=2, default=str)
    
    print(f"\n💾 Audit results saved to firebase_audit_results.json")
    print(f"\n🎯 SUMMARY:")
    print(f"   👥 Total users: {user_analysis.get('total_users', 0)}")
    print(f"   📚 Total stories: {story_analysis.get('total_stories', 0)}")
    print(f"   ✅ Users to keep: {len(cleanup_plan.get('users_to_keep', []))}")
    print(f"   ✅ Stories to keep: {len(cleanup_plan.get('stories_to_keep', []))}")
    print(f"   🔍 Marcus accounts: {len(user_analysis.get('marcus_users', []))}")

if __name__ == "__main__":
    main() 