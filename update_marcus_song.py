#!/usr/bin/env python3

import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate('firebase-credentials.json')
        firebase_admin.initialize_app(cred)
        print("✅ Firebase initialized with service account")
    except Exception as e:
        try:
            firebase_admin.initialize_app()
            print("✅ Firebase initialized with default credentials")
        except Exception as e2:
            print(f"❌ Failed to initialize Firebase: {e2}")
            exit(1)

# Get Firestore client
db = firestore.client()

def update_marcus_song():
    """Update Marcus story song with new lyrics"""
    
    STORY_ID = "7UV1cWhMHbnVVNK4m5HB"
    
    # The new lyrics provided by the user
    new_lyrics = """TITLE: "This Is My Story"

Walking through the morning, staring at the ceiling
Got this gut feeling, it's time for some healing
man I had it figured out, but I was just pretending
Now I'm starting over, this is my new beginning

I've been lost in the maze of what they told me to be
But I'm breaking the chains, now I'm finally free
Every choice that I make, every step that I take
I'm becoming myself for my own sake

This is my story, this is my song
Been quiet too long, but now I'm strong
Finding my voice in the chaos and noise
This is my moment, this is my choice

Used to think that i've was about fitting the mold
But the real treasure is being brave and bold
Every mistake that I made taught me how to grow
Now I'm ready to let the whole world know

This is my story, this is my song
Been quiet too long, but now I'm strong
Finding my voice in the chaos and noise
This is my moment, this is my choice

I'm not perfect, but I'm real
This is how it feels to heal
To finally see who I'm meant to be
Setting my spirit free

This is my story, this is my song
Been quiet too long, but now I'm strong
Finding my voice in the chaos and noise
This is my moment, this is my choice

This is my story, and I'm just getting started"""

    print(f"🎵 Updating Marcus story song: {STORY_ID}")
    
    try:
        # Get current song data from Firestore
        story_ref = db.collection('stories').document(STORY_ID)
        story_doc = story_ref.get()
        
        if story_doc.exists:
            print(f"📋 Story found, updating song content...")
            story_data = story_doc.to_dict()
            
            # Get existing formats
            formats = story_data.get('formats', {})
            
            # Update the song format (include the uploaded MP3)
            formats['song'] = {
                'content': new_lyrics,
                'title': 'This Is My Story',
                'created_at': formats.get('song', {}).get('created_at', firestore.SERVER_TIMESTAMP),
                # Add the uploaded MP3 file
                'audio_url': '/static/uploads/7UV1cWhMHbnVVNK4m5HB_song_f84ffab5-cc5d-4c76-b4c4-80217c8665ed.mp3'
            }
            
            # Update the story document with new formats
            story_ref.update({
                'formats': formats,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            print("✅ Song successfully updated!")
            print(f"📝 New title: 'This Is My Story'")
            print(f"📄 Content length: {len(new_lyrics)} characters")
            print(f"📊 Word count: {len(new_lyrics.split())} words")
                
        else:
            print("❌ Story not found")
            
    except Exception as e:
        print(f"❌ Error updating song: {e}")

if __name__ == "__main__":
    update_marcus_song() 