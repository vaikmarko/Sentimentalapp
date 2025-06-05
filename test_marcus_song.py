#!/usr/bin/env python3
"""
Test Marcus Story Song Generation
================================

Quick test to generate a song for Marcus's story and see the title.
"""

import os
import sys
import requests
import json

def test_marcus_song_generation():
    """Test song generation for Marcus's story via the API"""
    
    print("🎵 Testing Song Generation for Marcus's Story")
    print("=" * 50)
    
    # Marcus's story content
    marcus_story = """
    I realized today that I've been living my life on autopilot for way too long. 
    Sitting in another pointless meeting, watching people argue about metrics that 
    don't really matter, I had this moment where I thought: "What the hell am I doing here?"
    
    It's not that the job is terrible or my colleagues are bad people. It's just that 
    none of it feels... meaningful? Like, I could disappear tomorrow and the machine 
    would keep running exactly the same. That's a weird feeling when you're 29 and 
    supposed to be "building your career."
    
    I keep thinking about what I actually want to do with my life. Not what I'm 
    supposed to want, not what would make my parents proud, not what would look 
    good on LinkedIn. What would actually make me excited to wake up in the morning?
    
    Maybe it's time to stop pretending I have it all figured out and start 
    actually figuring it out.
    """
    
    # First, create a test story
    print("📝 Creating test story...")
    story_data = {
        'title': 'Life on Autopilot',
        'content': marcus_story.strip(),
        'author': 'Marcus Rodriguez',
        'public': True
    }
    
    try:
        # Add story
        response = requests.post('http://localhost:8080/api/stories', 
                               json=story_data, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 201:
            story = response.json()
            story_id = story['id']
            print(f"✅ Story created with ID: {story_id}")
            
            # Generate song format
            print("🎵 Generating song format...")
            format_response = requests.post(
                f'http://localhost:8080/api/stories/{story_id}/generate-format',
                json={'format_type': 'song'},
                headers={'Content-Type': 'application/json'}
            )
            
            if format_response.status_code == 200:
                result = format_response.json()
                print("✅ Song generation successful!")
                
                # Print results
                print(f"🔧 Generation method: {result.get('generation_method', 'unknown')}")
                if result.get('title'):
                    print(f"🎼 Generated title: '{result['title']}'")
                else:
                    print("❌ No title in response")
                
                content = result.get('content', '')
                print(f"📝 Content length: {len(content)} characters")
                
                if content:
                    print("\n📋 Song content preview:")
                    print("-" * 40)
                    # Show first 200 characters
                    preview = content[:200] + "..." if len(content) > 200 else content
                    print(preview)
                    print("-" * 40)
                    
                    # Check if it starts with TITLE:
                    if content.startswith('TITLE:'):
                        print("✅ Content starts with TITLE: format")
                        lines = content.split('\n')
                        title_line = lines[0] if lines else ''
                        print(f"🏷️  Title line: '{title_line}'")
                    else:
                        print("⚠️  Content doesn't start with TITLE: format")
                        
                    # Test frontend title extraction
                    print("\n🔧 Testing frontend title extraction...")
                    extracted_title = extract_song_title_frontend(content)
                    print(f"📤 Frontend would extract: '{extracted_title}'")
                    
                else:
                    print("❌ No content generated")
                    
            else:
                print(f"❌ Song generation failed: {format_response.status_code}")
                print(f"   Response: {format_response.text}")
                
        else:
            print(f"❌ Failed to create story: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.ConnectionError:
        print("❌ Could not connect to server. Is it running on localhost:8080?")
    except Exception as e:
        print(f"❌ Error: {e}")

def extract_song_title_frontend(content):
    """Simulate the frontend title extraction logic"""
    import re
    
    if not content or not isinstance(content, str):
        return 'Generated Song'
    
    # Look for "TITLE: 'Song Name'" or "TITLE: "Song Name""
    title_match = re.search(r'TITLE:\s*[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
    if title_match:
        return title_match.group(1)
    
    # Look for title without quotes: "TITLE: Song Name"
    title_match2 = re.search(r'TITLE:\s*([^\n]+)', content, re.IGNORECASE)
    if title_match2:
        return title_match2.group(1).strip()
    
    # Extract meaningful words from content
    words = re.sub(r'[^\w\s]', ' ', content).split()
    meaningful_words = [word for word in words[:10] 
                      if len(word) > 3 and word.lower() not in 
                      ['this', 'that', 'with', 'from', 'they', 'them', 'were', 'have', 'been', 'will', 'would', 'could', 'should', 'walking', 'through', 'morning']]
    
    if len(meaningful_words) >= 2:
        return ' '.join(meaningful_words[:3])
    
    return 'Generated Song'

if __name__ == "__main__":
    print("🎯 Testing Marcus's Story Song Generation")
    print("🚫 Template generation has been archived")
    print("🤖 Only AI generation through prompts engine is used")
    print()
    
    test_marcus_song_generation()
    
    print("\n🎉 Test complete!")
    print("💡 Check the logs above to see how titles are generated and extracted") 