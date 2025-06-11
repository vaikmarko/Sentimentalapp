#!/usr/bin/env python3
"""
Script to fix duplicate accounts for stella.taht@icloud.com
- Delete the newer account with 0 stories
- Keep the older account with the story "Growing Together with My Husband"
"""

import os
import sys
sys.path.append('.')

from app import db

def fix_stella_duplicates():
    try:
        if db is None:
            print("❌ Database not available")
            return False
        
        # Find both accounts
        users = db.collection('test_users').where('email', '==', 'stella.taht@icloud.com').get()
        users_list = list(users)
        
        if len(users_list) != 2:
            print(f"❌ Expected 2 accounts, found {len(users_list)}")
            return False
        
        # Identify which account to keep and which to delete
        account_to_keep = None
        account_to_delete = None
        
        for user_doc in users_list:
            user_data = user_doc.to_dict()
            stories_count = user_data.get('stories_created', 0)
            doc_id = user_doc.id
            created_at = user_data.get('created_at')
            
            print(f"Account {doc_id}:")
            print(f"  Created: {created_at}")
            print(f"  Stories: {stories_count}")
            
            if stories_count > 0:
                account_to_keep = user_doc
                print(f"  → KEEP (has stories)")
            else:
                account_to_delete = user_doc
                print(f"  → DELETE (no stories)")
            print()
        
        if not account_to_keep or not account_to_delete:
            print("❌ Could not identify which account to keep/delete")
            return False
        
        # Confirm deletion
        keep_data = account_to_keep.to_dict()
        delete_data = account_to_delete.to_dict()
        
        print(f"✅ PLAN:")
        print(f"  KEEP: {account_to_keep.id} (created {keep_data.get('created_at')}, {keep_data.get('stories_created', 0)} stories)")
        print(f"  DELETE: {account_to_delete.id} (created {delete_data.get('created_at')}, {delete_data.get('stories_created', 0)} stories)")
        print()
        
        # Delete the duplicate account
        account_to_delete.reference.delete()
        print(f"🗑️ Deleted duplicate account: {account_to_delete.id}")
        
        # Verify only one account remains
        users_after = db.collection('test_users').where('email', '==', 'stella.taht@icloud.com').get()
        users_after_list = list(users_after)
        
        if len(users_after_list) == 1:
            remaining_account = users_after_list[0]
            print(f"✅ Success! Only one account remains: {remaining_account.id}")
            print(f"   Stella can now log in with stella.taht@icloud.com")
            return True
        else:
            print(f"❌ Error: Expected 1 account after deletion, found {len(users_after_list)}")
            return False
        
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == '__main__':
    fix_stella_duplicates() 