"""
Format Types
============

Shared format type definitions to avoid circular imports.
"""

from enum import Enum

class FormatType(Enum):
    # Social Media Formats
    X = "x"  # X (formerly Twitter)
    X_THREAD = "x_thread"
    LINKEDIN = "linkedin" 
    INSTAGRAM = "instagram"
    REEL = "reel"
    FACEBOOK = "facebook"
    TIKTOK_SCRIPT = "tiktok_script"
    
    # Creative Formats
    POEM = "poem"
    SONG = "song"
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