#!/usr/bin/env python3
"""
Analyze Marcus's Song Title Extraction
=====================================

Analyzes how the frontend title extraction works on Marcus's current song.
"""

import re

def extract_song_title_frontend(content):
    """Simulate the frontend title extraction logic"""
    
    if not content or not isinstance(content, str):
        return 'Generated Song'
    
    print(f"🔍 Analyzing content (first 100 chars): '{content[:100]}...'")
    
    # Look for "TITLE: 'Song Name'" or "TITLE: "Song Name""
    title_match = re.search(r'TITLE:\s*[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
    if title_match:
        result = title_match.group(1)
        print(f"✅ Found quoted title: '{result}'")
        return result
    
    # Look for title without quotes: "TITLE: Song Name"
    title_match2 = re.search(r'TITLE:\s*([^\n]+)', content, re.IGNORECASE)
    if title_match2:
        result = title_match2.group(1).strip()
        print(f"✅ Found unquoted title: '{result}'")
        return result
    
    print("❌ No TITLE: format found, extracting from content...")
    
    # Extract meaningful words from content
    words = re.sub(r'[^\w\s]', ' ', content).split()
    print(f"📝 First 15 words: {words[:15]}")
    
    meaningful_words = [word for word in words[:10] 
                      if len(word) > 3 and word.lower() not in 
                      ['this', 'that', 'with', 'from', 'they', 'them', 'were', 'have', 'been', 'will', 'would', 'could', 'should', 'walking', 'through', 'morning']]
    
    print(f"🎯 Meaningful words: {meaningful_words}")
    
    if len(meaningful_words) >= 2:
        result = ' '.join(meaningful_words[:3])
        print(f"📤 Extracted title: '{result}'")
        return result
    
    print("🔄 Fallback to 'Generated Song'")
    return 'Generated Song'

def analyze_marcus_song():
    """Analyze Marcus's current song content"""
    
    print("🎵 Analyzing Marcus's Song Title Extraction")
    print("=" * 50)
    
    # Marcus's actual song content from the database
    marcus_song_content = """Walking through the morning, staring at the ceiling
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
    
    print(f"📊 Current stored title: 'Man'")
    print(f"📝 Content starts with: '{marcus_song_content[:50]}...'")
    print(f"📏 Content length: {len(marcus_song_content)} characters")
    print()
    
    # Test frontend extraction
    extracted_title = extract_song_title_frontend(marcus_song_content)
    
    print()
    print("=" * 50)
    print(f"📤 Frontend extraction result: '{extracted_title}'")
    print(f"🗃️  Current database title: 'Man'")
    
    # Suggest better titles from the content
    print()
    print("💡 Suggested better titles from lyrics:")
    suggestions = [
        "This Is My Story",
        "Finding My Voice", 
        "Breaking the Chains",
        "Setting My Spirit Free",
        "My New Beginning"
    ]
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"   {i}. '{suggestion}'")
    
    print()
    print("🔧 Issues identified:")
    print("   • Song content doesn't use TITLE: format")
    print("   • Current title 'Man' comes from old template system")
    print("   • Frontend extraction falls back to content analysis")
    print("   • AI generation would produce better titles with TITLE: format")

if __name__ == "__main__":
    analyze_marcus_song() 