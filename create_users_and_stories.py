#!/usr/bin/env python3
import requests
import time

BASE_URL = "http://localhost:8080"

# Users with their story content
USERS_AND_STORIES = [
    {
        'user_id': 'maya_deep_thinker',
        'name': 'Maya Rodriguez',
        'email': 'maya@example.com',
        'title': 'Finding My Own Path',
        'content': '''Maya stared at her computer screen, the cursor blinking mockingly in the empty job application field. Two years out of college and she still felt like she was playing dress-up in someone else's life.

"Everyone else has it figured out," she whispered to herself, scrolling through LinkedIn updates of friends getting promotions, buying houses, announcing engagements. Meanwhile, she was still at this random office job that had nothing to do with her education degree.

The teaching dream had crumbled during student teaching. She'd loved the one-on-one moments - seeing understanding dawn in a student's eyes, being someone they trusted with their problems. But the classroom management, the endless administrative tasks, the feeling of being trapped in a system that didn't value actual learning... it had suffocated her.

But weekends at the community center were different. Helping adults with GED prep, watching these determined faces who'd chosen to be there, who wanted to learn - it filled something in her she didn't know was empty. The director had even mentioned creating a coordinator position.

"I need to feel like I'm actually helping people," Maya realized, speaking to her reflection in the darkened window. "And I need autonomy. I hate being micromanaged."

The scariest part wasn't even the potential career change. It was disappointing her immigrant parents who'd sacrificed everything for her education. They saw teaching as stable, respectable. A community center job? That would be harder to explain.

But maybe success wasn't about meeting others' definitions. Maybe it was about waking up excited about work, making a real difference, feeling proud of her own path - even if it wasn't traditional. Maybe she could show them rather than tell them what fulfillment really meant.'''
    },
    {
        'user_id': 'jack_social_butterfly',
        'name': 'Jack Chen',
        'email': 'jack@example.com',
        'title': 'The Authentic Self',
        'content': '''Jack's chest still ached from Sarah's words: "You're always performing. Why can't you just be real?"

The party had been going perfectly. He'd been his usual self - talking to everyone, making jokes, being the connector who helped quiet people feel included. He genuinely loved making others laugh, seeing their faces light up. That energy was as real as breathing to him.

But Sarah, his best friend since high school, had pulled him aside with that look of disappointment he'd grown to dread. Her crowd was different - intellectual, serious, the type who rolled their eyes at small talk and only spoke when they had something "meaningful" to say.

Around them, Jack found himself monitoring every word. Was he being too loud? Too silly? Too much? The effort was exhausting, like walking on eggshells while suppressing his natural way of being.

But at his coworker's birthday party last month, when he'd known no one, he'd felt alive. By night's end, he had three new friends and rock climbing plans. Everyone had been laughing, and he'd felt completely himself.

"That IS me being real," he said aloud, the realization hitting him. His social energy wasn't a character flaw - it was a strength. He made people feel welcome and included. That was valuable.

Sarah's version of authenticity - deep thoughts over weekend plans, meaningful silence over connection - that was her way, not the only way.

He decided he'd rather be genuinely liked for who he was than fake-liked for who he was pretending to be. Some friendships celebrated his full personality. Maybe it was time to find more of those, and have an honest conversation with the ones that didn't.'''
    },
    {
        'user_id': 'riley_creative_soul',
        'name': 'Riley Kim',
        'email': 'riley@example.com',
        'title': 'The Canvas of Fear',
        'content': '''Riley's paintbrush trembled above the blank canvas, the curator's words echoing in her mind: "Technically proficient but lacks emotional depth."

Four months since that rejection, and she hadn't completed a single piece. Fifteen started, fifteen abandoned. Each brushstroke felt like a judgment, each color choice scrutinized by imaginary critics asking "Is this deep enough? Meaningful enough?"

Before that devastating feedback, painting had been her meditation, her escape. She'd lose hours exploring texture and color, creating landscapes, still lifes, abstract pieces - whatever felt right. Some terrible, some okay, a few genuinely good.

Like the painting after her grandmother's death - deep blues and purples swirling together, nothing literal, but capturing exactly how grief felt. She remembered crying while painting it, getting paint on her face because she was so absorbed.

"I wasn't trying to make 'art' with a capital A," she whispered to the empty studio. "I was just processing what I was feeling."

The hunger for external validation had poisoned the well. She wanted her art to matter to others, wanted to make a living from creativity, wanted to prove wrong everyone who'd said art wasn't a "real career."

But maybe the curator had been wrong about depth. Maybe emotional depth came from trusting her instincts, not overthinking everything. Maybe she needed to return to "practice painting" - cheap materials, no pressure, just the pure joy of creation.

She picked up her tiny watercolor set, abandoned because it wasn't "serious" enough. Perhaps the journey was as important as the destination. Perhaps allowing herself to play and experiment was exactly what would lead to the depth everyone was looking for.

The first brushstroke felt like coming home.'''
    }
]

def register_user(user_data):
    """Register a user"""
    print(f"👤 Registering {user_data['name']}...")
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json={
        'email': user_data['email'],
        'name': user_data['name'],
        'user_id': user_data['user_id']
    })
    
    if response.status_code in [200, 201]:
        print(f"   ✅ User registered")
        return True
    else:
        print(f"   ⚠️  Registration response: {response.status_code}")
        return True  # Might already exist

def create_story(user_data):
    """Create a story for a user"""
    print(f"📚 Creating story for {user_data['name']}...")
    
    story_data = {
        'title': user_data['title'],
        'content': user_data['content'],
        'author': user_data['name']
    }
    
    response = requests.post(f"{BASE_URL}/api/stories", 
        json=story_data,
        headers={'X-User-ID': user_data['user_id']}
    )
    
    if response.status_code in [200, 201]:
        print(f"   ✅ Story created")
        return True
    else:
        print(f"   ❌ Failed: {response.status_code}")
        try:
            error = response.json()
            print(f"      Error: {error.get('error', 'Unknown')}")
        except:
            pass
        return False

def main():
    print("🚀 CREATING USERS AND THEIR STORIES")
    print("=" * 40)
    
    # Clear existing stories
    print("1️⃣ Clearing existing stories...")
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        for story in response.json():
            try:
                requests.delete(f"{BASE_URL}/api/stories/{story['id']}")
            except:
                pass
    
    print(f"\n2️⃣ Processing {len(USERS_AND_STORIES)} users...")
    
    success_count = 0
    for i, user_data in enumerate(USERS_AND_STORIES, 1):
        print(f"\n{i}. {user_data['name']}")
        
        # Register user
        register_user(user_data)
        time.sleep(1)
        
        # Create story
        if create_story(user_data):
            success_count += 1
        
        time.sleep(2)
    
    # Check results
    print(f"\n3️⃣ Final Results:")
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        stories = response.json()
        print(f"✅ Stories created: {len(stories)}")
        for story in stories:
            word_count = len(story.get('content', '').split())
            print(f"   📖 \"{story.get('title', 'Untitled')}\" ({word_count} words)")
    
    print(f"\n🎊 Success rate: {success_count}/{len(USERS_AND_STORIES)}")

if __name__ == "__main__":
    main() 