#!/usr/bin/env python3
"""
Firebase Selective Cleanup Script
Keeps quality accounts and stories, removes test data
"""

import os
import sys
import json
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        if not firebase_admin._apps:
            # Use service account for admin operations
            cred = credentials.Certificate('firebase-credentials.json')
            firebase_admin.initialize_app(cred)
        
        return firestore.client()
    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}")
        return None

def analyze_user_quality(user_doc, stories_by_user):
    """Analyze if a user should be kept based on quality metrics"""
    user_data = user_doc.to_dict()
    user_id = user_doc.id
    
    # Always keep Marcus Rodriguez accounts
    email = user_data.get('email', '')
    if 'marcus' in email.lower() and ('rodriguez' in email.lower() or 'rod' in email.lower()):
        return True, "Marcus Rodriguez account"
    
    # Always keep core testing accounts (including any potential Gmail accounts for Merike/Lars)
    if email in ['lars@sentimental.app', 'merike@sentimental.app', 'marko@sentimental.app']:
        return True, "Core testing account"
    
    # Protect any real Gmail accounts that might be Merike/Lars using Google auth
    name = user_data.get('name', '').lower()
    if (email.endswith('@gmail.com') and 
        any(keyword in name for keyword in ['merike', 'lars', 'sisask', 'hion']) and
        not any(test_word in name for test_word in ['test', 'demo', 'fake'])):
        return True, "Potential core team Gmail account"
    
    # Check if user has quality stories
    user_stories = stories_by_user.get(user_id, [])
    if user_stories:
        # Check for substantial content
        for story in user_stories:
            story_data = story.to_dict()
            content = story_data.get('content', '')
            
            # Quality indicators
            if (len(content) > 200 and  # Substantial content
                not content.startswith('Test') and  # Not test content
                'test' not in content.lower()[:50] and  # No test in beginning
                any(word in content.lower() for word in ['life', 'work', 'relationship', 'dream', 'journey', 'experience', 'feeling', 'moment', 'realized', 'learned'])):  # Real content keywords
                return True, f"Quality story: {story_data.get('title', 'Untitled')[:50]}..."
    
    # Check for non-test email patterns
    if (email and 
        not email.endswith('@test.com') and 
        not email.endswith('@example.com') and
        'test' not in email.lower() and
        not email.startswith('test_')):
        return True, "Real email address"
    
    # Check for real names (not test patterns)
    name = user_data.get('name', '')
    if (name and 
        len(name) > 5 and
        not name.lower().startswith('test') and
        not name.lower().startswith('user') and
        ' ' in name and  # Has first and last name
        not any(test_word in name.lower() for test_word in ['test', 'demo', 'sample', 'fake'])):
        return True, "Real name pattern"
    
    return False, "Test/low-quality account"

def get_all_data(db):
    """Get all users and stories for analysis"""
    print("📊 Analyzing all data...")
    
    # Get all users from both collections
    users_data = {}
    test_users_data = {}
    
    try:
        # Get users collection
        users_ref = db.collection('users')
        for doc in users_ref.stream():
            users_data[doc.id] = doc
        print(f"   Found {len(users_data)} users in 'users' collection")
        
        # Get test_users collection
        test_users_ref = db.collection('test_users')
        for doc in test_users_ref.stream():
            test_users_data[doc.id] = doc
        print(f"   Found {len(test_users_data)} users in 'test_users' collection")
        
    except Exception as e:
        print(f"❌ Error getting users: {e}")
        return None, None, None
    
    # Get all stories grouped by user
    stories_by_user = {}
    try:
        stories_ref = db.collection('stories')
        for doc in stories_ref.stream():
            story_data = doc.to_dict()
            user_id = story_data.get('user_id')
            if user_id:
                if user_id not in stories_by_user:
                    stories_by_user[user_id] = []
                stories_by_user[user_id].append(doc)
        
        total_stories = sum(len(stories) for stories in stories_by_user.values())
        print(f"   Found {total_stories} stories across {len(stories_by_user)} users")
        
    except Exception as e:
        print(f"❌ Error getting stories: {e}")
        return None, None, None
    
    return users_data, test_users_data, stories_by_user

