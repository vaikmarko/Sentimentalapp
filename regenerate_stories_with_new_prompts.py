#!/usr/bin/env python3
"""Regenerate existing stories with updated natural prompts"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def regenerate_stories_with_natural_prompts():
    print("🔄 REGENERATING STORIES WITH UPDATED NATURAL PROMPTS")
    print("=" * 60)
    
    # 1. Get all existing stories
    print("1️⃣ Fetching existing stories...")
    response = requests.get(f"{BASE_URL}/api/stories")
    
    if response.status_code != 200:
        print(f"❌ Failed to get stories: {response.status_code}")
        return
    
    stories = response.json()
    print(f"✅ Found {len(stories)} stories")
    
    # 2. Filter stories that have conversations (AI-generated ones)
    stories_with_conversations = []
    for story in stories:
        if story.get('conversation') and len(story['conversation']) > 2:
            stories_with_conversations.append(story)
    
    print(f"📊 {len(stories_with_conversations)} stories have conversation data")
    
    if not stories_with_conversations:
        print("⚠️ No stories with conversation data found")
        return
    
    # 3. Process each story with conversation data
    regenerated_count = 0
    improved_count = 0
    
    for i, story in enumerate(stories_with_conversations, 1):
        print(f"\n🔄 Processing story {i}/{len(stories_with_conversations)}")
        print(f"   📖 Original Title: '{story['title']}'")
        
        # Get the conversation from the story
        conversation = story.get('conversation', [])
        if not conversation:
            print("   ⚠️ No conversation data, skipping")
            continue
        
        # Extract user messages to simulate the conversation flow
        user_messages = [msg['content'] for msg in conversation if msg.get('role') == 'user']
        
        if len(user_messages) < 3:
            print("   ⚠️ Too few user messages, skipping")
            continue
        
        print(f"   💬 Found {len(user_messages)} user messages")
        
        # Find a user for this story
        user_id = story.get('user_id', 'anonymous')
        if user_id == 'anonymous':
            print("   ⚠️ No user_id, skipping")
            continue
        
        # Simulate the conversation flow to trigger story generation
        try:
            conversation_history = []
            story_created = False
            
            for j, message in enumerate(user_messages, 1):
                print(f"   📝 Sending message {j}: {message[:40]}...")
                
                chat_data = {
                    "message": message,
                    "user_id": user_id,
                    "conversation_history": conversation_history
                }
                
                chat_response = requests.post(f"{BASE_URL}/api/chat/message", json=chat_data)
                
                if chat_response.status_code == 200:
                    result = chat_response.json()
                    
                    # Update conversation history
                    conversation_history.append({"role": "user", "content": message})
                    if result.get('message'):
                        conversation_history.append({"role": "assistant", "content": result['message']})
                    
                    readiness_score = result.get('story_readiness_score', 0)
                    print(f"      📊 Story readiness: {readiness_score:.2f}")
                    
                    # Check if story was created
                    if result.get('story_created'):
                        new_story_id = result.get('story_id')
                        new_title = result.get('story_title')
                        
                        print(f"   🎉 NEW STORY CREATED!")
                        print(f"      📖 New Title: '{new_title}'")
                        print(f"      🆔 New Story ID: {new_story_id}")
                        
                        # Get the new story content
                        stories_response = requests.get(f"{BASE_URL}/api/stories")
                        if stories_response.status_code == 200:
                            updated_stories = stories_response.json()
                            new_story = next((s for s in updated_stories if s['id'] == new_story_id), None)
                            
                            if new_story:
                                print(f"\n📊 COMPARISON:")
                                print(f"   OLD: '{story['title']}'")
                                print(f"   NEW: '{new_story['title']}'")
                                
                                # Analyze improvement
                                old_natural = analyze_naturalness(story['title'], story['content'])
                                new_natural = analyze_naturalness(new_story['title'], new_story['content'])
                                
                                if new_natural['score'] > old_natural['score']:
                                    print(f"   ✅ IMPROVED! ({old_natural['score']:.1%} → {new_natural['score']:.1%})")
                                    improved_count += 1
                                else:
                                    print(f"   ➡️  Similar quality ({old_natural['score']:.1%} → {new_natural['score']:.1%})")
                                
                                print(f"\n📄 NEW STORY CONTENT:")
                                print("-" * 50)
                                print(new_story['content'][:300] + "..." if len(new_story['content']) > 300 else new_story['content'])
                                print("-" * 50)
                        
                        story_created = True
                        regenerated_count += 1
                        break
                
                else:
                    print(f"      ❌ Chat failed: {chat_response.status_code}")
                
                time.sleep(0.3)  # Small delay between messages
            
            if not story_created:
                print("   ⚠️ No story was generated from this conversation")
        
        except Exception as e:
            print(f"   ❌ Error processing story: {e}")
            continue
        
        print("\n" + "="*40)
        time.sleep(1)  # Pause between stories
    
    print(f"\n🎉 REGENERATION COMPLETE!")
    print(f"   📊 Processed: {len(stories_with_conversations)} stories")
    print(f"   🔄 Regenerated: {regenerated_count} stories")
    print(f"   ✅ Improved: {improved_count} stories")
    print(f"   📈 Improvement rate: {improved_count/regenerated_count*100:.1f}%" if regenerated_count > 0 else "   📈 Improvement rate: 0%")

def analyze_naturalness(title, content):
    """Analyze how natural and authentic the language sounds"""
    score = 0.0
    
    # Title analysis
    poetic_words = ['whisper', 'shadow', 'dance', 'thread', 'solace', 'embrace', 'ethereal', 'profound', 'tapestry']
    title_natural = not any(word.lower() in title.lower() for word in poetic_words)
    if title_natural:
        score += 0.25
    
    # First person analysis
    first_person = content.count(' I ') >= 3 or content.lower().startswith('i ')
    if first_person:
        score += 0.25
    
    # Conversational phrases
    conversational_phrases = ['i realized', 'i started', 'i learned', 'looking back', 'the thing is', 'i guess', 'i never thought', 'it\'s funny', 'i remember', 'you know', 'i mean', 'gotta']
    conversational = any(phrase in content.lower() for phrase in conversational_phrases)
    if conversational:
        score += 0.25
    
    # Natural language (not overly fancy)
    overly_fancy = ['profound', 'ethereal', 'whisper', 'embrace', 'unfolds', 'tapestry', 'essence', 'illuminated', 'symphony', 'resonance']
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
        regenerate_stories_with_natural_prompts()
    except KeyboardInterrupt:
        print("\n👋 Regeneration interrupted by user")
    except Exception as e:
        print(f"\n❌ Regeneration failed: {e}") 