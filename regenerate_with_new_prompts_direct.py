#!/usr/bin/env python3
"""Directly regenerate stories from existing conversations with new prompts"""

import sys
sys.path.append('.')

import requests
import json
from app import generate_intelligent_story, generate_intelligent_title, create_story_from_conversation
from knowledge_engine import KnowledgeEngine
from personal_context_mapper import PersonalContextMapper
import firebase_admin
from firebase_admin import credentials, firestore
import os

BASE_URL = "http://localhost:8080"

def setup_database():
    """Setup database connection"""
    try:
        db = firestore.client()
        return db
    except:
        print("⚠️ Using HTTP API instead of direct database access")
        return None

def direct_regenerate_stories():
    print("🎯 DIRECT STORY REGENERATION WITH NEW NATURAL PROMPTS")
    print("=" * 60)
    
    # Get existing stories with conversations
    print("1️⃣ Fetching existing stories...")
    response = requests.get(f"{BASE_URL}/api/stories")
    
    if response.status_code != 200:
        print(f"❌ Failed to get stories: {response.status_code}")
        return
    
    stories = response.json()
    print(f"✅ Found {len(stories)} total stories")
    
    # Filter stories with conversations
    stories_with_convs = [s for s in stories if s.get('conversation') and len(s.get('conversation', [])) > 3]
    print(f"📊 {len(stories_with_convs)} stories have conversation data")
    
    if not stories_with_convs:
        print("⚠️ No stories with conversations found")
        return
    
    # Setup engines for direct story generation
    knowledge_engine = KnowledgeEngine(db=None)
    personal_context_mapper = PersonalContextMapper(db=None)
    
    regenerated_count = 0
    improved_count = 0
    
    for i, story in enumerate(stories_with_convs, 1):
        print(f"\n🔄 Processing story {i}/{len(stories_with_convs)}")
        print(f"   📖 Original Title: '{story['title']}'")
        
        # Check/create unique user
        user_id = story.get('user_id')
        if not user_id or user_id == 'anonymous':
            # Create a unique user for this story
            timestamp_hash = abs(hash(story.get('timestamp', f'story_{i}'))) % 10000000
            user_id = f"regen_user_{i}_{timestamp_hash}"
            print(f"   👤 Creating user: {user_id}")
        else:
            print(f"   👤 Using existing user: {user_id}")
        
        conversation = story.get('conversation', [])
        if not conversation:
            print("   ⚠️ No conversation data, skipping")
            continue
        
        try:
            # Extract user messages for context
            user_messages = [msg['content'] for msg in conversation if msg.get('role') == 'user']
            conversation_text = "\n".join([f"User: {msg}" for msg in user_messages])
            
            print(f"   💬 Processing {len(user_messages)} user messages")
            
            # Analyze for domain insights
            domain_insights = knowledge_engine.analyze_story_for_insights(conversation_text, user_id)
            
            # Get user context
            user_context = personal_context_mapper.get_user_context_profile(user_id)
            
            # Generate new story with updated prompts
            print("   🤖 Generating story with new natural prompts...")
            new_story_content = generate_intelligent_story(
                conversation_text=conversation_text,
                user_context=user_context,
                domain_insights=domain_insights,
                conversation_flow=conversation
            )
            
            # Generate new natural title
            new_title = generate_intelligent_title(new_story_content, domain_insights, user_context)
            
            print(f"   📝 NEW STORY GENERATED!")
            print(f"      🔀 OLD: '{story['title']}'")
            print(f"      ✨ NEW: '{new_title}'")
            
            # Analyze naturalness improvement
            old_natural = analyze_naturalness(story['title'], story['content'])
            new_natural = analyze_naturalness(new_title, new_story_content)
            
            print(f"\n📊 NATURALNESS COMPARISON:")
            print(f"   OLD Score: {old_natural['score']:.1%} (Title: {'✅' if old_natural['title_natural'] else '❌'}, 1st Person: {'✅' if old_natural['first_person'] else '❌'}, Conv: {'✅' if old_natural['conversational'] else '❌'}, Natural: {'✅' if old_natural['natural_language'] else '❌'})")
            print(f"   NEW Score: {new_natural['score']:.1%} (Title: {'✅' if new_natural['title_natural'] else '❌'}, 1st Person: {'✅' if new_natural['first_person'] else '❌'}, Conv: {'✅' if new_natural['conversational'] else '❌'}, Natural: {'✅' if new_natural['natural_language'] else '❌'})")
            
            if new_natural['score'] > old_natural['score']:
                print(f"   🎉 IMPROVED! (+{(new_natural['score'] - old_natural['score'])*100:.0f} points)")
                improved_count += 1
            else:
                print(f"   ➡️  Similar quality")
            
            # Save the new story
            new_story_data = {
                'id': f"regen_{story['id']}_{i}",
                'title': new_title,
                'content': new_story_content,
                'author': 'You',
                'user_id': user_id,
                'timestamp': story.get('timestamp', ''),
                'format': 'text',
                'public': False,
                'reactions': 0,
                'inCosmos': True,
                'createdFormats': {},
                'conversation': conversation,
                'emotional_intensity': domain_insights.get('confidence', 0.5),
                'analysis': {
                    'themes': domain_insights.get('themes', []),
                    'domains': list(domain_insights.get('domains', {}).keys()),
                    'emotional_markers': domain_insights.get('emotional_markers', []),
                    'ai_generated': True,
                    'regenerated_with_natural_prompts': True
                },
                'cosmic_insights': domain_insights.get('themes', [])[:3],
                'original_story_id': story['id'],
                'regeneration_timestamp': '2025-01-01T00:00:00'
            }
            
            # Post the new story
            create_response = requests.post(f"{BASE_URL}/api/stories", json=new_story_data, headers={'X-User-ID': user_id})
            
            if create_response.status_code in [200, 201]:
                print(f"   ✅ New story saved successfully!")
                regenerated_count += 1
                
                print(f"\n📄 NEW STORY PREVIEW:")
                print("-" * 50)
                preview = new_story_content[:250] + "..." if len(new_story_content) > 250 else new_story_content
                print(preview)
                print("-" * 50)
            else:
                print(f"   ❌ Failed to save new story: {create_response.status_code}")
            
        except Exception as e:
            print(f"   ❌ Error processing story: {e}")
            continue
        
        print("\n" + "="*50)
    
    print(f"\n🎉 REGENERATION COMPLETE!")
    print(f"   📊 Processed: {len(stories_with_convs)} stories")
    print(f"   🔄 Successfully regenerated: {regenerated_count} stories")
    print(f"   ✅ Improved naturalness: {improved_count} stories")
    print(f"   📈 Improvement rate: {improved_count/regenerated_count*100:.1f}%" if regenerated_count > 0 else "   📈 Improvement rate: 0%")

