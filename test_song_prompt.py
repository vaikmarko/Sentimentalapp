#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prompts_engine import PromptsEngine, PromptType
from format_types import FormatType

def test_song_prompt():
    """Test the exact song prompt being generated"""
    
    print("🎵 Testing Song Prompt Generation")
    print("=" * 50)
    
    # Initialize prompts engine
    prompts_engine = PromptsEngine()
    
    # Test story content (Marcus story excerpt)
    story_content = """Every morning, I wake up with a familiar feeling in the pit of my stomach. It's a nagging sensation that I can't seem to shake off. As I stare at the ceiling, I can't help but think, "I need to quit my job." It's a scary thought, like stepping off the edge of a cliff into the unknown. But as the days go by, this feeling only grows stronger, and I know I can't ignore it any longer."""
    
    # Get the exact prompt that formats engine would use
    try:
        prompt = prompts_engine.get_prompt(
            PromptType.FORMAT_GENERATION,
            format_type=FormatType.SONG,
            content=story_content
        )
        
        print("✅ Successfully generated prompt!")
        print("\n📝 FULL PROMPT:")
        print("-" * 40)
        print(prompt)
        print("-" * 40)
        
        # Check key elements
        if "viral" in prompt.lower():
            print("✅ Contains 'viral' requirement")
        else:
            print("❌ Missing 'viral' requirement")
            
        if "no labels like [Verse] or [Chorus]" in prompt:
            print("✅ Explicitly says no verse/chorus labels")
        else:
            print("❌ Missing instruction to avoid labels")
            
        if "TITLE:" in prompt:
            print("✅ Includes title format instruction")
        else:
            print("❌ Missing title format instruction")
            
        if "7500 characters" in prompt:
            print("✅ Includes Suno AI character limit")
        else:
            print("❌ Missing character limit info")
            
        print(f"\n📊 Prompt length: {len(prompt)} characters")
        
    except Exception as e:
        print(f"❌ Error generating prompt: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_song_prompt() 