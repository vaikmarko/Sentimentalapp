#!/usr/bin/env python3
"""
Script to update stella.taht@icloud.com password to stella123
"""

import os
import sys
sys.path.append('.')

# Import app context to get database connection
from app import db
from datetime import datetime

def update_stella_password():
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
        
        # Calculate new password hash (same method as login system)
        new_password = 'stella123'
        new_password_hash = str(hash(new_password))
        
        # Update the user
        user_doc.reference.update({
            'password_hash': new_password_hash,
            'last_login': datetime.now().isoformat()
        })
        
        print(f'✅ Updated password for stella.taht@icloud.com')
        print(f'📧 Email: {user_data.get("email")}')
        print(f'👤 Name: {user_data.get("name")}')
        print(f'🔑 New password: stella123')
        print(f'🆔 User ID: {user_doc.id}')
        return True
        
    except Exception as e:
        print(f'❌ Error updating password: {e}')
        return False

if __name__ == '__main__':
    success = update_stella_password()
    sys.exit(0 if success else 1) 