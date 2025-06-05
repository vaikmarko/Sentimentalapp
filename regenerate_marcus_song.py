#!/usr/bin/env python3

import requests
import json

# Marcus story ID from the logs
STORY_ID = "7UV1cWhMHbnVVNK4m5HB"
BASE_URL = "http://127.0.0.1:8080"

def regenerate_song():
    """Regenerate song for Marcus story to test the current system"""
    
    print(f"Regenerating song for Marcus story: {STORY_ID}")
    
    # Trigger song generation
    generate_url = f"{BASE_URL}/api/stories/{STORY_ID}/generate-format"
    
    try:
        response = requests.post(generate_url, json={"format_type": "song"})
        
        if response.status_code == 200:
            print("✅ Song generation successful!")
            result = response.json()
            print(f"Generated song data: {json.dumps(result, indent=2)}")
            
            # Get the generated song
            get_url = f"{BASE_URL}/api/stories/{STORY_ID}/formats/song"
            get_response = requests.get(get_url)
            
            if get_response.status_code == 200:
                song_data = get_response.json()
                print("\n📋 Generated Song:")
                print(f"Title: {song_data.get('title', 'No title')}")
                print(f"Content preview: {song_data.get('content', 'No content')[:200]}...")
                
                # Check if it has verse labels (bad) or no labels (good)
                content = song_data.get('content', '')
                if '[Verse' in content or 'Verse:' in content:
                    print("⚠️  WARNING: Song still contains verse labels - old system being used")
                else:
                    print("✅ Good: No verse labels found - prompts engine working!")
                    
                if song_data.get('title') == 'Default Title':
                    print("⚠️  WARNING: Still showing 'Default Title'")
                else:
                    print(f"✅ Good: Proper title extracted: {song_data.get('title')}")
                    
            else:
                print(f"❌ Failed to retrieve song: {get_response.status_code}")
                
        else:
            print(f"❌ Song generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    regenerate_song() 