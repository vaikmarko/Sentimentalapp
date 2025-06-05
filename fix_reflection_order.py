#!/usr/bin/env python3
"""
Fix Reflection Format Order
===========================

This script reorders the createdFormats arrays in existing stories
to move 'reflection' to the first position among therapeutic formats.
"""

import firebase_admin
from firebase_admin import credentials, firestore
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_firebase():
    """Initialize Firebase for local development"""
    try:
        # Initialize Firebase app
        if not firebase_admin._apps:
            # In local development, use default credentials
            firebase_admin.initialize_app()
        
        # Get Firestore client
        db = firestore.client()
        logger.info("Firebase initialized successfully")
        return db
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        return None

def reorder_created_formats(created_formats_list):
    """Reorder formats to put reflection first among therapeutic formats"""
    if not created_formats_list or 'reflection' not in created_formats_list:
        return created_formats_list
    
    # Define therapeutic formats
    therapeutic_formats = ['reflection', 'insights', 'growth_summary', 'journal_entry']
    
    # Separate formats
    therapeutic_in_story = [f for f in created_formats_list if f in therapeutic_formats]
    non_therapeutic = [f for f in created_formats_list if f not in therapeutic_formats]
    
    # Sort therapeutic formats with reflection first
    therapeutic_sorted = sorted(therapeutic_in_story, 
                              key=lambda x: 0 if x == 'reflection' else therapeutic_formats.index(x))
    
    # Rebuild the list: non-therapeutic first, then therapeutic with reflection first
    return non_therapeutic + therapeutic_sorted

def fix_stories_reflection_order():
    """Fix the reflection ordering in all existing stories"""
    db = init_firebase()
    if not db:
        return
    
    try:
        # Get all stories
        stories_ref = db.collection('test_stories')
        stories = stories_ref.get()
        
        updated_count = 0
        total_count = 0
        
        for story_doc in stories:
            total_count += 1
            story_data = story_doc.to_dict()
            story_id = story_doc.id
            
            created_formats = story_data.get('createdFormats', [])
            
            if 'reflection' in created_formats:
                # Reorder the formats
                new_order = reorder_created_formats(created_formats)
                
                if new_order != created_formats:
                    logger.info(f"Updating story {story_id}:")
                    logger.info(f"  Old order: {created_formats}")
                    logger.info(f"  New order: {new_order}")
                    
                    # Update the story
                    story_doc.reference.update({
                        'createdFormats': new_order
                    })
                    updated_count += 1
                else:
                    logger.info(f"Story {story_id} already has correct order")
            else:
                logger.info(f"Story {story_id} doesn't have reflection format")
        
        logger.info(f"✅ Processing complete:")
        logger.info(f"   Total stories: {total_count}")
        logger.info(f"   Updated stories: {updated_count}")
        
    except Exception as e:
        logger.error(f"Error fixing reflection order: {e}")

if __name__ == "__main__":
    print("🔧 Fixing reflection format order in existing stories...")
    fix_stories_reflection_order()
    print("✅ Done!") 