#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from formats_generation_engine import FormatsGenerationEngine, FormatType
from prompts_engine import PromptsEngine, PromptType

def test_generation_flow():
    """Debug the song generation flow step by step"""
    
    print("🔍 Testing Song Generation Flow")
    print("=" * 50)
    
    # Test story data (Marcus story)
    story_data = {
        'content': """Every morning, I wake up with a familiar feeling in the pit of my stomach. It's a nagging sensation that I can't seem to shake off. As I stare at the ceiling, I can't help but think, "I need to quit my job." It's a scary thought, like stepping off the edge of a cliff into the unknown. But as the days go by, this feeling only grows stronger, and I know I can't ignore it any longer.

I chose to pursue a career in marketing because I believed it would allow me to tap into my creativity and innovation. However, as I immersed myself in the industry, I quickly realized that my job was not about creating meaningful connections or making a positive impact. It was simply about manipulating people into buying things they don't need. I felt like a puppet master, pulling strings and making people dance to my tune."""
    }
    
    # Initialize engines
    prompts_engine = PromptsEngine()
    formats_engine = FormatsGenerationEngine(prompts_engine)
    
    print("1️⃣ Testing Prompts Engine directly:")
    try:
        prompt_result = prompts_engine.generate_song_prompt(story_data['content'])
        print(f"   Prompts engine result: {prompt_result[:200]}...")
        
        if '[Verse' in prompt_result or 'Verse:' in prompt_result:
            print("   ❌ Prompts engine producing verse labels!")
        else:
            print("   ✅ Prompts engine producing clean content")
            
    except Exception as e:
        print(f"   ❌ Prompts engine error: {e}")
    
    print("\n2️⃣ Testing Formats Engine:")
    try:
        format_result = formats_engine.generate_format(story_data, FormatType.SONG)
        print(f"   Format result success: {format_result.get('success', False)}")
        print(f"   Content preview: {format_result.get('content', 'No content')[:200]}...")
        
        content = format_result.get('content', '')
        if '[Verse' in content or 'Verse:' in content:
            print("   ❌ Formats engine producing verse labels!")
        else:
            print("   ✅ Formats engine producing clean content")
            
        # Check title extraction
        if 'TITLE:' in content:
            print("   ✅ Found TITLE: prefix in content")
        else:
            print("   ❌ No TITLE: prefix found")
            
    except Exception as e:
        print(f"   ❌ Formats engine error: {e}")
    
    print("\n3️⃣ Checking which prompts are being used:")
    try:
        # Check if prompts engine has the right song prompt
        song_prompt = prompts_engine.get_prompt(PromptType.SONG)
        print(f"   Song prompt preview: {song_prompt[:200]}...")
        
        if 'viral' in song_prompt.lower() and 'chorus:' not in song_prompt.lower():
            print("   ✅ Using high-quality viral prompt")
        else:
            print("   ❌ Using old basic prompt")
            
    except Exception as e:
        print(f"   ❌ Error checking prompts: {e}")

if __name__ == "__main__":
    test_generation_flow() 