def analyze_naturalness(title, content):
    """Analyze how natural and authentic the language sounds"""
    score = 0.0
    
    # Title analysis - avoid overly poetic words
    poetic_words = ['whisper', 'shadow', 'dance', 'thread', 'solace', 'embrace', 'ethereal', 'profound', 'tapestry', 'blossoming', 'embracing']
    title_natural = not any(word.lower() in title.lower() for word in poetic_words)
    if title_natural:
        score += 0.25
    
    # First person analysis
    first_person = content.count(' I ') >= 3 or content.lower().startswith('i ')
    if first_person:
        score += 0.25
    
    # Conversational phrases
    conversational_phrases = ['i realized', 'i started', 'i learned', 'looking back', 'the thing is', 'i guess', 'i never thought', 'it\'s funny', 'i remember', 'you know', 'i mean', 'gotta', 'boy,', 'honestly']
    conversational = any(phrase in content.lower() for phrase in conversational_phrases)
    if conversational:
        score += 0.25
    
    # Natural language (not overly fancy)
    overly_fancy = ['profound', 'ethereal', 'whisper', 'embrace', 'unfolds', 'tapestry', 'essence', 'illuminated', 'symphony', 'resonance', 'profound']
    natural_language = not any(word in content.lower() for word in overly_fancy)
    if natural_language:
        score += 0.25
    
    return {
        'score': score,
        'title_natural': title_natural,
        'first_person': first_person,
        'conversational': conversational,
        'natural_language': natural_language
    }

if __name__ == "__main__":
    try:
        direct_regenerate_stories()
    except KeyboardInterrupt:
        print("\n👋 Regeneration interrupted by user")
    except Exception as e:
        print(f"\n❌ Regeneration failed: {e}")
        import traceback
        traceback.print_exc() 