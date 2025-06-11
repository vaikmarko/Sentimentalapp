#!/usr/bin/env python3
"""
Script to check stella.taht@icloud.com password hash
"""

import os
import sys
sys.path.append('.')

# Import app context to get database connection
from app import db

def check_stella_hash():
    try:
        if db is None:
            print("❌ Database not available")
            return False
        
        # Find stella's user record
        users = db.collection('test_users').where('email', '==', 'stella.taht@icloud.com').get()
        users_list = list(users)
        
        if len(users_list) == 0:
            print('❌ User stella.taht@icloud.com not found')
            return False
        
        user_doc = users_list[0]
        user_data = user_doc.to_dict()
        
        print(f'📧 Email: {user_data.get("email")}')
        print(f'👤 Name: {user_data.get("name")}')
        print(f'🔑 Stored hash: {user_data.get("password_hash")}')
        print(f'🔍 Expected hash for "stella123": {str(hash("stella123"))}')
        print(f'✅ Hashes match: {user_data.get("password_hash") == str(hash("stella123"))}')
        
        # Let's also try updating with a simple known password
        simple_hash = str(hash("test123"))
        print(f'🔍 Hash for "test123": {simple_hash}')
        
        return True
        
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == '__main__':
    check_stella_hash() 