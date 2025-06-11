import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
if os.path.exists('firebase-credentials.json'):
    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    print("🔍 Checking for Stella's chat data...")
    
    # Find users with Stella in name/email
    users = db.collection('users').get()
    stella_users = []
    for user in users:
        data = user.to_dict()
        if any(term in str(data).lower() for term in ['stella', 'test']):
            stella_users.append((user.id, data))
            print(f"👤 User: {user.id}")
            print(f"   Email: {data.get('email', 'N/A')}")
            print(f"   Name: {data.get('displayName', 'N/A')}")
            print()
    
    # Check recent conversations
    print("💬 Recent conversations:")
    conversations = db.collection('conversations').order_by('created_at', direction=firestore.Query.DESCENDING).limit(10).get()
    for conv in conversations:
        data = conv.to_dict()
        if 'messages' in data and data['messages']:
            print(f"🗨️ Conversation: {conv.id}")
            print(f"   User: {data.get('user_id', 'Unknown')}")
            print(f"   Created: {data.get('created_at', 'Unknown')}")
            print(f"   Messages ({len(data['messages'])}):")
            for msg in data['messages'][-3:]:  # Last 3 messages
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')[:100] + ('...' if len(msg.get('content', '')) > 100 else '')
                print(f"     {role}: {content}")
            print()
    
    # Check for any chat errors in logs collection
    try:
        logs = db.collection('chat_logs').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(5).get()
        if logs:
            print("⚠️ Recent chat logs:")
            for log in logs:
                data = log.to_dict()
                print(f"   {data.get('timestamp', 'Unknown')}: {data.get('message', 'No message')}")
    except:
        print("📝 No chat_logs collection found")
        
else:
    print("❌ firebase-credentials.json not found") 