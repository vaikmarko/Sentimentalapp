"""
Format Types
============

Shared format type definitions to avoid circular imports.
"""

from enum import Enum

class FormatType(Enum):
    # Social Media Formats
    TWITTER = "twitter"
    TWITTER_THREAD = "twitter_thread"
    LINKEDIN = "linkedin" 
    INSTAGRAM = "instagram"
    INSTAGRAM_REEL = "instagram_reel"
    FACEBOOK = "facebook"
    TIKTOK_SCRIPT = "tiktok_script"
    
    # Creative Formats
    POEM = "poem"
    SONG = "song"
    REEL = "reel"
    SHORT_STORY = "short_story"
    
    # Professional Formats
    ARTICLE = "article"
    BLOG_POST = "blog_post"
    PRESENTATION = "presentation"
    NEWSLETTER = "newsletter"
    PODCAST = "podcast"
    
    # Therapeutic Formats
    INSIGHTS = "insights"
    GROWTH_SUMMARY = "growth_summary"
    JOURNAL_ENTRY = "journal_entry" 