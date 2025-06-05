#!/usr/bin/env python3
"""
Debug Title Extraction
======================

Debug what the frontend is extracting to get "Walking through morning"
"""

import re

def debug_frontend_extraction(content):
    """Debug the exact extraction logic that produces 'Walking through morning'"""
    
    print("🔍 Debugging Frontend Title Extraction")
    print("=" * 50)
    print(f"📝 Content (first 200 chars): '{content[:200]}...'")
    print()
    
    if not content or not isinstance(content, str):
        print("❌ Content is empty or not string")
        return 'Generated Song'
    
    # Look for "TITLE: 'Song Name'" or "TITLE: "Song Name""
    title_match = re.search(r'TITLE:\s*[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
    if title_match:
        result = title_match.group(1)
        print(f"✅ Found quoted title: '{result}'")
        return result
    else:
        print("❌ No quoted TITLE: format found")
    
    # Look for title without quotes: "TITLE: Song Name"
    title_match2 = re.search(r'TITLE:\s*([^\n]+)', content, re.IGNORECASE)
    if title_match2:
        result = title_match2.group(1).strip()
        print(f"✅ Found unquoted title: '{result}'")
        return result
    else:
        print("❌ No unquoted TITLE: format found")
    
    print("⚠️  No TITLE: format found, falling back to content analysis...")
    
    # Check if content starts with a potential title (short line, not lyrics)
    lines = content.split('\n')
    first_line = lines[0].strip() if lines else ''
    print(f"📄 First line: '{first_line}'")
    
    if first_line and len(first_line) < 50 and not first_line.lower().startswith(('verse', 'chorus', 'bridge')):
        # Check if it looks like a title (not obviously lyrics)
        if not re.search(r'\b(through|walking|feeling|looking|going|coming|talking|singing)\b.*\b(the|my|your|his|her)\b', first_line.lower()):
            print(f"🎯 First line could be title: '{first_line}'")
            return first_line
        else:
            print(f"❌ First line looks like lyrics: '{first_line}'")
    
    # Extract meaningful words from content
    words = re.sub(r'[^\w\s]', ' ', content).split()
    print(f"📝 First 15 words: {words[:15]}")
    
    meaningful_words = [word for word in words[:10] 
                      if len(word) > 3 and word.lower() not in 
                      ['this', 'that', 'with', 'from', 'they', 'them', 'were', 'have', 'been', 'will', 'would', 'could', 'should', 'walking', 'through', 'morning']]
    
    print(f"🎯 Meaningful words (after filtering): {meaningful_words}")
    
    if len(meaningful_words) >= 2:
        result = ' '.join(meaningful_words[:3])
        print(f"📤 Would extract from meaningful words: '{result}'")
        return result
    
    # If that doesn't work, try first few words
    if len(words) >= 3:
        result = ' '.join(words[:3])
        print(f"📤 Would extract from first words: '{result}'")
        return result
    
    print("🔄 Fallback to 'Generated Song'")
    return 'Generated Song'

def simulate_frontend_extraction():
    """Simulate exactly what frontend might be doing"""
    
    # Marcus's actual song content
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
This is my moment, this is my choice"""
    
    print("🎵 Marcus's Song Content Analysis")
    print("=" * 50)
    
    extracted = debug_frontend_extraction(marcus_song_content)
    
    print()
    print("=" * 50)
    print(f"🎯 Final extraction result: '{extracted}'")
    print(f"🖥️  Frontend shows: 'Walking through morning'")
    print()
    
    # Try to figure out where "Walking through morning" comes from
    print("🕵️ Investigating 'Walking through morning'...")
    
    # Check if it's from first few words
    words = marcus_song_content.split()
    print(f"First 3 words: '{' '.join(words[:3])}'")
    print(f"First 4 words: '{' '.join(words[:4])}'")
    
    # Check if it's some substring
    first_line = marcus_song_content.split('\n')[0]
    print(f"First line: '{first_line}'")
    
    # Check for different word combinations
    if 'walking through the morning' in marcus_song_content.lower():
        print("✅ 'Walking through the morning' found in content")
    
    # Maybe it's truncating?
    if first_line.lower().startswith('walking through the morning'):
        truncated = 'Walking through morning'
        print(f"🎯 Might be truncating: '{truncated}'")

if __name__ == "__main__":
    simulate_frontend_extraction() 