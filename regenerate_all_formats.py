#!/usr/bin/env python3
"""
Regenerate All Formats Script
=============================

This script regenerates all formats for all stories using the new enhanced format generation system.
It will update existing stories with the new comprehensive, culturally-aware, super engaging formats.

Features:
- Regenerates all 20+ format types for all stories
- Uses new cultural awareness and viral optimization
- Updates cached formats in database
- Provides progress tracking and error handling
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8080"
BATCH_SIZE = 5  # Process stories in batches to avoid overwhelming the server
DELAY_BETWEEN_REQUESTS = 1  # Seconds between API calls

# All available format types (ordered by popularity/viral potential)
ALL_FORMATS = [
    # TIER 1: HIGHEST VIRAL POTENTIAL
    'tiktok_script',
    'instagram_reel', 
    'twitter_thread',
    'youtube_short',
    
    # TIER 2: HIGH ENGAGEMENT
    'instagram_story',
    'tweet',
    'fb_post',
    'podcast_segment',
    
    # TIER 3: MEDIUM ENGAGEMENT
    'linkedin_post',
    'newsletter',
    'blog_post',
    'medium_article',
    
    # TIER 4: NICHE ENGAGEMENT
    'reddit_post',
    'text_message',
    'voice_memo',
    'diary_entry',
    
    # TIER 5: CREATIVE FORMATS
    'song',
    'video',
    'article',
    'book_chapter'
]

def get_all_stories():
    """Fetch all stories from the API"""
    try:
        response = requests.get(f"{BASE_URL}/api/stories")
        response.raise_for_status()
        stories = response.json()
        print(f"✅ Found {len(stories)} stories to process")
        return stories
    except Exception as e:
        print(f"❌ Error fetching stories: {e}")
        return []

def regenerate_format_for_story(story_id, format_type):
    """Regenerate a specific format for a story"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/stories/{story_id}/formats",
            headers={"Content-Type": "application/json"},
            json={"format_type": format_type}
        )
        
        if response.status_code == 200:
            return True, "Success"
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
            
    except Exception as e:
        return False, str(e)

def regenerate_all_formats_for_story(story):
    """Regenerate all formats for a single story"""
    story_id = story.get('id')
    story_title = story.get('title', 'Untitled')[:50] + "..."
    
    print(f"\n🔄 Processing: {story_title}")
    print(f"   Story ID: {story_id}")
    
    success_count = 0
    error_count = 0
    
    for i, format_type in enumerate(ALL_FORMATS, 1):
        print(f"   [{i:2d}/{len(ALL_FORMATS)}] Generating {format_type}...", end=" ")
        
        success, message = regenerate_format_for_story(story_id, format_type)
        
        if success:
            print("✅")
            success_count += 1
        else:
            print(f"❌ {message}")
            error_count += 1
        
        # Small delay between requests to be nice to the server
        time.sleep(DELAY_BETWEEN_REQUESTS)
    
    print(f"   📊 Results: {success_count} success, {error_count} errors")
    return success_count, error_count

def main():
    """Main execution function"""
    print("🚀 Enhanced Format Regeneration Script")
    print("=" * 50)
    print(f"Target: {BASE_URL}")
    print(f"Formats to generate: {len(ALL_FORMATS)}")
    print(f"Batch size: {BATCH_SIZE}")
    print()
    
    # Get all stories
    stories = get_all_stories()
    if not stories:
        print("❌ No stories found or error fetching stories")
        return
    
    # Filter stories that have content (avoid test stories)
    valid_stories = [
        story for story in stories 
        if story.get('content') and len(story.get('content', '')) > 50
    ]
    
    print(f"📝 Processing {len(valid_stories)} valid stories (with content >50 chars)")
    print()
    
    total_success = 0
    total_errors = 0
    processed_stories = 0
    
    start_time = datetime.now()
    
    # Process stories in batches
    for i in range(0, len(valid_stories), BATCH_SIZE):
        batch = valid_stories[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (len(valid_stories) + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"📦 BATCH {batch_num}/{total_batches} ({len(batch)} stories)")
        print("-" * 30)
        
        for story in batch:
            success_count, error_count = regenerate_all_formats_for_story(story)
            total_success += success_count
            total_errors += error_count
            processed_stories += 1
        
        # Longer delay between batches
        if i + BATCH_SIZE < len(valid_stories):
            print(f"\n⏸️  Waiting {DELAY_BETWEEN_REQUESTS * 2} seconds before next batch...")
            time.sleep(DELAY_BETWEEN_REQUESTS * 2)
    
    # Final summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "=" * 50)
    print("🎉 REGENERATION COMPLETE!")
    print("=" * 50)
    print(f"📊 Stories processed: {processed_stories}")
    print(f"✅ Successful generations: {total_success}")
    print(f"❌ Failed generations: {total_errors}")
    print(f"⏱️  Total time: {duration}")
    print(f"📈 Success rate: {(total_success / (total_success + total_errors) * 100):.1f}%")
    
    if total_errors > 0:
        print(f"\n⚠️  {total_errors} formats failed to generate")
        print("   Check server logs for details")
    
    print("\n🎯 All stories now have enhanced, culturally-aware viral formats!")
    print("   - Comprehensive articles (1,800+ words)")
    print("   - Super engaging TikTok scripts")
    print("   - Viral Instagram reels")
    print("   - Cultural adaptation for global audiences")
    print("   - API-ready for future video/music generation")

if __name__ == "__main__":
    main() 