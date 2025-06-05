#!/usr/bin/env python3
"""
Test script for the Smart Story Engine

This script tests various conversation scenarios to ensure the smart story engine
correctly identifies when conversations should become stories vs continue as chats.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_story_engine import SmartStoryEngine

def test_conversation_scenarios():
    """Test different conversation scenarios"""
    
    # Initialize the smart story engine (without other engines for testing)
    engine = SmartStoryEngine()
    
    print("🧠 Testing Smart Story Engine")
    print("=" * 50)
    
    # Test scenarios
    scenarios = [
        {
            'name': 'Simple Question',
            'conversation': [
                {'role': 'user', 'content': 'How are you?'},
                {'role': 'assistant', 'content': 'I\'m doing well, thank you!'},
                {'role': 'user', 'content': 'What should I do today?'}
            ],
            'expected': 'continue_conversation'
        },
        {
            'name': 'Story-worthy Experience',
            'conversation': [
                {'role': 'user', 'content': 'I had this amazing realization yesterday when I was walking in the park.'},
                {'role': 'assistant', 'content': 'That sounds meaningful. Tell me more about it.'},
                {'role': 'user', 'content': 'I realized that I\'ve been so focused on pleasing others that I forgot what makes me happy. It was like a weight lifted off my shoulders. I felt this deep sense of relief and clarity about my relationships and what I really want in life.'}
            ],
            'expected': 'generate_story'
        },
        {
            'name': 'Moderate Potential',
            'conversation': [
                {'role': 'user', 'content': 'I\'ve been thinking about my job lately.'},
                {'role': 'assistant', 'content': 'What\'s been on your mind about it?'},
                {'role': 'user', 'content': 'I feel like I\'m not growing anymore. It\'s comfortable but I wonder if I should take more risks.'}
            ],
            'expected': 'guide_to_story'
        },
        {
            'name': 'Advice Seeking',
            'conversation': [
                {'role': 'user', 'content': 'I need help deciding something.'},
                {'role': 'assistant', 'content': 'I\'m here to help. What\'s the decision?'},
                {'role': 'user', 'content': 'Should I move to a new city for work? I\'m not sure what to do.'}
            ],
            'expected': 'continue_conversation'
        },
        {
            'name': 'Deep Personal Story',
            'conversation': [
                {'role': 'user', 'content': 'When I was younger, I used to be terrified of speaking up in groups.'},
                {'role': 'assistant', 'content': 'That must have been challenging. What was that like for you?'},
                {'role': 'user', 'content': 'It was really hard. I remember this one time in college when I had something important to say in a meeting, but I just sat there silent. I felt so frustrated with myself.'},
                {'role': 'assistant', 'content': 'That sounds like a difficult moment. How did you work through that fear?'},
                {'role': 'user', 'content': 'It took years, but I slowly learned that my voice matters. I started small - speaking up in smaller groups first. Now I can lead presentations confidently. That scared college student feels like a different person.'}
            ],
            'expected': 'generate_story'
        }
    ]
    
    # Test each scenario
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. Testing: {scenario['name']}")
        print("-" * 30)
        
        # Analyze the conversation
        analysis = engine.analyze_conversation_for_story_potential(
            scenario['conversation'], 
            user_id='test_user'
        )
        
        # Display results
        recommendation = analysis['recommendation']
        score = analysis['story_readiness_score']
        reasoning = analysis['reasoning']
        
        print(f"📊 Story Readiness Score: {score:.2f}")
        print(f"🎯 Recommendation: {recommendation}")
        print(f"💭 Reasoning: {reasoning}")
        
        # Check if it matches expected
        expected = scenario['expected']
        if recommendation == expected:
            print(f"✅ PASS - Expected: {expected}")
        else:
            print(f"❌ FAIL - Expected: {expected}, Got: {recommendation}")
        
        # Show story elements if any
        story_elements = analysis['story_elements']
        if story_elements and story_elements.get('total_indicators', 0) > 0:
            print(f"📖 Story Elements Found: {story_elements['total_indicators']}")
            for category, data in story_elements.items():
                if isinstance(data, dict) and data.get('count', 0) > 0:
                    print(f"   - {category}: {data['count']} indicators")
    
    print("\n" + "=" * 50)
    print("🎉 Smart Story Engine Testing Complete!")

def test_story_guidance():
    """Test conversation guidance generation"""
    
    engine = SmartStoryEngine()
    
    print("\n🗣️ Testing Conversation Guidance")
    print("=" * 50)
    
    # Test conversation that needs guidance
    conversation = [
        {'role': 'user', 'content': 'I\'ve been feeling stuck lately.'},
        {'role': 'assistant', 'content': 'I\'m sorry to hear that. Can you tell me more?'},
        {'role': 'user', 'content': 'I just feel like I\'m going through the motions every day.'}
    ]
    
    guidance = engine.get_conversation_guidance(conversation, 'test_user')
    
    if guidance:
        print(f"Strategy: {guidance.get('strategy', 'None')}")
        
        if guidance.get('suggested_responses'):
            print("Suggested Responses:")
            for response in guidance['suggested_responses']:
                print(f"  - {response}")
        
        if guidance.get('story_development_questions'):
            print("Story Development Questions:")
            for question in guidance['story_development_questions']:
                print(f"  - {question}")
    else:
        print("No guidance generated")

def test_story_worthy_response():
    """Test story-worthy response generation"""
    
    engine = SmartStoryEngine()
    
    print("\n💬 Testing Story-Worthy Response Generation")
    print("=" * 50)
    
    # Test different conversation types
    test_conversations = [
        {
            'name': 'Story Development',
            'conversation': [
                {'role': 'user', 'content': 'I had this moment yesterday where everything clicked.'},
                {'role': 'assistant', 'content': 'That sounds significant. What happened?'},
                {'role': 'user', 'content': 'I was talking to my friend and suddenly understood why I always feel anxious in social situations.'}
            ]
        },
        {
            'name': 'Advice Seeking',
            'conversation': [
                {'role': 'user', 'content': 'I need help with something.'},
                {'role': 'assistant', 'content': 'I\'m here to help. What\'s going on?'},
                {'role': 'user', 'content': 'I don\'t know how to handle conflict with my roommate.'}
            ]
        }
    ]
    
    for test in test_conversations:
        print(f"\n{test['name']}:")
        response = engine.generate_story_worthy_response(test['conversation'], 'test_user')
        print(f"Generated Response: {response}")

if __name__ == "__main__":
    test_conversation_scenarios()
    test_story_guidance()
    test_story_worthy_response() 