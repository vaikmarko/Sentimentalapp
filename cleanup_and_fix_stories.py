#!/usr/bin/env python3
"""Clean up stories: remove old poetic ones, fix user names, and remove duplicates"""

import requests
import json
from collections import defaultdict

BASE_URL = "http://localhost:8080"

def cleanup_and_fix_stories():
    print("🧹 CLEANING UP AND FIXING STORIES")
    print("=" * 50)
    
    # Get all stories
    print("1️⃣ Fetching all stories...")
    response = requests.get(f"{BASE_URL}/api/stories")
    
    if response.status_code != 200:
        print(f"❌ Failed to get stories: {response.status_code}")
        return
    
    stories = response.json()
    print(f"✅ Found {len(stories)} total stories")
    
    # Define poetic titles to remove (old versions)
    poetic_titles = [
        "Blossoming in Silence",
        "Embracing the Shadows Within", 
        "The Dance of Uncertain Hearts",
        "Finding Solace in the Shadows",
        "Embracing the Shadows of Time",
        "The Fragile Thread of Resilience", 
        "Whispers of the Heart's Truth"
    ]
    
    # User names for each user ID (realistic names for 16-30 year olds)
    user_names = {
        'user_51843': 'Alex Rivera',
        'user_35946': 'Jordan Chen', 
        'user_42869': 'Sam Taylor',
        'user_66639': 'Riley Kim',
        'user_36196': 'Casey Morgan',
        'user_24016': 'Alex Rivera',  # Same person, different story
        'test_user_debug': 'Debug User'
    }
    
    # Natural titles - these are the good ones we want to keep
    natural_titles = [
        "Figuring Out Emotion",
        "Figuring Out Discovery", 
        "What I Learned About Relationship",
        "My Personal Journey",
        "My Experience with Discovery",
        "Surviving Day One at My New Job"
    ]
    
    # Detect duplicates by user_id and title
    user_stories = defaultdict(list)
    for story in stories:
        user_id = story.get('user_id')
        if user_id:
            user_stories[user_id].append(story)
    
    # Find stories to delete and update
    stories_to_delete = []
    stories_to_update = []
    duplicate_stories = []
    
    # First, delete all poetic titles
    stories_to_delete.extend([s for s in stories if s['title'] in poetic_titles])
    
    # Then find duplicates for each user
    for user_id, user_story_list in user_stories.items():
        if len(user_story_list) > 1:
            print(f"   👤 User {user_id} has {len(user_story_list)} stories")
            
            # Group by title similarity and naturalness
            natural_stories = [s for s in user_story_list if s['title'] in natural_titles]
            poetic_stories = [s for s in user_story_list if s['title'] in poetic_titles]
            
            # If user has both natural and poetic versions, delete poetic ones
            if natural_stories and poetic_stories:
                stories_to_delete.extend(poetic_stories)
                print(f"      🗑️  Will delete {len(poetic_stories)} poetic stories for this user")
            
            # Check for duplicate natural titles
            title_count = defaultdict(list)
            for story in natural_stories:
                title_count[story['title']].append(story)
            
            for title, story_list in title_count.items():
                if len(story_list) > 1:
                    # Keep the most recent one, delete older duplicates
                    sorted_stories = sorted(story_list, key=lambda x: x.get('timestamp', ''), reverse=True)
                    duplicate_stories.extend(sorted_stories[1:])  # Delete all but the newest
                    print(f"      🔄 Found {len(sorted_stories)-1} duplicates of '{title}'")
    
    # Add duplicates to deletion list
    stories_to_delete.extend(duplicate_stories)
    
    # Remove duplicates from delete list
    stories_to_delete = list({s['id']: s for s in stories_to_delete}.values())
    
    # Find stories to update (natural titles with "You" as author, not in delete list)
    delete_ids = {s['id'] for s in stories_to_delete}
    stories_to_update = [
        s for s in stories 
        if s['title'] in natural_titles 
        and s.get('author') == 'You' 
        and s['id'] not in delete_ids
    ]
    
    print(f"🗑️  Found {len(stories_to_delete)} total stories to delete")
    print(f"🔧 Found {len(stories_to_update)} natural stories needing proper author names")
    print(f"🔄 Found {len(duplicate_stories)} duplicate stories to remove")
    
    deleted_count = 0
    updated_count = 0
    
    # Create authentication headers using a test user
    auth_headers = {'X-User-ID': 'user_51843'}  # Use existing user for auth
    
    # Delete stories
    print(f"\n2️⃣ Deleting stories...")
    for story in stories_to_delete:
        try:
            delete_response = requests.delete(
                f"{BASE_URL}/api/stories/{story['id']}", 
                headers=auth_headers
            )
            if delete_response.status_code in [200, 204]:
                reason = "poetic" if story['title'] in poetic_titles else "duplicate"
                print(f"   ✅ Deleted ({reason}): '{story['title']}'")
                deleted_count += 1
            else:
                print(f"   ❌ Failed to delete '{story['title']}': {delete_response.status_code}")
                if delete_response.text:
                    error_data = delete_response.json() if delete_response.headers.get('content-type', '').startswith('application/json') else delete_response.text
                    print(f"      Error: {error_data}")
        except Exception as e:
            print(f"   ❌ Error deleting '{story['title']}': {e}")
    
    # Update natural stories with proper user names
    print(f"\n3️⃣ Updating author names in remaining stories...")
    for story in stories_to_update:
        try:
            user_id = story.get('user_id')
            user_name = user_names.get(user_id, f"User {user_id[-5:] if user_id else 'Unknown'}")
            
            # Prepare update data
            update_data = {
                'author': user_name
            }
            
            # Send PUT request to update the story
            update_response = requests.put(
                f"{BASE_URL}/api/stories/{story['id']}", 
                json=update_data,
                headers=auth_headers
            )
            
            if update_response.status_code in [200, 201]:
                print(f"   ✅ Updated '{story['title']}' → Author: {user_name}")
                updated_count += 1
            else:
                print(f"   ❌ Failed to update '{story['title']}': {update_response.status_code}")
                if update_response.text:
                    error_data = update_response.json() if update_response.headers.get('content-type', '').startswith('application/json') else update_response.text
                    print(f"      Error: {error_data}")
                
        except Exception as e:
            print(f"   ❌ Error updating '{story['title']}': {e}")
    
    print(f"\n🎉 CLEANUP COMPLETE!")
    print(f"   🗑️  Deleted: {deleted_count} stories (poetic + duplicates)")
    print(f"   🔧 Updated: {updated_count} stories with proper author names")
    print(f"   📊 Expected remaining stories: {len(stories) - deleted_count}")

