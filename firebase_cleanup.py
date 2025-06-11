#!/usr/bin/env python3
"""
Firebase Cleanup Script for Sentimental App
Smart cleanup that preserves valuable content while removing test data
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime

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

def load_audit_results():
    """Load the audit results"""
    try:
        with open('firebase_audit_results.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Please run firebase_data_audit.py first!")
        exit(1)

def confirm_cleanup(audit_results):
    """Confirm cleanup plan with user"""
    print(f"\n🧹 CLEANUP PLAN CONFIRMATION")
    print("=" * 50)
    
    total_users = audit_results['user_analysis']['total_users']
    users_to_keep = len(audit_results['cleanup_plan']['users_to_keep'])
    users_to_remove = total_users - users_to_keep
    
    total_stories = audit_results['story_analysis']['total_stories']
    stories_to_keep = len(audit_results['cleanup_plan']['stories_to_keep'])
    stories_to_remove = total_stories - stories_to_keep
    
    print(f"   👥 Users: {total_users} → {users_to_keep} (remove {users_to_remove})")
    print(f"   📚 Stories: {total_stories} → {stories_to_keep} (remove {stories_to_remove})")
    
    print(f"\n   ✅ WILL PRESERVE:")
    marcus_users = audit_results['user_analysis']['marcus_users']
    for marcus in marcus_users:
        print(f"      🎯 Marcus: {marcus['name']} ({marcus['email']})")
    
    print(f"      📖 All {stories_to_keep} quality stories (>200 chars)")
    print(f"      ✨ All stories with formats")
    print(f"      🌍 All public stories")
    
    print(f"\n   🗑️  WILL REMOVE:")
    print(f"      👥 {users_to_remove} test/inactive users")
    print(f"      💬 Empty conversations and connections")
    print(f"      🧹 Orphaned data")
    
    response = input(f"\n   ❓ Proceed with cleanup? (type 'yes' to confirm): ")
    return response.lower() == 'yes'

def backup_important_data(audit_results):
    """Create backup of important data before cleanup"""
    print(f"\n💾 Creating backup...")
    
    backup_data = {
        'timestamp': datetime.now().isoformat(),
        'marcus_users': audit_results['user_analysis']['marcus_users'],
        'quality_stories': [],
        'active_users': audit_results['user_analysis']['active_users']
    }
    
    # Backup quality stories
    for story in audit_results['story_analysis']['quality_stories']:
        backup_data['quality_stories'].append({
            'id': story['doc_id'],
            'title': story.get('title', 'No title'),
            'author': story.get('author', 'Unknown'),
            'content_length': len(story.get('content', '')),
            'formats': story.get('createdFormats', []),
            'public': story.get('public', False)
        })
    
    backup_filename = f"firebase_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_filename, 'w') as f:
        json.dump(backup_data, f, indent=2, default=str)
    
    print(f"   ✅ Backup saved to {backup_filename}")
    return backup_filename

def clean_users(users_to_keep):
    """Remove test users while keeping quality users"""
    print(f"\n👥 Cleaning users...")
    
    collections_to_clean = ['test_users', 'users']
    total_removed = 0
    
    for collection_name in collections_to_clean:
        try:
            users = list(db.collection(collection_name).stream())
            for user_doc in users:
                if user_doc.id not in users_to_keep:
                    user_data = user_doc.to_dict()
                    name = user_data.get('name', 'Unknown')
                    email = user_data.get('email', 'No email')
                    
                    print(f"   🗑️  Removing: {name[:20]} ({email[:30]})")
                    user_doc.reference.delete()
                    total_removed += 1
                else:
                    user_data = user_doc.to_dict()
                    name = user_data.get('name', 'Unknown')
                    print(f"   ✅ Keeping: {name[:20]}")
        
        except Exception as e:
            print(f"   ❌ Error cleaning {collection_name}: {e}")
    
    print(f"   📊 Removed {total_removed} users")

def clean_conversations():
    """Clean up conversation data"""
    print(f"\n💬 Cleaning conversations...")
    
    try:
        conversations = list(db.collection('conversations').stream())
        removed_count = 0
        
        for conv_doc in conversations:
            conv_data = conv_doc.to_dict()
            message_count = conv_data.get('message_count', 0)
            
            # Remove conversations with very few messages or test data
            if message_count < 3:
                conv_doc.reference.delete()
                removed_count += 1
            
        print(f"   📊 Removed {removed_count} minimal conversations")
        print(f"   ✅ Kept {len(conversations) - removed_count} meaningful conversations")
        
    except Exception as e:
        print(f"   ❌ Error cleaning conversations: {e}")

def clean_empty_collections():
    """Clean up empty collections"""
    print(f"\n🧹 Cleaning empty collections...")
    
    empty_collections = ['chat_messages', 'story_formats', 'connections']
    
    for collection_name in empty_collections:
        try:
            docs = list(db.collection(collection_name).stream())
            if docs:
                for doc in docs:
                    doc.reference.delete()
                print(f"   🗑️  Cleaned {len(docs)} docs from {collection_name}")
            else:
                print(f"   ✅ {collection_name} already empty")
        except Exception as e:
            print(f"   ❌ Error cleaning {collection_name}: {e}")

def optimize_stories():
    """Optimize story data structure"""
    print(f"\n📚 Optimizing stories...")
    
    try:
        stories = list(db.collection('stories').stream())
        
        for story_doc in stories:
            story_data = story_doc.to_dict()
            
            # Ensure story has proper structure
            updates = {}
            
            # Ensure proper timestamp format
            if 'created_at' not in story_data:
                updates['created_at'] = firestore.SERVER_TIMESTAMP
            
            # Ensure proper format tracking
            if 'createdFormats' not in story_data:
                formats = story_data.get('formats', {})
                updates['createdFormats'] = list(formats.keys()) if formats else []
            
            # Update if needed
            if updates:
                story_doc.reference.update(updates)
                title = story_data.get('title', 'Untitled')[:30]
                print(f"   ✅ Updated: {title}...")
        
        print(f"   📊 Optimized {len(stories)} stories")
        
    except Exception as e:
        print(f"   ❌ Error optimizing stories: {e}")

def create_test_user():
    """Create a fresh test user for continued testing"""
    print(f"\n🧪 Creating fresh test user...")
    
    test_user_data = {
        'email': 'test@sentimentalapp.com',
        'name': 'Test User',
        'created_at': datetime.now().isoformat(),
        'stories_created': 0,
        'formats_generated': 0,
        'conversations_count': 0,
        'is_test_user': True
    }
    
    try:
        user_ref = db.collection('test_users').add(test_user_data)
        test_user_id = user_ref[1].id
        print(f"   ✅ Created test user: {test_user_id}")
        return test_user_id
    except Exception as e:
        print(f"   ❌ Error creating test user: {e}")
        return None

def main():
    """Main cleanup function"""
    print("🧹 SENTIMENTAL APP FIREBASE CLEANUP")
    print("=" * 60)
    
    # Load audit results
    audit_results = load_audit_results()
    
    # Confirm cleanup plan
    if not confirm_cleanup(audit_results):
        print("   ❌ Cleanup cancelled by user")
        return
    
    # Create backup
    backup_filename = backup_important_data(audit_results)
    
    print(f"\n🚀 Starting cleanup...")
    
    # Execute cleanup steps
    users_to_keep = audit_results['cleanup_plan']['users_to_keep']
    
    clean_users(users_to_keep)
    clean_conversations()
    clean_empty_collections()
    optimize_stories()
    
    # Create fresh test user
    test_user_id = create_test_user()
    
    print(f"\n🎉 CLEANUP COMPLETE!")
    print("=" * 40)
    print(f"   💾 Backup: {backup_filename}")
    print(f"   👥 Users kept: {len(users_to_keep)}")
    print(f"   📚 Stories kept: {len(audit_results['cleanup_plan']['stories_to_keep'])}")
    print(f"   🧪 New test user: {test_user_id}")
    
    print(f"\n✨ Your database is now clean and optimized!")
    print(f"   🎯 Marcus Rodriguez data preserved")
    print(f"   📖 All quality stories maintained")
    print(f"   🔄 Ready for fresh testing")

if __name__ == "__main__":
    main() 