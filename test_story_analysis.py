#!/usr/bin/env python3
"""Test story analysis directly to debug the scoring issue"""

import sys
sys.path.append('.')

from smart_story_engine import SmartStoryEngine
import openai
import os

def test_story_analysis():
    print("🧪 TESTING STORY ANALYSIS DIRECTLY")
    print("=" * 50)
    
    # Initialize the engine
    engine = SmartStoryEngine()
    
    # Test conversation that should score high
    test_conversation = [
        {"role": "user", "content": "I start my first 'real' job tomorrow and I'm literally shaking"},
        {"role": "assistant", "content": "That's such a big moment! What's going through your mind right now?"},
        {"role": "user", "content": "Everyone there has years of experience and I barely graduated 3 months ago"},
        {"role": "assistant", "content": "It sounds like you're worried about fitting in. What drew you to this job in the first place?"},
        {"role": "user", "content": "I applied thinking I'd never get it, like it was practice... and somehow they said yes?"},
        {"role": "assistant", "content": "Wait, so they chose YOU out of all their candidates. What does that tell you?"},
        {"role": "user", "content": "I keep thinking they made a mistake or I lied on my resume somehow"},
        {"role": "assistant", "content": "That feeling has a name - imposter syndrome. But here's the thing..."},
        {"role": "user", "content": "My mom keeps saying 'fake it till you make it' but I'm tired of feeling fake"},
        {"role": "assistant", "content": "What if instead of faking confidence, you embraced being new? What would that look like?"},
        {"role": "user", "content": "Maybe... asking questions instead of pretending I know everything?"},
        {"role": "assistant", "content": "Exactly. Your questions might be exactly what they need to hear."}
    ]
    
    print("📝 Testing with job anxiety conversation...")
    print(f"   Messages: {len(test_conversation)}")
    
    # Test the analysis
    try:
        result = engine.analyze_conversation_for_story_potential(test_conversation, "test_user_123")
        
        print(f"\n📊 ANALYSIS RESULTS:")
        print(f"   Score: {result.get('story_readiness_score', 'N/A')}")
        print(f"   Recommendation: {result.get('recommendation', 'N/A')}")
        print(f"   Reasoning: {result.get('reasoning', 'N/A')}")
        print(f"   Has potential: {result.get('has_story_potential', 'N/A')}")
        print(f"   Method: {result.get('analysis_details', {}).get('analysis_method', 'N/A')}")
        
        # Show story elements if available
        story_elements = result.get('story_elements', {})
        if story_elements:
            print(f"\n🎭 STORY ELEMENTS:")
            for key, value in story_elements.items():
                print(f"   {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

def test_openai_directly():
    print("\n🔗 TESTING OPENAI CONNECTION DIRECTLY")
    print("=" * 50)
    
    # Check if OpenAI key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return
    
    print(f"✅ OpenAI API key found: {api_key[:10]}...")
    
    try:
        # Test a simple OpenAI call
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello' and nothing else."}
            ],
            max_tokens=10
        )
        
        print(f"✅ OpenAI response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ OpenAI error: {e}")

if __name__ == "__main__":
    test_openai_directly()
    test_story_analysis() 