def verify_cleanup():
    """Verify the cleanup worked"""
    print(f"\n4️⃣ Verifying cleanup...")
    response = requests.get(f"{BASE_URL}/api/stories")
    
    if response.status_code == 200:
        stories = response.json()
        print(f"✅ Final story count: {len(stories)}")
        
        # Group by user to detect remaining duplicates
        user_stories = defaultdict(list)
        for story in stories:
            user_id = story.get('user_id', 'no_user')
            user_stories[user_id].append(story)
        
        print(f"\n📋 FINAL STORY LIST:")
        story_num = 1
        for user_id, user_story_list in user_stories.items():
            if len(user_story_list) > 1:
                print(f"\n👤 User {user_id} ({len(user_story_list)} stories):")
            
            for story in user_story_list:
                user_name = story.get('author', 'Unknown')
                title = story.get('title', 'No Title')
                naturalness = analyze_title_naturalness(title)
                natural_indicator = "✅" if naturalness else "❌"
                
                if len(user_story_list) > 1:
                    print(f"     {natural_indicator} \"{title}\" by {user_name}")
                else:
                    print(f"{story_num:2d}. {natural_indicator} \"{title}\" by {user_name} ({user_id})")
                    story_num += 1
        
        # Summary
        natural_count = sum(1 for s in stories if analyze_title_naturalness(s.get('title', '')))
        proper_name_count = sum(1 for s in stories if s.get('author') != 'You')
        
        # Check for remaining duplicates
        title_count = defaultdict(int)
        for story in stories:
            title_count[story.get('title', '')] += 1
        
        duplicate_titles = [title for title, count in title_count.items() if count > 1]
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total stories: {len(stories)}")
        print(f"   Natural titles: {natural_count}")
        print(f"   Poetic titles: {len(stories) - natural_count}")
        print(f"   Stories with proper names: {proper_name_count}")
        print(f"   Remaining duplicates: {len(duplicate_titles)} titles")
        
        if duplicate_titles:
            print(f"   ⚠️  Duplicate titles found: {duplicate_titles}")
        else:
            print(f"   ✅ No duplicate titles remaining")
        
    else:
        print(f"❌ Failed to verify: {response.status_code}")

def analyze_title_naturalness(title):
    """Quick check if title sounds natural vs poetic"""
    poetic_words = ['whisper', 'shadow', 'dance', 'thread', 'solace', 'embrace', 'ethereal', 'profound', 'tapestry', 'blossoming', 'embracing']
    return not any(word.lower() in title.lower() for word in poetic_words)

if __name__ == "__main__":
    try:
        cleanup_and_fix_stories()
        verify_cleanup()
    except KeyboardInterrupt:
        print("\n👋 Cleanup interrupted by user")
    except Exception as e:
        print(f"\n❌ Cleanup failed: {e}")
        import traceback
        traceback.print_exc() 