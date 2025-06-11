#!/usr/bin/env python3
"""
Script to check stories for stella's accounts
"""

import os
import sys
sys.path.append('.')

from app import db

def check_stella_stories():
    try:
        if db is None:
            print("❌ Database not available")
            return False
        
        # Check stories for both accounts
        account_ids = ['0NtyrmOJMJOOn192yhPs', 'ver822PXIQalqOkkg0ir']
        
        for account_id in account_ids:
            print(f"🔍 Checking stories for account {account_id}:")
            
            # Get stories for this user
            stories = db.collection('test_stories').where('user_id', '==', account_id).get()
            stories_list = list(stories)
            
            print(f"  Found {len(stories_list)} stories")
            
            for i, story_doc in enumerate(stories_list):
                story_data = story_doc.to_dict()
                print(f"  Story {i+1}:")
                print(f"    📄 Story ID: {story_doc.id}")
                print(f"    📝 Title: {story_data.get('title', 'No title')}")
                print(f"    📅 Created: {story_data.get('created_at')}")
                print(f"    🔒 Privacy: {story_data.get('privacy_setting', 'unknown')}")
                print()
        
        return True
        
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == '__main__':
    check_stella_stories() 