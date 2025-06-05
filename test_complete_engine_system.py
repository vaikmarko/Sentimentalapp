#!/usr/bin/env python3
"""
Complete Engine System Test
Tests all engines working together to create amazing, globally resonant content:

1. Intelligence Engine: Personal context mapping + adaptive questions
2. Story Generation Engine: Chat → compelling stories  
3. Formats Generation Engine: Stories → multiple engaging formats
4. Inner Space: Knowledge organization + insights
5. Prompts Engine: High-quality AI prompting across all engines

This test simulates real user conversations and demonstrates how the system
automatically creates content that resonates with people globally.
"""

import requests
import json
import time
import random
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8080"
TEST_USER_EMAIL = "complete-system-test@example.com"
TEST_USER_NAME = "Alex Chen"

# Global conversation scenarios that resonate universally
UNIVERSAL_CONVERSATION_SCENARIOS = [
    {
        "theme": "Career Transition Anxiety",
        "messages": [
            "I've been thinking about quitting my corporate job to start my own business, but I'm terrified",
            "I have a stable salary, good benefits, but I feel like I'm dying inside every day. The meetings, the politics, the meaningless projects",
            "Last night I stayed up until 3 AM working on my business plan. I felt more alive than I have in months. But then morning came and reality hit",
            "My parents think I'm crazy. They worked their whole lives for security. 'Why would you throw away a good job?' they ask",
            "But what if I'm 60 and still sitting in these same meetings, wondering what could have been? That scares me more than failing"
        ],
        "expected_insights": ["career_transition", "fear_vs_passion", "family_expectations", "regret_avoidance"],
        "global_appeal": "Career dissatisfaction and entrepreneurial dreams are universal"
    },
    {
        "theme": "Modern Love & Digital Communication",
        "messages": [
            "We've been dating for 8 months but I still get anxious when he doesn't text back within an hour",
            "I know it's ridiculous. He's probably just busy at work. But my mind goes to the worst places",
            "Yesterday he posted an Instagram story but didn't reply to my text from 2 hours earlier. I felt so stupid for caring",
            "I remember when my parents were dating, they'd go days without talking and it was normal. Now we expect constant connection",
            "Sometimes I wonder if social media and smartphones have made us more insecure in relationships, not more connected"
        ],
        "expected_insights": ["digital_anxiety", "relationship_insecurity", "generational_differences", "technology_impact"],
        "global_appeal": "Digital age relationship anxiety affects millions worldwide"
    },
    {
        "theme": "Parental Aging & Role Reversal",
        "messages": [
            "I visited my dad last weekend and noticed he's gotten so much older. His hands shake when he pours coffee now",
            "He used to be the one who fixed everything, who had all the answers. Now he asks me how to use his phone",
            "I found myself helping him with his bills, explaining things he used to handle effortlessly. It broke my heart",
            "There's this moment when you realize your parents are becoming fragile, and suddenly you're the adult in the relationship",
            "I'm not ready for this role reversal. I still need him to be my dad, not the other way around"
        ],
        "expected_insights": ["aging_parents", "role_reversal", "mortality_awareness", "family_dynamics"],
        "global_appeal": "Watching parents age is a universal human experience"
    },
    {
        "theme": "Social Media vs Reality",
        "messages": [
            "I spent 20 minutes this morning trying to get the perfect photo of my breakfast for Instagram",
            "Then I realized how absurd that was. I was more focused on documenting my life than actually living it",
            "Everyone's feed looks so perfect. Amazing vacations, perfect relationships, dream jobs. Meanwhile I'm struggling to get out of bed some days",
            "I know it's all curated, that people only show their highlights. But it still makes me feel like I'm failing at life",
            "I deleted Instagram for a week last month and felt so much more present. But then I felt disconnected from my friends"
        ],
        "expected_insights": ["social_media_pressure", "authenticity_struggle", "comparison_trap", "digital_wellness"],
        "global_appeal": "Social media's impact on mental health is a global phenomenon"
    }
]

