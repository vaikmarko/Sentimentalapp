import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

def clear_collection(collection_name):
    """Delete all documents in a collection"""
    docs = db.collection(collection_name).stream()
    count = 0
    for doc in docs:
        doc.reference.delete()
        count += 1
    print(f'Deleted {count} documents from {collection_name}')

# Clear all test data
print('Clearing test data...')
clear_collection('stories')
clear_collection('connections')
clear_collection('chat_messages')
print('Test data cleared successfully!') 