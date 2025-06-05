#!/usr/bin/env python3

import os
import openai
from prompts_engine import PromptsEngine, PromptType
from format_types import FormatType

def test_openai_direct():
    """Test OpenAI API directly with the exact prompt"""
    
    print("🤖 Testing OpenAI API Direct Response")
    print("=" * 50)
    
    # Check if OpenAI is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No OpenAI API key - cannot test")
        return
    
    # Set up OpenAI client (legacy format)
    openai.api_key = api_key
    
    # Initialize prompts engine and get the exact prompt
    prompts_engine = PromptsEngine()
    
    story_content = """Every morning, I wake up with a familiar feeling in the pit of my stomach. It's a nagging sensation that I can't seem to shake off. As I stare at the ceiling, I can't help but think, "I need to quit my job." It's a scary thought, like stepping off the edge of a cliff into the unknown. But as the days go by, this feeling only grows stronger, and I know I can't ignore it any longer."""
    
    prompt = prompts_engine.get_prompt(
        PromptType.FORMAT_GENERATION,
        format_type=FormatType.SONG,
        content=story_content
    )
    
    print(f"📝 Using prompt length: {len(prompt)} characters")
    print("🎯 Key instruction: 'Output pure lyrics after the title - no labels like [Verse] or [Chorus]'")
    
    try:
        # Make the exact same API call as formats engine
        print("\n🔄 Calling OpenAI API...")
        completion = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7,
            stop=None
        )
        
        generated_content = completion.choices[0].text.strip()
        
        print("✅ API call successful!")
        print(f"\n🎵 GENERATED CONTENT:")
        print("-" * 40)
        print(generated_content)
        print("-" * 40)
        
        # Analyze the response
        print("\n📊 ANALYSIS:")
        
        # Check for labels
        if '[Verse' in generated_content or 'Verse:' in generated_content:
            print("❌ PROBLEM: Contains verse labels - AI is not following instructions!")
            labels_found = []
            if '[Verse' in generated_content:
                labels_found.append('[Verse]')
            if 'Verse:' in generated_content:
                labels_found.append('Verse:')
            if '[Chorus' in generated_content:
                labels_found.append('[Chorus]')
            if 'Chorus:' in generated_content:
                labels_found.append('Chorus:')
            print(f"   Labels found: {', '.join(labels_found)}")
        else:
            print("✅ Good: No verse/chorus labels found")
            
        # Check for title
        if 'TITLE:' in generated_content:
            print("✅ Good: Includes title format")
            # Extract title
            lines = generated_content.split('\n')
            title_line = next((line for line in lines if 'TITLE:' in line), None)
            if title_line:
                print(f"   Title: {title_line}")
        else:
            print("❌ Missing title format")
            
        # Check length
        print(f"📏 Content length: {len(generated_content)} characters")
        
        # Check if it looks viral/high quality
        if 'viral' in generated_content.lower() or len(generated_content) > 500:
            print("✅ Appears to be substantial content")
        else:
            print("⚠️  Content seems short for viral song")
            
    except Exception as e:
        print(f"❌ API call failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_openai_direct() 