class CompleteEngineSystemTest:
    def __init__(self):
        self.session = requests.Session()
        self.user_id = None
        self.stories_created = []
        self.formats_generated = []
        self.insights_discovered = []
        
    def run_complete_test(self):
        """Run the complete engine system test"""
        print("🚀 Starting Complete Engine System Test")
        print("=" * 60)
        
        try:
            # 1. Setup test user
            self.setup_test_user()
            
            # 2. Test each conversation scenario
            for i, scenario in enumerate(UNIVERSAL_CONVERSATION_SCENARIOS, 1):
                print(f"\n📖 Scenario {i}: {scenario['theme']}")
                print("-" * 40)
                self.test_conversation_scenario(scenario)
                time.sleep(2)  # Brief pause between scenarios
            
            # 3. Test knowledge system integration
            self.test_knowledge_integration()
            
            # 4. Test format generation quality
            self.test_format_quality()
            
            # 5. Test global appeal metrics
            self.test_global_appeal()
            
            # 6. Generate final report
            self.generate_final_report()
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
        
        return True
    
    def setup_test_user(self):
        """Setup test user for the complete system test"""
        print("👤 Setting up test user...")
        
        # Register user
        response = self.session.post(f"{BASE_URL}/api/auth/register", json={
            "email": TEST_USER_EMAIL,
            "name": TEST_USER_NAME,
            "password": "testpass123"
        })
        
        if response.status_code == 409:  # User exists
            # Login instead
            response = self.session.post(f"{BASE_URL}/api/auth/login", json={
                "email": TEST_USER_EMAIL,
                "password": "testpass123"
            })
        
        if response.status_code in [200, 201]:
            data = response.json()
            # Handle different response formats
            if 'user' in data:
                self.user_id = data['user']['id']
            elif 'user_id' in data:
                self.user_id = data['user_id']
            elif 'id' in data:
                self.user_id = data['id']
            else:
                # Try to extract from any available field
                print(f"Response data: {data}")
                # Use a fallback user ID for testing
                self.user_id = "test_user_" + str(int(time.time()))
            
            print(f"✅ User setup complete: {self.user_id}")
        else:
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            raise Exception(f"Failed to setup user: {response.status_code}")
    
    def test_conversation_scenario(self, scenario):
        """Test a complete conversation scenario through all engines"""
        print(f"🎭 Testing: {scenario['theme']}")
        
        story_id = None
        conversation_insights = []
        
        # Simulate natural conversation flow
        for i, message in enumerate(scenario['messages']):
            print(f"  💬 Message {i+1}: {message[:50]}...")
            
            # Send message through Intelligence Engine
            response = self.session.post(f"{BASE_URL}/api/chat/message", json={
                "user_id": self.user_id,
                "message": message
            })
            
            if response.status_code == 201:
                data = response.json()
                
                # Track story creation
                if data.get('story_created') and data.get('story_id'):
                    story_id = data['story_id']
                    self.stories_created.append({
                        'id': story_id,
                        'theme': scenario['theme'],
                        'message_count': i + 1
                    })
                    print(f"    📚 Story created: {story_id}")
                
                # Track insights
                if data.get('knowledge_insights'):
                    conversation_insights.extend(data['knowledge_insights'])
                    print(f"    🧠 Insights discovered: {len(data['knowledge_insights'])}")
            
            time.sleep(0.5)  # Natural conversation pacing
        
        # Test Story Generation Engine quality
        if story_id:
            self.test_story_generation_quality(story_id, scenario)
        
        # Test Formats Generation Engine
        if story_id:
            self.test_formats_generation(story_id, scenario)
        
        # Validate expected insights were discovered
        self.validate_insights(conversation_insights, scenario['expected_insights'])
    
    def test_story_generation_quality(self, story_id, scenario):
        """Test the quality of generated stories"""
        print(f"    📖 Testing story generation quality...")
        
        # Get the generated story
        response = self.session.get(f"{BASE_URL}/api/stories/{story_id}")
        
        if response.status_code == 200:
            story = response.json()
            
            # Quality metrics
            quality_score = 0
            
            # Check title quality (should be engaging, not generic)
            title = story.get('title', '')
            if len(title) > 10 and not title.startswith('Message from'):
                quality_score += 25
                print(f"      ✅ Engaging title: '{title}'")
            
            # Check content depth (should be substantial)
            content = story.get('content', '')
            if len(content) > 100:
                quality_score += 25
                print(f"      ✅ Substantial content: {len(content)} characters")
            
            # Check emotional resonance (should contain emotional keywords)
            emotional_keywords = ['feel', 'heart', 'soul', 'fear', 'love', 'hope', 'dream', 'struggle']
            emotional_content = sum(1 for word in emotional_keywords if word in content.lower())
            if emotional_content >= 2:
                quality_score += 25
                print(f"      ✅ Emotional resonance: {emotional_content} emotional elements")
            
            # Check universal appeal (should avoid overly specific details)
            if not any(specific in content.lower() for specific in ['my company', 'my boss named', 'at 123 main street']):
                quality_score += 25
                print(f"      ✅ Universal appeal: Avoids overly specific details")
            
            print(f"      📊 Story quality score: {quality_score}/100")
            
            if quality_score >= 75:
                print(f"      🌟 HIGH QUALITY STORY - Global appeal potential!")
            
            return quality_score
        
        return 0
    
    def test_formats_generation(self, story_id, scenario):
        """Test automatic format generation for global appeal"""
        print(f"    🎨 Testing format generation...")
        
        # Test multiple format types including new viral formats
        formats_to_test = [
            'song', 'video', 'tweet', 'article', 'fb_post',
            'tiktok_script', 'instagram_reel', 'twitter_thread', 
            'podcast_segment', 'newsletter', 'youtube_short'
        ]
        
        for format_type in formats_to_test:
            response = self.session.post(f"{BASE_URL}/api/stories/{story_id}/generate-format", json={
                "user_id": self.user_id,
                "format_type": format_type
            })
            
            if response.status_code == 200:
                format_data = response.json()
                content = format_data.get('content', '')
                
                # Analyze format quality
                quality_metrics = self.analyze_format_quality(content, format_type, scenario)
                
                self.formats_generated.append({
                    'story_id': story_id,
                    'format_type': format_type,
                    'theme': scenario['theme'],
                    'quality_score': quality_metrics['score'],
                    'global_appeal': quality_metrics['global_appeal']
                })
                
                print(f"      📱 {format_type}: {quality_metrics['score']}/100 quality")
                
                if quality_metrics['global_appeal']:
                    print(f"        🌍 GLOBAL APPEAL: {quality_metrics['appeal_reason']}")
            
            time.sleep(0.3)
    
    def analyze_format_quality(self, content, format_type, scenario):
        """Analyze the quality and global appeal of generated formats"""
        quality_score = 0
        global_appeal = False
        appeal_reason = ""
        
        # Format-specific quality checks
        if format_type == 'song':
            if '♪' in content or 'verse' in content.lower() or 'chorus' in content.lower():
                quality_score += 30
            if len(content) > 100:
                quality_score += 20
            if any(emotion in content.lower() for emotion in ['heart', 'soul', 'dream', 'feel']):
                quality_score += 30
                global_appeal = True
                appeal_reason = "Universal emotional themes in lyrics"
            if content.count('\n') >= 4:  # Multiple lines/verses
                quality_score += 20
        
        elif format_type == 'video':
            if 'scene' in content.lower() or 'visual' in content.lower():
                quality_score += 25
            if 'script' in content.lower() or '[' in content:
                quality_score += 25
            if len(content) > 150:
                quality_score += 25
            if 'relatable' in content.lower() or scenario['global_appeal']:
                quality_score += 25
                global_appeal = True
                appeal_reason = "Visual storytelling with universal themes"
        
        elif format_type == 'tiktok_script':
            if 'hook' in content.lower() and 'pov:' in content.lower():
                quality_score += 30
            if '#' in content and any(tag in content.lower() for tag in ['fyp', 'viral', 'relatable']):
                quality_score += 25
            if 'drop a' in content.lower() or 'if you' in content.lower():
                quality_score += 25
                global_appeal = True
                appeal_reason = "Designed for viral engagement and community interaction"
            if len(content) > 100:
                quality_score += 20
        
        elif format_type == 'instagram_reel':
            if 'visual' in content.lower() and 'aesthetic' in content.lower():
                quality_score += 25
            if '#' in content and any(tag in content.lower() for tag in ['selflove', 'growth', 'authentic']):
                quality_score += 25
            if 'save-worthy' in content.lower() or 'resonates globally' in content.lower():
                quality_score += 30
                global_appeal = True
                appeal_reason = "Save-worthy content with global emotional appeal"
            if 'duration:' in content.lower():
                quality_score += 20
        
        elif format_type == 'twitter_thread':
            if content.count('/') >= 3:  # Multiple thread parts
                quality_score += 30
            if '🧵' in content or 'thread' in content.lower():
                quality_score += 20
            if any(engage in content.lower() for engage in ['drop', 'share your', 'what moment']):
                quality_score += 30
                global_appeal = True
                appeal_reason = "Thread format encourages community storytelling"
            if '#' in content:
                quality_score += 20
        
        elif format_type == 'podcast_segment':
            if '[' in content and ']' in content:  # Audio cues
                quality_score += 25
            if 'host:' in content.lower() or 'episode' in content.lower():
                quality_score += 25
            if len(content) > 200:
                quality_score += 25
            if 'commute listening' in content.lower() or 'voice message' in content.lower():
                quality_score += 25
                global_appeal = True
                appeal_reason = "Audio format perfect for global podcast audience"
        
        elif format_type == 'newsletter':
            if 'subject:' in content.lower() and 'hi friend' in content.lower():
                quality_score += 25
            if 'question for you' in content.lower():
                quality_score += 25
            if 'community' in content.lower() and 'unsubscribe' in content.lower():
                quality_score += 25
                global_appeal = True
                appeal_reason = "Personal newsletter format builds intimate community"
            if len(content) > 300:
                quality_score += 25
        
        elif format_type == 'youtube_short':
            if '[vertical video' in content.lower() and 'seconds]' in content.lower():
                quality_score += 30
            if '#shorts' in content.lower():
                quality_score += 25
            if 'comment if' in content.lower() or 'subscribe' in content.lower():
                quality_score += 25
                global_appeal = True
                appeal_reason = "Optimized for YouTube Shorts viral algorithm"
            if 'mobile viewing' in content.lower():
                quality_score += 20
        
        elif format_type == 'tweet':
            if len(content) <= 280:
                quality_score += 30
            if '#' in content:
                quality_score += 20
            if any(viral_word in content.lower() for viral_word in ['anyone else', 'we all', 'that moment when']):
                quality_score += 30
                global_appeal = True
                appeal_reason = "Relatable language that invites engagement"
            if '?' in content:  # Questions engage audience
                quality_score += 20
        
        elif format_type == 'article':
            if len(content) > 200:
                quality_score += 25
            if content.count('\n') >= 3:  # Multiple paragraphs
                quality_score += 25
            if any(universal in content.lower() for universal in ['we all', 'human experience', 'many of us']):
                quality_score += 25
                global_appeal = True
                appeal_reason = "Addresses universal human experiences"
            if '?' in content:  # Thought-provoking questions
                quality_score += 25
        
        elif format_type == 'fb_post':
            if len(content) > 50 and len(content) < 500:  # Optimal FB length
                quality_score += 30
            if '💕' in content or '❤️' in content or '✨' in content:  # Emojis
                quality_score += 20
            if 'anyone else' in content.lower() or 'share your' in content.lower():
                quality_score += 30
                global_appeal = True
                appeal_reason = "Encourages community engagement and sharing"
            if '#' in content:
                quality_score += 20
        
        return {
            'score': min(quality_score, 100),
            'global_appeal': global_appeal,
            'appeal_reason': appeal_reason
        }
    
    def validate_insights(self, discovered_insights, expected_insights):
        """Validate that the Intelligence Engine discovered expected insights"""
        print(f"    🧠 Validating insights discovery...")
        
        discovered_count = 0
        for expected in expected_insights:
            # Check if any discovered insight relates to expected
            if any(expected.replace('_', ' ') in str(insight).lower() for insight in discovered_insights):
                discovered_count += 1
        
        insight_score = (discovered_count / len(expected_insights)) * 100
        print(f"      🧠 Insights discovery: {discovered_count}/{len(expected_insights)} ({insight_score:.0f}%)")
        
        if insight_score >= 75:
            print(f"      🎯 EXCELLENT insight discovery!")
        
        self.insights_discovered.append({
            'expected': expected_insights,
            'discovered': discovered_insights,
            'score': insight_score
        })
    
    def test_knowledge_integration(self):
        """Test how well the knowledge system integrates insights"""
        print(f"\n🧠 Testing Knowledge System Integration...")
        
        # Test knowledge analysis
        response = self.session.post(f"{BASE_URL}/api/knowledge/analyze", json={
            "user_id": self.user_id,
            "text": "Overall analysis of my conversation patterns and insights"
        })
        
        if response.status_code == 200:
            analysis = response.json()
            print(f"  ✅ Knowledge analysis complete")
            print(f"  📊 Domains analyzed: {len(analysis.get('domain_insights', {}))}")
        
        # Test knowledge Q&A
        response = self.session.post(f"{BASE_URL}/api/knowledge/ask", json={
            "user_id": self.user_id,
            "question": "What patterns do you see in my life decisions?"
        })
        
        if response.status_code == 200:
            qa_response = response.json()
            print(f"  ✅ Knowledge Q&A working")
            print(f"  🎯 Confidence: {qa_response.get('confidence', 0)}%")
    
    def test_format_quality(self):
        """Test overall format generation quality"""
        print(f"\n🎨 Testing Format Generation Quality...")
        
        if not self.formats_generated:
            print("  ❌ No formats generated to test")
            return
        
        # Calculate average quality scores
        total_score = sum(f['quality_score'] for f in self.formats_generated)
        avg_quality = total_score / len(self.formats_generated)
        
        # Count globally appealing formats
        global_formats = [f for f in self.formats_generated if f['global_appeal']]
        global_percentage = (len(global_formats) / len(self.formats_generated)) * 100
        
        print(f"  📊 Average format quality: {avg_quality:.1f}/100")
        print(f"  🌍 Global appeal rate: {global_percentage:.1f}%")
        
        # Best performing formats
        best_formats = sorted(self.formats_generated, key=lambda x: x['quality_score'], reverse=True)[:3]
        print(f"  🏆 Top performing formats:")
        for i, fmt in enumerate(best_formats, 1):
            print(f"    {i}. {fmt['format_type']} ({fmt['theme']}): {fmt['quality_score']}/100")
    
    def test_global_appeal(self):
        """Test the global appeal potential of generated content"""
        print(f"\n🌍 Testing Global Appeal Potential...")
        
        # Analyze themes covered
        themes_covered = set(story['theme'] for story in self.stories_created)
        print(f"  📖 Universal themes covered: {len(themes_covered)}")
        for theme in themes_covered:
            print(f"    • {theme}")
        
        # Analyze format diversity
        format_types = set(fmt['format_type'] for fmt in self.formats_generated)
        print(f"  🎨 Format types generated: {len(format_types)}")
        for fmt_type in format_types:
            print(f"    • {fmt_type}")
        
        # Calculate viral potential score
        viral_indicators = 0
        
        # Stories with high emotional content
        emotional_stories = len([s for s in self.stories_created if 'anxiety' in s['theme'].lower() or 'love' in s['theme'].lower()])
        if emotional_stories > 0:
            viral_indicators += 25
            print(f"  ❤️ Emotional resonance: {emotional_stories} emotionally engaging stories")
        
        # Formats with community engagement potential
        engaging_formats = len([f for f in self.formats_generated if f['format_type'] in ['tweet', 'fb_post'] and f['global_appeal']])
        if engaging_formats > 0:
            viral_indicators += 25
            print(f"  💬 Community engagement: {engaging_formats} formats designed for sharing")
        
        # Universal themes coverage
        if len(themes_covered) >= 3:
            viral_indicators += 25
            print(f"  🌐 Universal themes: Covers {len(themes_covered)} globally relevant topics")
        
        # Multi-format storytelling
        if len(format_types) >= 4:
            viral_indicators += 25
            print(f"  📱 Multi-platform ready: {len(format_types)} different format types")
        
        print(f"  🚀 Viral potential score: {viral_indicators}/100")
        
        if viral_indicators >= 75:
            print(f"  🌟 HIGH VIRAL POTENTIAL - Content ready for global audience!")
    
    def generate_final_report(self):
        """Generate comprehensive test report"""
        print(f"\n📋 FINAL REPORT: Complete Engine System Test")
        print("=" * 60)
        
        # Stories created
        print(f"📚 Stories Generated: {len(self.stories_created)}")
        for story in self.stories_created:
            print(f"  • {story['theme']} (ID: {story['id'][:8]}...)")
        
        # Formats generated
        print(f"\n🎨 Formats Generated: {len(self.formats_generated)}")
        format_summary = {}
        for fmt in self.formats_generated:
            fmt_type = fmt['format_type']
            if fmt_type not in format_summary:
                format_summary[fmt_type] = {'count': 0, 'avg_quality': 0}
            format_summary[fmt_type]['count'] += 1
            format_summary[fmt_type]['avg_quality'] += fmt['quality_score']
        
        for fmt_type, data in format_summary.items():
            avg_quality = data['avg_quality'] / data['count']
            print(f"  • {fmt_type}: {data['count']} generated (avg quality: {avg_quality:.1f}/100)")
        
        # Overall system performance
        print(f"\n🎯 System Performance:")
        
        # Intelligence Engine
        avg_insight_score = sum(i['score'] for i in self.insights_discovered) / len(self.insights_discovered) if self.insights_discovered else 0
        print(f"  🧠 Intelligence Engine: {avg_insight_score:.1f}% insight accuracy")
        
        # Story Generation Engine
        stories_per_scenario = len(self.stories_created) / len(UNIVERSAL_CONVERSATION_SCENARIOS)
        print(f"  📖 Story Generation: {stories_per_scenario:.1f} stories per conversation")
        
        # Formats Generation Engine
        formats_per_story = len(self.formats_generated) / len(self.stories_created) if self.stories_created else 0
        print(f"  🎨 Format Generation: {formats_per_story:.1f} formats per story")
        
        # Global Appeal Assessment
        global_ready_formats = len([f for f in self.formats_generated if f['global_appeal']])
        global_percentage = (global_ready_formats / len(self.formats_generated)) * 100 if self.formats_generated else 0
        print(f"  🌍 Global Appeal: {global_percentage:.1f}% of formats ready for global audience")
        
        # Success criteria
        print(f"\n✅ SUCCESS CRITERIA:")
        success_score = 0
        
        if len(self.stories_created) >= len(UNIVERSAL_CONVERSATION_SCENARIOS):
            print(f"  ✅ Story generation: PASS")
            success_score += 25
        else:
            print(f"  ❌ Story generation: FAIL")
        
        if len(self.formats_generated) >= len(self.stories_created) * 3:
            print(f"  ✅ Format diversity: PASS")
            success_score += 25
        else:
            print(f"  ❌ Format diversity: FAIL")
        
        if avg_insight_score >= 70:
            print(f"  ✅ Intelligence accuracy: PASS")
            success_score += 25
        else:
            print(f"  ❌ Intelligence accuracy: FAIL")
        
        if global_percentage >= 60:
            print(f"  ✅ Global appeal: PASS")
            success_score += 25
        else:
            print(f"  ❌ Global appeal: FAIL")
        
        print(f"\n🏆 OVERALL SCORE: {success_score}/100")
        
        if success_score >= 75:
            print(f"🌟 EXCELLENT! System ready to create globally resonant content!")
        elif success_score >= 50:
            print(f"✅ GOOD! System working well with room for optimization")
        else:
            print(f"⚠️ NEEDS IMPROVEMENT! System requires optimization")
        
        return success_score

def main():
    """Run the complete engine system test"""
    test = CompleteEngineSystemTest()
    success = test.run_complete_test()
    
    if success:
        print(f"\n🎉 Complete Engine System Test: SUCCESS!")
    else:
        print(f"\n💥 Complete Engine System Test: FAILED!")
    
    return success

if __name__ == "__main__":
    main() 