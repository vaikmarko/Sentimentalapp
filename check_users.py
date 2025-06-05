#!/usr/bin/env python3
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase
if not firebase_admin._apps:
    cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        
        users = list(db.collection('test_users').stream())
        print(f'Found {len(users)} users:')
        for user in users[:10]:  # First 10 users
            data = user.to_dict()
            print(f'  {user.id}: {data.get("name", "No name")}')
    else:
        print('Firebase not configured') 