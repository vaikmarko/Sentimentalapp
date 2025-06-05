import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
try:
    if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
        firebase_admin.initialize_app()
    else:
        cred = credentials.Certificate('firebase-credentials.json')
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    print('🧹 Starting database cleanup...\n')
    
    # Define criteria for meaningful stories
    MIN_CONTENT_LENGTH = 200  # Minimum content length to keep
    
    # Get all stories
    stories = db.collection('stories').stream()
    
    stories_to_keep = []
    stories_to_delete = []
    
    for story in stories:
        story_data = story.to_dict()
        story_id = story.id
        
        title = story_data.get('title', '').strip()
        author = story_data.get('author', '').strip()
        content = story_data.get('content', '').strip()
        
        # Criteria for keeping a story:
        # 1. Has meaningful content (>200 chars)
        # 2. Has a proper title (not "No title" or empty)
        # 3. Has a proper author (not "No author" or empty)
        # 4. Content is not just test data
        
        should_keep = (
            len(content) >= MIN_CONTENT_LENGTH and
            title and title != "No title" and
            author and author != "No author" and
            not content.lower().startswith('this is a test') and
            not title.lower().startswith('test')
        )
        
        if should_keep:
            stories_to_keep.append({
                'id': story_id,
                'title': title,
                'author': author,
                'content_length': len(content)
            })
        else:
            stories_to_delete.append({
                'id': story_id,
                'title': title or 'No title',
                'author': author or 'No author',
                'content_length': len(content)
            })
    
    print(f'📊 Analysis Results:')
    print(f'   Stories to KEEP: {len(stories_to_keep)}')
    print(f'   Stories to DELETE: {len(stories_to_delete)}')
    print()
    
    print('✅ Stories to KEEP:')
    for story in stories_to_keep:
        print(f'   - "{story["title"]}" by {story["author"]} ({story["content_length"]} chars)')
    print()
    
    print('❌ Stories to DELETE:')
    for story in stories_to_delete[:10]:  # Show first 10
        print(f'   - "{story["title"]}" by {story["author"]} ({story["content_length"]} chars)')
    if len(stories_to_delete) > 10:
        print(f'   ... and {len(stories_to_delete) - 10} more')
    print()
    
    # Ask for confirmation
    response = input('Do you want to proceed with the cleanup? (yes/no): ').lower().strip()
    
    if response == 'yes':
        print('\n🗑️  Deleting stories...')
        deleted_count = 0
        
        for story in stories_to_delete:
            try:
                db.collection('stories').document(story['id']).delete()
                deleted_count += 1
                print(f'   Deleted: {story["title"]} ({story["id"]})')
            except Exception as e:
                print(f'   Error deleting {story["id"]}: {e}')
        
        print(f'\n✅ Deleted {deleted_count} stories')
        
        # Clean up other collections
        print('\n🧹 Cleaning up other collections...')
        
        # Delete test users (keep only real users with proper emails)
        print('   Cleaning test_users collection...')
        users = db.collection('test_users').stream()
        test_users_deleted = 0
        for user in users:
            user_data = user.to_dict()
            email = user_data.get('email', '')
            # Delete test users
            if 'test' in email.lower() or 'example.com' in email.lower():
                db.collection('test_users').document(user.id).delete()
                test_users_deleted += 1
                print(f'     Deleted test user: {email}')
        
        # Delete all connections (they'll be regenerated)
        print('   Cleaning connections collection...')
        connections = db.collection('connections').stream()
        connections_deleted = 0
        for conn in connections:
            db.collection('connections').document(conn.id).delete()
            connections_deleted += 1
        
        # Delete chat messages
        print('   Cleaning chat_messages collection...')
        messages = db.collection('chat_messages').stream()
        messages_deleted = 0
        for msg in messages:
            db.collection('chat_messages').document(msg.id).delete()
            messages_deleted += 1
        
        print(f'\n📈 Cleanup Summary:')
        print(f'   Stories deleted: {deleted_count}')
        print(f'   Stories kept: {len(stories_to_keep)}')
        print(f'   Test users deleted: {test_users_deleted}')
        print(f'   Connections deleted: {connections_deleted}')
        print(f'   Chat messages deleted: {messages_deleted}')
        print('\n✨ Database cleanup completed!')
        
    else:
        print('\n❌ Cleanup cancelled.')
    
except Exception as e:
    print(f'Error: {e}') 