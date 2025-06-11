#!/usr/bin/env python3
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('firebase-credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Search for Merike and Lars by name and email patterns
print('Searching for Merike and Lars with various email patterns...')

# Check test_users collection
users_ref = db.collection('test_users')
for doc in users_ref.stream():
    data = doc.to_dict()
    name = data.get('name', '').lower()
    email = data.get('email', '').lower()
    
    # Look for Merike and Lars by name OR email patterns
    if ('merike' in name or 'lars' in name or 
        'merike' in email or 'lars' in email or
        'sisask' in name or 'sisask' in email or
        'hion' in name or 'hion' in email):
        print(f'Found in test_users: {data.get("name", "No name")} - {data.get("email", "")}')

# Check users collection  
users_ref = db.collection('users')
for doc in users_ref.stream():
    data = doc.to_dict()
    name = data.get('name', '').lower()
    email = data.get('email', '').lower()
    
    # Look for Merike and Lars by name OR email patterns
    if ('merike' in name or 'lars' in name or 
        'merike' in email or 'lars' in email or
        'sisask' in name or 'sisask' in email or
        'hion' in name or 'hion' in email):
        print(f'Found in users: {data.get("name", "No name")} - {data.get("email", "")}')

print('\nAlso checking for any Gmail addresses that might be theirs...')

# Check for Gmail addresses
users_ref = db.collection('test_users')
gmail_users = []
for doc in users_ref.stream():
    data = doc.to_dict()
    email = data.get('email', '')
    if '@gmail.com' in email:
        gmail_users.append((data.get('name', 'No name'), email))

# Sort and show Gmail users
gmail_users.sort()
print(f'Found {len(gmail_users)} Gmail users in test_users:')
for name, email in gmail_users:
    print(f'  {name} - {email}') 