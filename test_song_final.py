#!/usr/bin/env python3
"""
Test Final Song Prompt
======================

Tests the new improved song prompt with:
- Character count limit checking
- Chorus repetition detection  
- Label detection (should be none)
"""

import requests
import json
import re

def test_new_song_prompt():
    """Test the new viral song prompt"""
    
    print("🎵 Testing New Short Viral Song Prompt")
    print("=" * 50)
    
    # Marcus's story ID
    STORY_ID = "7UV1cWhMHbnVVNK4m5HB"
    BASE_URL = "http://127.0.0.1:8080"
    
    try:
        # Generate new song
        print(f"📖 Generating new song for story: {STORY_ID}")
        
        response = requests.post(
            f"{BASE_URL}/api/stories/{STORY_ID}/generate-format",
            json={"format_type": "song"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Song generated successfully!")
            
            # Get the generated song
            song_response = requests.get(f"{BASE_URL}/api/stories/{STORY_ID}/formats/song")
            
            if song_response.status_code == 200:
                song_data = song_response.json()
                song_text = song_data.get('content', '')
                
                print("\n🎵 GENERATED SONG:")
                print("-" * 40)
                print(song_text)
                print("-" * 40)
                
                # Analysis
                print(f"\n📊 SONG ANALYSIS:")
                print(f"• Character count: {len(song_text)}")
                print(f"• Word count: {len(song_text.split())}")
                print(f"• Line count: {len(song_text.split(chr(10)))}")
                
                # Check for forbidden labels
                labels_found = []
                forbidden_labels = ['Verse:', 'Chorus:', 'Bridge:', '[Verse', '[Chorus', '[Bridge']
                for label in forbidden_labels:
                    if label.lower() in song_text.lower():
                        labels_found.append(label)
                
                if labels_found:
                    print(f"❌ Found forbidden labels: {labels_found}")
                else:
                    print("✅ No forbidden labels found!")
                
                # Check for chorus repetition
                lines = [line.strip() for line in song_text.split('\n') if line.strip() and not line.startswith('TITLE')]
                unique_lines = set(lines)
                repeated_lines = []
                
                for line in unique_lines:
                    count = lines.count(line)
                    if count > 1:
                        repeated_lines.append((line, count))
                
                if repeated_lines:
                    print(f"✅ Found {len(repeated_lines)} repeated lines (chorus detection):")
                    for line, count in repeated_lines:
                        print(f"   '{line}' appears {count} times")
                else:
                    print("❌ No repeated lines found - missing chorus repetition")
                
                # Length check
                if len(song_text) <= 300:
                    print(f"✅ Song length good: {len(song_text)}/300 characters")
                else:
                    print(f"❌ Song too long: {len(song_text)}/300 characters")
                
                # Overall score
                score = 0
                if not labels_found: score += 25
                if repeated_lines: score += 25
                if len(song_text) <= 300: score += 25
                if len(song_text) > 50: score += 25  # Not too short either
                
                print(f"\n🎯 OVERALL SCORE: {score}/100")
                
                if score >= 75:
                    print("🎉 EXCELLENT! Song meets all requirements!")
                elif score >= 50:
                    print("👍 GOOD! Song meets most requirements")
                else:
                    print("⚠️  NEEDS WORK: Song doesn't meet requirements")
                
            else:
                print(f"❌ Failed to get song: {song_response.status_code}")
                
        else:
            print(f"❌ Failed to generate song: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_new_song_prompt() 