def selective_cleanup(db, dry_run=True):
    """Perform selective cleanup keeping quality accounts"""
    print(f"\n🧹 Starting {'DRY RUN' if dry_run else 'ACTUAL'} selective cleanup...")
    
    users_data, test_users_data, stories_by_user = get_all_data(db)
    if not users_data and not test_users_data:
        return
    
    # Analyze all users for quality
    keep_users = []
    remove_users = []
    
    print("\n📋 Analyzing user quality...")
    
    # Analyze users collection
    for user_id, user_doc in users_data.items():
        should_keep, reason = analyze_user_quality(user_doc, stories_by_user)
        user_data = user_doc.to_dict()
        
        if should_keep:
            keep_users.append({
                'id': user_id,
                'collection': 'users',
                'email': user_data.get('email', ''),
                'name': user_data.get('name', ''),
                'reason': reason,
                'stories_count': len(stories_by_user.get(user_id, []))
            })
        else:
            remove_users.append({
                'id': user_id,
                'collection': 'users',
                'email': user_data.get('email', ''),
                'name': user_data.get('name', ''),
                'reason': reason,
                'stories_count': len(stories_by_user.get(user_id, []))
            })
    
    # Analyze test_users collection
    for user_id, user_doc in test_users_data.items():
        should_keep, reason = analyze_user_quality(user_doc, stories_by_user)
        user_data = user_doc.to_dict()
        
        if should_keep:
            keep_users.append({
                'id': user_id,
                'collection': 'test_users',
                'email': user_data.get('email', ''),
                'name': user_data.get('name', ''),
                'reason': reason,
                'stories_count': len(stories_by_user.get(user_id, []))
            })
        else:
            remove_users.append({
                'id': user_id,
                'collection': 'test_users',
                'email': user_data.get('email', ''),
                'name': user_data.get('name', ''),
                'reason': reason,
                'stories_count': len(stories_by_user.get(user_id, []))
            })
    
    # Display analysis results
    print(f"\n✅ USERS TO KEEP ({len(keep_users)}):")
    for user in keep_users:
        print(f"   👤 {user['name']} ({user['email']}) - {user['stories_count']} stories")
        print(f"      📍 Collection: {user['collection']}")
        print(f"      💡 Reason: {user['reason']}")
        print()
    
    print(f"\n❌ USERS TO REMOVE ({len(remove_users)}):")
    for user in remove_users[:10]:  # Show first 10
        print(f"   🗑️  {user['name']} ({user['email']}) - {user['stories_count']} stories")
        print(f"      📍 Collection: {user['collection']}")
        print(f"      💡 Reason: {user['reason']}")
    
    if len(remove_users) > 10:
        print(f"   ... and {len(remove_users) - 10} more users")
    
    # Count stories to be removed
    remove_user_ids = {user['id'] for user in remove_users}
    stories_to_remove = []
    for user_id in remove_user_ids:
        if user_id in stories_by_user:
            stories_to_remove.extend(stories_by_user[user_id])
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"   🟢 Keep: {len(keep_users)} users")
    print(f"   🔴 Remove: {len(remove_users)} users")
    print(f"   📚 Stories to remove: {len(stories_to_remove)}")
    print(f"   📚 Stories to keep: {sum(user['stories_count'] for user in keep_users)}")
    
    if not dry_run:
        print(f"\n⚠️  PERFORMING ACTUAL CLEANUP...")
        
        # Remove users and their stories
        removed_users = 0
        removed_stories = 0
        
        for user in remove_users:
            try:
                # Remove user's stories first
                user_stories = stories_by_user.get(user['id'], [])
                for story_doc in user_stories:
                    db.collection('stories').document(story_doc.id).delete()
                    removed_stories += 1
                
                # Remove user
                db.collection(user['collection']).document(user['id']).delete()
                removed_users += 1
                
                if removed_users % 50 == 0:
                    print(f"   Removed {removed_users} users and {removed_stories} stories...")
                
            except Exception as e:
                print(f"   ❌ Error removing user {user['id']}: {e}")
        
        print(f"\n✅ CLEANUP COMPLETED!")
        print(f"   🗑️  Removed {removed_users} users")
        print(f"   🗑️  Removed {removed_stories} stories")
        print(f"   🟢 Kept {len(keep_users)} quality accounts")
    
    else:
        print(f"\n🔍 This was a DRY RUN - no changes made")
        print(f"   To perform actual cleanup, run with --execute flag")

def main():
    """Main execution function"""
    print("🧹 Firebase Selective Cleanup Tool")
    print("Preserves quality accounts while removing test data")
    print("=" * 60)
    
    # Check for execute flag
    dry_run = '--execute' not in sys.argv
    if dry_run:
        print("🔍 Running in DRY RUN mode (no changes will be made)")
        print("   Add --execute flag to perform actual cleanup")
    else:
        print("⚠️  EXECUTE mode - changes will be permanent!")
        response = input("   Are you sure you want to proceed? (yes/no): ")
        if response.lower() != 'yes':
            print("   Cleanup cancelled.")
            return
    
    print()
    
    # Initialize Firebase
    db = initialize_firebase()
    if not db:
        return
    
    # Perform cleanup
    selective_cleanup(db, dry_run)
    
    print(f"\n📋 Cleanup {'simulation' if dry_run else 'operation'} completed!")

if __name__ == "__main__":
    main() 