#!/usr/bin/env python3
"""Test updated prompts directly on existing conversation data"""

import sys
sys.path.append('.')

import openai
import os
from prompts_engine import PromptsEngine, PromptType
from datetime import datetime

# Set up OpenAI if available
openai.api_key = os.getenv('OPENAI_API_KEY')

def test_story_generation_direct():
    print("🎯 TESTING UPDATED PROMPTS ON EXISTING CONVERSATIONS")
    print("=" * 60)
    
    # Initialize the prompts engine
    prompts_engine = PromptsEngine()
    
    # Sample conversation data (from our previous successful creations)
    test_conversations = [
        {
            "name": "Alex - Job Anxiety",
            "conversation_text": """User: I start my first 'real' job tomorrow and I'm literally shaking
User: Everyone there has years of experience and I barely graduated 3 months ago
User: I applied thinking I'd never get it, like it was practice... and somehow they said yes?
User: I keep thinking they made a mistake or I lied on my resume somehow
User: My mom keeps saying 'fake it till you make it' but I'm tired of feeling fake
User: Maybe... asking questions instead of pretending I know everything?""",
            "themes": ["career", "imposter_syndrome", "new_beginning", "anxiety"],
            "emotional_markers": ["nervous", "uncertain", "hopeful"]
        },
        
        {
            "name": "Jordan - Social Media",
            "conversation_text": """User: I deleted Instagram today and I feel like I'm having withdrawals
User: I spent 3 hours last night scrolling through everyone's perfect lives
User: Honestly? Proof that I'm not the only one struggling to figure life out
User: Engagement photos, dream jobs, perfect bodies, 'living my best life' captions
User: Like I'm failing at being 23. Like everyone got a manual I never received
User: I just want to be real but 'real' doesn't get likes, you know?
User: Messy hair, failed attempts, small victories... actual human moments""",
            "themes": ["social_media", "authenticity", "comparison", "self_worth"],
            "emotional_markers": ["frustrated", "insecure", "seeking_authenticity"]
        }
    ]
    
    print(f"📚 Testing {len(test_conversations)} conversations")
    
    for i, conv_data in enumerate(test_conversations, 1):
        print(f"\n{'='*40}")
        print(f"🧪 TEST {i}: {conv_data['name']}")
        print(f"{'='*40}")
        
        # Mock context data
        user_context = {
            "primary_themes": conv_data["themes"][:2],
            "emotional_expression_style": "conversational",
            "engagement_level": "high"
        }
        
        domain_insights = {
            "themes": conv_data["themes"],
            "emotional_markers": conv_data["emotional_markers"],
            "domains": {"personal_growth": 0.8, "career": 0.6},
            "confidence": 0.75
        }
        
        conversation_flow = [{"role": "user", "content": line.replace("User: ", "")} 
                           for line in conv_data["conversation_text"].split("\n")]
        
        # Test the NEW updated prompts
        print(f"\n📝 GENERATING STORY WITH UPDATED NATURAL PROMPTS...")
        
        try:
            # Get the updated story creation prompt
            story_prompt = prompts_engine.get_prompt(
                PromptType.STORY_CREATION,
                conversation=conv_data["conversation_text"],
                user_context=user_context,
                domain_insights=domain_insights,
                conversation_flow=conversation_flow
            )
            
            if openai.api_key:
                print("   🤖 Using OpenAI GPT-4...")
                
                # Generate story with updated prompt
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You create authentic, relatable personal stories that sound like real people wrote them about their own experiences. Use natural, conversational language - never poetic or overly sophisticated."
                        },
                        {"role": "user", "content": story_prompt}
                    ],
                    max_tokens=600,
                    temperature=0.7
                )
                
                generated_story = response.choices[0].message.content.strip()
                
                # Generate title with updated prompt
                title_prompt = f"""Create a natural, authentic title for this personal story. Make it sound like something a real person (age 16-30) would actually write about their own experience.

Story excerpt: {generated_story[:200]}...

Key themes: {', '.join(conv_data['themes'][:2])}

Create a title that feels personal and real - NOT poetic or literary. Examples:
- "Starting My First Real Job"
- "Why I Deleted Social Media"
- "Learning to Ask for Help"
- "My Anxiety About Looking Stupid"

Make it conversational and authentic. Generate just the title:"""

                title_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": title_prompt}],
                    max_tokens=30,
                    temperature=0.8
                )
                
                generated_title = title_response.choices[0].message.content.strip().strip('"').strip("'")
                
            else:
                print("   ⚠️  No OpenAI key - using simplified analysis")
                generated_story = f"I've been thinking about {conv_data['themes'][0]} lately, and it's making me realize some things about myself..."
                generated_title = f"Learning About {conv_data['themes'][0].title()}"
            
            # Display results
            print(f"\n📖 GENERATED TITLE: '{generated_title}'")
            print(f"\n📄 GENERATED STORY:")
            print("-" * 50)
            print(generated_story)
            print("-" * 50)
            
            # Analyze the language quality
            print(f"\n🔍 LANGUAGE ANALYSIS:")
            
            # Title analysis
            poetic_title_words = ['whisper', 'shadow', 'dance', 'thread', 'solace', 'embrace', 'ethereal', 'profound']
            title_natural = not any(word in generated_title.lower() for word in poetic_title_words)
            print(f"   📋 Title Style: {'✅ Natural' if title_natural else '❌ Too poetic'}")
            
            # Story analysis
            first_person = generated_story.count(' I ') >= 3
            print(f"   👤 First Person: {'✅ Yes' if first_person else '❌ No'}")
            
            conversational_phrases = ['i realized', 'i started', 'i learned', 'looking back', 'the thing is', 'i guess', 'i never thought', 'it\'s funny']
            conversational = any(phrase in generated_story.lower() for phrase in conversational_phrases)
            print(f"   💬 Conversational: {'✅ Yes' if conversational else '❌ No'}")
            
            fancy_words = ['profound', 'ethereal', 'whisper', 'embrace', 'unfolds', 'tapestry', 'essence', 'profound', 'illuminated']
            natural_language = not any(word in generated_story.lower() for word in fancy_words)
            print(f"   🗣️  Natural Language: {'✅ Yes' if natural_language else '❌ Too fancy'}")
            
            # Word count
            word_count = len(generated_story.split())
            print(f"   📊 Word Count: {word_count} ({'✅ Good' if 250 <= word_count <= 500 else '⚠️ Check length'})")
            
            # Overall score
            scores = [title_natural, first_person, conversational, natural_language]
            overall_score = sum(scores) / len(scores)
            print(f"   🏆 Overall Authenticity: {overall_score:.1%} ({'✅ Great' if overall_score >= 0.75 else '⚠️ Needs work' if overall_score >= 0.5 else '❌ Too formal'})")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    print(f"\n🎉 TESTING COMPLETE!")
    print("\nKey improvements in updated prompts:")
    print("• Asks for 'authentic and relatable' instead of 'sophisticated'")
    print("• Emphasizes 'natural language' over 'poetic'")
    print("• Instructs to 'mirror their energy' and voice")
    print("• Uses first-person perspective")
    print("• Focuses on being 'grounded and real'")
    print("• Provides conversational example phrases")

if __name__ == "__main__":
    test_story_generation_direct() 