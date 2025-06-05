#!/usr/bin/env python3
import requests
import time

BASE_URL = "http://localhost:8080"

# Use the existing test users we created
EXISTING_USERS = [
    'maya_deep_thinker',
    'jack_social_butterfly', 
    'riley_creative_soul',
    'alex_ambitious_burnout',
    'sam_anxious_achiever'
]

def generate_story_for_user(user_id):
    """Generate a story from existing conversation for a user"""
    print(f"📚 Generating story for {user_id}...")
    
    # Send a message that triggers story creation
    final_message = "I want to create a story from our conversation. Please generate a thoughtful story that captures the essence of what we've discussed."
    
    response = requests.post(f"{BASE_URL}/api/chat/message", 
        json={
            "message": final_message,
            "generate_story": True
        },
        headers={"X-User-ID": user_id}
    )
    
    if response.status_code in [200, 201]:
        data = response.json()
        if data.get('story_created') or data.get('story_id'):
            print(f"   ✅ Story created: {data.get('story_id', 'Success')}")
            return True
        else:
            print(f"   ⚠️  Response: {data.get('message', 'Story generation triggered')}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        try:
            error_data = response.json()
            print(f"      Error: {error_data.get('error', 'Unknown error')}")
        except:
            pass
    
    return False

def main():
    print("🚀 GENERATING STORIES FROM EXISTING CONVERSATIONS")
    print("=" * 55)
    
    # Delete existing stories first
    print("1️⃣ Clearing existing stories...")
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        stories = response.json()
        for story in stories:
            try:
                requests.delete(f"{BASE_URL}/api/stories/{story['id']}")
                print(f"   🗑️  Deleted: {story.get('title', 'Untitled')}")
            except:
                pass
    
    print(f"\n2️⃣ Generating stories for {len(EXISTING_USERS)} users...")
    
    success_count = 0
    for i, user_id in enumerate(EXISTING_USERS, 1):
        print(f"\n{i}. {user_id}")
        if generate_story_for_user(user_id):
            success_count += 1
        
        # Wait between requests
        if i < len(EXISTING_USERS):
            time.sleep(3)
    
    # Check results
    print(f"\n3️⃣ Final Results:")
    print("=" * 30)
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        stories = response.json()
        print(f"✅ Stories created: {len(stories)}")
        for story in stories:
            word_count = len(story.get('content', '').split())
            print(f"   📖 \"{story.get('title', 'Untitled')}\" ({word_count} words)")
    else:
        print("❌ Failed to check stories")
    
    print(f"\n🎊 Success rate: {success_count}/{len(EXISTING_USERS)}")

if __name__ == "__main__":
    main() 