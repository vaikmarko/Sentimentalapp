#!/usr/bin/env python3
"""
Test Format Generation for Marcus Rodriguez's Story
Demonstrates all available format types and their output quality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from formats_generation_engine import FormatsGenerationEngine, FormatType
import json

# Marcus Rodriguez's story content
MARCUS_STORY = """
I used to love making videos because it felt creative and authentic. But lately, everything feels like work. I'm spending more time worrying about views and engagement than actually enjoying the process of creating. 

Yesterday I realized I've been creating content based on what I think people want to see, not what I actually want to share. The algorithm has become my creative director instead of my own curiosity and passion.

I need to remember why I started: the joy of storytelling and connecting with people through shared experiences. Maybe it's time to create for the love of it again, even if fewer people see it.
"""

def test_all_formats():
    """Test all available format types"""
    
    print("🎨 TESTING ALL FORMAT TYPES FOR MARCUS'S STORY")
    print("=" * 60)
    
    # Initialize the engine
    engine = FormatsGenerationEngine()
    
    # All available format types
    format_types = [
        FormatType.TWITTER,
        FormatType.LINKEDIN, 
        FormatType.INSTAGRAM,
        FormatType.FACEBOOK,
        FormatType.POEM,
        FormatType.SONG,
        FormatType.SCRIPT,
        FormatType.SHORT_STORY,
        FormatType.ARTICLE,
        FormatType.BLOG_POST,
        FormatType.PRESENTATION,
        FormatType.NEWSLETTER,
        FormatType.INSIGHTS,
        FormatType.REFLECTION,
        FormatType.GROWTH_SUMMARY,
        FormatType.JOURNAL_ENTRY
    ]
    
    results = {}
    
    for format_type in format_types:
        print(f"\n📝 Generating {format_type.value.upper()} format...")
        
        try:
            result = engine.generate_format(MARCUS_STORY, format_type)
            
            if result.get('success'):
                content = result['content']
                char_count = result.get('character_count', len(content))
                word_count = result.get('word_count', len(content.split()))
                method = result.get('generation_method', 'unknown')
                
                print(f"✅ SUCCESS - {char_count} chars, {word_count} words ({method})")
                print(f"📄 Preview: {content[:150]}...")
                
                results[format_type.value] = {
                    'success': True,
                    'content': content,
                    'character_count': char_count,
                    'word_count': word_count,
                    'method': method
                }
            else:
                error = result.get('error', 'Unknown error')
                print(f"❌ FAILED - {error}")
                results[format_type.value] = {'success': False, 'error': error}
                
        except Exception as e:
            print(f"💥 EXCEPTION - {str(e)}")
            results[format_type.value] = {'success': False, 'error': str(e)}
    
    # Summary
    successful = len([r for r in results.values() if r.get('success')])
    total = len(results)
    
    print(f"\n🎯 SUMMARY: {successful}/{total} formats generated successfully")
    
    return results

def show_format_details(results):
    """Show detailed output for each format"""
    
    print("\n" + "=" * 60)
    print("📋 DETAILED FORMAT OUTPUTS")
    print("=" * 60)
    
    for format_name, result in results.items():
        if result.get('success'):
            print(f"\n🎨 {format_name.upper()} FORMAT:")
            print("-" * 40)
            print(result['content'])
            print(f"\n📊 Stats: {result['character_count']} chars, {result['word_count']} words")
            print("-" * 40)

if __name__ == "__main__":
    try:
        results = test_all_formats()
        
        # Show successful formats in detail
        successful_results = {k: v for k, v in results.items() if v.get('success')}
        if successful_results:
            show_format_details(successful_results)
        else:
            print("\n❌ No formats were successfully generated")
            
    except Exception as e:
        print(f"\n💥 Script failed: {e}") 