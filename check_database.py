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
    
    print('=== STORIES COLLECTION ===')
    stories = db.collection('stories').stream()
    story_count = 0
    for story in stories:
        story_data = story.to_dict()
        story_count += 1
        print(f'ID: {story.id}')
        print(f'Title: {story_data.get("title", "No title")}')
        print(f'Author: {story_data.get("author", "No author")}')
        print(f'Content length: {len(story_data.get("content", ""))} chars')
        print(f'User ID: {story_data.get("user_id", "No user_id")}')
        print(f'Public: {story_data.get("public", "Unknown")}')
        print('---')
    
    print(f'Total stories: {story_count}')
    
    print('\n=== TEST USERS COLLECTION ===')
    users = db.collection('test_users').stream()
    user_count = 0
    for user in users:
        user_data = user.to_dict()
        user_count += 1
        print(f'ID: {user.id}')
        print(f'Email: {user_data.get("email", "No email")}')
        print(f'Name: {user_data.get("name", "No name")}')
        print('---')
    
    print(f'Total test users: {user_count}')
    
    print('\n=== CHAT MESSAGES COLLECTION ===')
    messages = db.collection('chat_messages').stream()
    message_count = 0
    for msg in messages:
        message_count += 1
    
    print(f'Total chat messages: {message_count}')
    
    print('\n=== CONNECTIONS COLLECTION ===')
    connections = db.collection('connections').stream()
    conn_count = 0
    for conn in connections:
        conn_count += 1
    
    print(f'Total connections: {conn_count}')
    
    print('\n=== WAITLIST COLLECTION ===')
    waitlist = db.collection('waitlist').stream()
    waitlist_count = 0
    for entry in waitlist:
        waitlist_count += 1
    
    print(f'Total waitlist entries: {waitlist_count}')
    
except Exception as e:
    print(f'Error: {e}') 