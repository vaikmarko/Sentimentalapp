"""
Format Types
============

Shared format type definitions to avoid circular imports.
"""

from enum import Enum

class FormatType(Enum):
    # Social Media Formats
    TWITTER = "twitter"
    LINKEDIN = "linkedin" 
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    
    # Creative Formats
    POEM = "poem"
    SONG = "song"
    SCRIPT = "script"
    SHORT_STORY = "short_story"
    
    # Professional Formats
    ARTICLE = "article"
    BLOG_POST = "blog_post"
    PRESENTATION = "presentation"
    NEWSLETTER = "newsletter"
    
    # Therapeutic Formats - reflection moved to first position
    REFLECTION = "reflection"
    INSIGHTS = "insights"
    GROWTH_SUMMARY = "growth_summary"
    JOURNAL_ENTRY = "journal_entry" 