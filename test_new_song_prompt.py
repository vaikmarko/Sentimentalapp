#!/usr/bin/env python3
"""
Test New Viral Song Prompt
=========================

Tests the new improved song prompt to see if it generates better,
more engaging, viral-worthy songs from Marcus's story.
"""

import sys
import os
import requests
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prompts_engine import PromptsEngine, PromptType
from format_types import FormatType

def test_new_song_prompt():
    """Test the new viral song prompt"""
    
    print("🎵 Testing New Viral Song Prompt")
    print("=" * 50)
    
    # Marcus's story ID
    STORY_ID = "7UV1cWhMHbnVVNK4m5HB"
    BASE_URL = "http://127.0.0.1:8080"
    
    print(f"📖 Testing with Marcus's story: {STORY_ID}")
    
    try:
        # Generate new song with the improved prompt
        print("\n🚀 Generating new song...")
        
        response = requests.post(f"{BASE_URL}/api/stories/{STORY_ID}/generate-format", 
                               json={'format_type': 'song'},
                               timeout=30)
        
        if response.status_code == 200:
            print("✅ Song generation successful!")
            
            # Get the generated song
            get_response = requests.get(f"{BASE_URL}/api/stories/{STORY_ID}/formats/song")
            
            if get_response.status_code == 200:
                song_data = get_response.json()
                content = song_data.get('content', '')
                title = song_data.get('title', 'No title')
                
                print(f"\n🎼 Generated Song:")
                print("=" * 40)
                print(f"Title: {title}")
                print()
                print(content)
                print("=" * 40)
                
                # Analyze the new song
                print(f"\n📊 Song Analysis:")
                print(f"   Length: {len(content)} characters")
                print(f"   Title quality: {'✅' if title != 'Default Title' and len(title) > 5 else '❌'}")
                
                # Check for proper structure
                lines = content.split('\n')
                non_empty_lines = [line.strip() for line in lines if line.strip()]
                
                print(f"   Total lines: {len(non_empty_lines)}")
                
                # Look for chorus repetition
                line_counts = {}
                for line in non_empty_lines:
                    if len(line) > 10:  # Only count substantial lines
                        line_counts[line] = line_counts.get(line, 0) + 1
                
                repeated_lines = {line: count for line, count in line_counts.items() if count > 1}
                
                if repeated_lines:
                    print("   ✅ Has repeating chorus sections:")
                    for line, count in repeated_lines.items():
                        print(f"      '{line[:50]}...' (repeated {count} times)")
                else:
                    print("   ❌ No repeating chorus found")
                
                # Check for engaging language
                viral_words = ['ready', 'done', 'time', 'moment', 'rise', 'fight', 'shine', 'break', 'free', 'alive']
                found_viral_words = [word for word in viral_words if word.lower() in content.lower()]
                
                if found_viral_words:
                    print(f"   ✅ Contains viral language: {', '.join(found_viral_words)}")
                else:
                    print("   ❓ Limited viral language found")
                
                # Check for emotional hooks
                emotional_phrases = ['this is my', "i'm done", "i won't", "ready to", "time to"]
                found_hooks = [phrase for phrase in emotional_phrases if phrase in content.lower()]
                
                if found_hooks:
                    print(f"   ✅ Contains emotional hooks: {', '.join(found_hooks)}")
                else:
                    print("   ❓ Limited emotional hooks found")
                
                print(f"\n🎯 Overall Assessment:")
                
                score = 0
                if len(content) >= 400:
                    score += 20
                    print("   ✅ Good length for radio/streaming")
                else:
                    print("   ⚠️  Might be too short")
                    
                if repeated_lines:
                    score += 30
                    print("   ✅ Has proper chorus structure")
                else:
                    print("   ❌ Missing chorus repetition")
                    
                if found_viral_words:
                    score += 25
                    print("   ✅ Uses engaging language")
                    
                if found_hooks:
                    score += 25
                    print("   ✅ Has emotional hooks")
                
                print(f"\n   📈 Viral Potential Score: {score}/100")
                
                if score >= 75:
                    print("   🎉 EXCELLENT - This song has strong viral potential!")
                elif score >= 50:
                    print("   👍 GOOD - Solid song with room for improvement")
                elif score >= 25:
                    print("   ⚠️  OKAY - Needs work to become viral")
                else:
                    print("   ❌ POOR - Significant improvements needed")
                
            else:
                print(f"❌ Failed to retrieve song: {get_response.status_code}")
                
        else:
            print(f"❌ Song generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_prompt_directly():
    """Test the prompt generation directly"""
    
    print("\n" + "=" * 50)
    print("🔧 Testing Prompt Generation Directly")
    print("=" * 50)
    
    # Initialize prompts engine
    prompts_engine = PromptsEngine()
    
    # Marcus's story content
    story_content = """Every morning, I wake up with a familiar feeling in the pit of my stomach. It's a nagging sensation that I can't seem to shake off. As I stare at the ceiling, I can't help but think, "I need to quit my job." It's a scary thought, like stepping off the edge of a cliff into the unknown. But as the days go by, this feeling only grows stronger, and I know I can't ignore it any longer."""
    
    try:
        # Get the prompt
        prompt = prompts_engine.get_prompt(
            PromptType.FORMAT_GENERATION,
            format_type=FormatType.SONG,
            content=story_content
        )
        
        print("✅ Prompt generated successfully!")
        print(f"\n📝 Prompt Preview (first 500 chars):")
        print("-" * 30)
        print(prompt[:500] + "...")
        print("-" * 30)
        
        # Check for key viral elements in prompt
        viral_elements = ['viral', 'emotional', 'chorus', 'singalong', 'hook']
        found_elements = [element for element in viral_elements if element.lower() in prompt.lower()]
        
        print(f"\n🎯 Viral Elements in Prompt: {', '.join(found_elements)}")
        
        if len(found_elements) >= 3:
            print("✅ Prompt contains strong viral guidance")
        else:
            print("⚠️  Prompt may need more viral elements")
            
        print(f"\n📏 Total prompt length: {len(prompt)} characters")
        
    except Exception as e:
        print(f"❌ Error generating prompt: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_new_song_prompt()
    test_prompt_directly() 