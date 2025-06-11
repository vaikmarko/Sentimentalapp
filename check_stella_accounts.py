#!/usr/bin/env python3
"""
Script to check for duplicate accounts for stella.taht@icloud.com
"""

import os
import sys
sys.path.append('.')

from app import db

def check_stella_accounts():
    try:
        if db is None:
            print("❌ Database not available")
            return False
        
        # Find all accounts with stella's email
        users = db.collection('test_users').where('email', '==', 'stella.taht@icloud.com').get()
        users_list = list(users)
        
        print(f'Found {len(users_list)} accounts for stella.taht@icloud.com:')
        print()
        
        for i, user_doc in enumerate(users_list):
            user_data = user_doc.to_dict()
            print(f'Account {i+1}:')
            print(f'  📄 Doc ID: {user_doc.id}')
            print(f'  👤 Name: {user_data.get("name")}')
            print(f'  📧 Email: {user_data.get("email")}')
            print(f'  📅 Created: {user_data.get("created_at")}')
            print(f'  📚 Stories: {user_data.get("stories_created", 0)}')
            print(f'  🔗 Provider: {user_data.get("provider", "unknown")}')
            print(f'  🆔 Firebase UID: {user_data.get("firebase_uid", "none")}')
            print(f'  🔑 Has Password Hash: {"yes" if user_data.get("password_hash") else "no"}')
            print()
        
        return True
        
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == '__main__':
    check_stella_accounts() 