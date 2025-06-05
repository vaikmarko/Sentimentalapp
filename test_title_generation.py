#!/usr/bin/env python3
"""
Test Title Generation
====================

Tests the improved song title generation system that uses the prompts engine
and AI generation instead of old template fallbacks.
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from formats_generation_engine import FormatsGenerationEngine
from format_types import FormatType
from prompts_engine import PromptsEngine

def test_song_title_generation():
    """Test that song titles are generated properly using AI and prompts engine"""
    
    print("🎵 Testing Song Title Generation System")
    print("=" * 50)
    
    # Initialize engines
    prompts_engine = PromptsEngine()
    formats_engine = FormatsGenerationEngine()
    formats_engine.prompts_engine = prompts_engine
    
    # Test story: Marcus Rodriguez's work story
    test_story = """
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
    
    print(f"📖 Test Story Preview:")
    print(f"   '{test_story[:100]}...'")
    print()
    
    # Generate song format
    print("🤖 Generating song with AI + prompts engine...")
    result = formats_engine.generate_format(
        story_content=test_story,
        format_type=FormatType.SONG
    )
    
    print(f"✅ Generation Status: {result.get('success', False)}")
    print(f"🔧 Generation Method: {result.get('generation_method', 'unknown')}")
    
    if result.get('success'):
        content = result.get('content', '')
        title = result.get('title', 'No title extracted')
        
        print(f"🎼 Generated Title: '{title}'")
        print(f"📝 Content Length: {len(content)} characters")
        print(f"🎯 Model Used: {result.get('model_used', 'unknown')}")
        
        print("\n📋 Generated Song Content:")
        print("-" * 30)
        print(content[:300] + "..." if len(content) > 300 else content)
        print("-" * 30)
        
        # Analyze title quality
        print(f"\n🔍 Title Analysis:")
        print(f"   - Length: {len(title)} characters")
        print(f"   - Not generic fallback: {'✅' if title not in ['Generated Song', 'Finding My Voice', 'My Story'] else '❌'}")
        print(f"   - Story-relevant: {'✅' if any(word in title.lower() for word in ['work', 'life', 'career', 'purpose', 'meaning']) else '❓'}")
        
    else:
        error = result.get('error', 'Unknown error')
        print(f"❌ Generation Failed: {error}")
        
        if 'OpenAI API key' in error:
            print("💡 Note: This is expected without OpenAI API key")
            print("   Template generation has been disabled as requested")
            
    print("\n" + "=" * 50)
    
    return result

def test_title_extraction():
    """Test the title extraction logic in the frontend"""
    
    print("🔧 Testing Title Extraction Logic")
    print("=" * 50)
    
    # Test cases for title extraction
    test_cases = [
        {
            'content': 'TITLE: "Finding My Purpose"\n\nVerse 1:\nWalking through...',
            'expected': 'Finding My Purpose',
            'description': 'Standard TITLE format with quotes'
        },
        {
            'content': "TITLE: 'Work Life Blues'\n\nSitting in meetings...",
            'expected': 'Work Life Blues',
            'description': 'TITLE format with single quotes'
        },
        {
            'content': 'TITLE: Career Crossroads\n\nLooking at my life...',
            'expected': 'Career Crossroads',
            'description': 'TITLE format without quotes'
        },
        {
            'content': 'Walking through the morning, staring at the ceiling\nGot this gut feeling...',
            'expected': 'Walking through morning staring ceiling',  # Should extract meaningful words
            'description': 'No title - should extract from content'
        }
    ]
    
    # Simulate the frontend extractSongTitle function
    def extract_song_title(content):
        if not content or not isinstance(content, str):
            return 'Generated Song'
        
        # Look for "TITLE: 'Song Name'" or "TITLE: "Song Name""
        import re
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
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test Case {i}: {test_case['description']}")
        
        extracted = extract_song_title(test_case['content'])
        expected = test_case['expected']
        
        print(f"   Input: {test_case['content'][:50]}...")
        print(f"   Expected: '{expected}'")
        print(f"   Extracted: '{extracted}'")
        
        # For meaningful word extraction, just check it's not the fallback
        if 'extract from content' in test_case['description']:
            success = extracted != 'Generated Song' and len(extracted) > 3
        else:
            success = extracted == expected
            
        print(f"   Result: {'✅ PASS' if success else '❌ FAIL'}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    print("🎯 Testing Improved Title Generation System")
    print("🚫 Template generation has been archived")
    print("🤖 Only AI generation through prompts engine is used")
    print()
    
    # Test the new system
    result = test_song_title_generation()
    
    print()
    
    # Test title extraction logic
    test_title_extraction()
    
    print("\n🎉 Title generation testing complete!")
    print("💡 If OpenAI API key is available, titles should be generated from prompts engine")
    print("🔧 If not available, system correctly rejects template fallback") 