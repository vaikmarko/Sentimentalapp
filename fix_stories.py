#!/usr/bin/env python3
"""Simple script to replace short conversations with longer ones and generate better stories"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def main():
    print("🔧 FIXING STORIES WITH LONGER CONVERSATIONS")
    print("=" * 50)
    
    # Step 1: Delete all existing stories
    print("1️⃣ Deleting existing stories...")
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        stories = response.json()
        for story in stories:
            try:
                requests.delete(f"{BASE_URL}/api/stories/{story['id']}")
                print(f"   🗑️  Deleted: {story['title']}")
            except:
                pass
    
    # Step 2: Create longer conversations and generate stories
    users = [
        {
            'id': 'maya_deep_thinker',
            'name': 'Maya Rodriguez',
            'conversation': create_maya_conversation()
        },
        {
            'id': 'jack_social_butterfly',
            'name': 'Jack Chen', 
            'conversation': create_jack_conversation()
        },
        {
            'id': 'riley_creative_soul',
            'name': 'Riley Kim',
            'conversation': create_riley_conversation()
        }
    ]
    
    print(f"\n2️⃣ Creating stories from longer conversations...")
    
    for i, user in enumerate(users, 1):
        print(f"\n📚 Processing {i}: {user['name']}")
        
        # Store conversation
        conversation_data = {
            'user_id': user['id'],
            'messages': user['conversation'],
            'scenario': f"Rich conversation for {user['name']}"
        }
        
        response = requests.post(f"{BASE_URL}/api/debug/store-conversation", json=conversation_data)
        if response.status_code == 200:
            print(f"   ✅ Conversation stored")
        else:
            print(f"   ❌ Failed to store conversation")
            continue
        
        # Generate story by sending final message
        time.sleep(2)
        final_message = "I'd like to reflect on our conversation and create a story from it."
        
        response = requests.post(
            f"{BASE_URL}/api/chat/message",
            json={
                'message': final_message,
                'user_id': user['id'],
                'force_story_creation': True
            },
            headers={'X-User-ID': user['id']}
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            if result.get('story_created'):
                print(f"   ✅ Story created: {result.get('story_id')}")
            else:
                print(f"   ⚠️  Story generation triggered")
        else:
            print(f"   ❌ Failed to generate story")
        
        time.sleep(3)
    
    # Step 3: Check results
    print(f"\n3️⃣ Final Results:")
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        stories = response.json()
        print(f"✅ Total stories: {len(stories)}")
        for story in stories:
            word_count = len(story.get('content', '').split())
            print(f"   📖 \"{story['title']}\" ({word_count} words)")
    else:
        print(f"❌ Failed to get stories")

def create_maya_conversation():
    """Maya's quarter-life crisis - much longer conversation"""
    return [
        {"role": "user", "content": "I've been feeling so lost lately. I graduated college two years ago and still have no idea what I'm doing with my life."},
        {"role": "assistant", "content": "That uncertainty can feel overwhelming. What aspects of feeling lost are weighing on you most right now?"},
        {"role": "user", "content": "Everyone else seems to have their life figured out. My friends are getting promotions, buying houses, getting engaged. I'm still working this random office job that has nothing to do with my degree."},
        {"role": "assistant", "content": "It sounds like you're comparing your internal experience to others' external achievements. What did you imagine your life would look like at this point?"},
        {"role": "user", "content": "I thought I'd be passionate about something by now. In college, I was sure I wanted to be a teacher. But student teaching showed me I hated the classroom management and dealing with administration."},
        {"role": "assistant", "content": "That's a significant realization. What parts of teaching did you enjoy?"},
        {"role": "user", "content": "I loved the one-on-one moments with students. When you could see something click for them, or when they'd come to me with problems. I liked being someone they could trust."},
        {"role": "assistant", "content": "Those meaningful connections seem really important to you. Have you found ways to have similar impacts in other contexts?"},
        {"role": "user", "content": "Actually, yes. I volunteer at a community center on weekends, helping adults with GED prep. It's completely different energy - these people chose to be there, they want to learn."},
        {"role": "assistant", "content": "That sounds incredibly fulfilling. What does that volunteer experience tell you about what you value in work?"},
        {"role": "user", "content": "I need to feel like I'm actually helping people, not just going through motions. And I need autonomy - I hate being micromanaged. The community center lets me teach however works best for each person."},
        {"role": "assistant", "content": "Those are important insights about your values. What would it look like to find work that honors those needs?"},
        {"role": "user", "content": "I've been thinking about social work or nonprofit management. But I'm scared of more debt when I already have student loans. What if I hate that too?"},
        {"role": "assistant", "content": "Fear of making the 'wrong' choice again makes sense. What small steps could you take to explore these fields?"},
        {"role": "user", "content": "I could shadow some social workers, or look into nonprofit jobs that don't require a master's degree. The community center director mentioned creating a coordinator position."},
        {"role": "assistant", "content": "That sounds practical. What feels scariest about potentially making a career change?"},
        {"role": "user", "content": "Disappointing my parents. They're immigrants who sacrificed so much for my education. They see teaching as stable and respectable. If I tell them I want to work at a community center..."},
        {"role": "assistant", "content": "Their expectations come from love and their experiences with security. How might you help them understand what fulfillment means to you?"},
        {"role": "user", "content": "Maybe I need to show them rather than tell them. If I can prove this work makes me happy and successful in my own way... They want me to be happy, they just define success differently."},
        {"role": "assistant", "content": "That's a mature perspective. What would success look like to you in five years?"},
        {"role": "user", "content": "Waking up excited about work most days. Having enough money to live comfortably. Making a real difference in people's lives. Maybe running my own program eventually. Feeling proud of my path, even if it's not traditional."}
    ]

def create_jack_conversation():
    """Jack's friendship authenticity struggle"""
    return [
        {"role": "user", "content": "I'm dealing with serious friend drama. My best friend since high school basically called me fake to my face."},
        {"role": "assistant", "content": "That must have been really hurtful to hear. What led to that conversation?"},
        {"role": "user", "content": "We were at a party last weekend, and I was being my usual social self - talking to everyone, making jokes, being the life of the party. Later she said I was 'performing' and asked why I can't just be real."},
        {"role": "assistant", "content": "How did that land for you when she said that?"},
        {"role": "user", "content": "It crushed me. That IS me being real. I genuinely enjoy meeting people and making them laugh. But then I started second-guessing everything. Am I actually fake?"},
        {"role": "assistant", "content": "It sounds like her comment made you question your authentic self. What feels true about how you show up in social situations?"},
        {"role": "user", "content": "I do get energy from making people happy. When someone laughs at my joke or I help someone feel included, that genuinely makes me feel good. But Sarah's always been more introverted. Maybe she doesn't get it."},
        {"role": "assistant", "content": "Different people express authenticity in different ways. What do you think Sarah means when she talks about being 'real'?"},
        {"role": "user", "content": "She only talks when she has something meaningful to say. She hates small talk, rolls her eyes at 'surface-level interactions.' For her, being real means sharing deep thoughts, not chatting about weekend plans."},
        {"role": "assistant", "content": "It sounds like you have different styles of connecting. Have there been times when you've felt pressure to be different than you naturally are?"},
        {"role": "user", "content": "Actually, yes. Around Sarah and her friends, I tone myself down. They're all intellectual and serious, and sometimes I feel like my humor is too much. So I try to match their energy."},
        {"role": "assistant", "content": "That's an interesting observation. How does it feel when you're adjusting yourself in those situations?"},
        {"role": "user", "content": "Exhausting. I spend the whole time monitoring myself - is this too loud? Too silly? Am I talking too much? It's like walking on eggshells."},
        {"role": "assistant", "content": "There's a difference between being considerate and completely suppressing your natural way of being. What happens when you're with friends who appreciate your full personality?"},
        {"role": "user", "content": "I feel alive! Last month at my coworker's birthday party, I didn't know anyone. By the end of the night, I had three new Instagram friends and plans to go rock climbing. Everyone was laughing and I felt like myself."},
        {"role": "assistant", "content": "That sounds energizing. What does that tell you about the friendships that work best for you?"},
        {"role": "user", "content": "Maybe I need friends who celebrate my social side instead of making me feel like it's a character flaw. I value deep conversations too, but I shouldn't have to choose between being social and being authentic."},
        {"role": "assistant", "content": "That's a powerful realization. How might this change how you approach your friendship with Sarah?"},
        {"role": "user", "content": "I think I need an honest conversation with her. Tell her that calling me fake really hurt, and explain that my social personality isn't a performance - it's genuinely who I am."},
        {"role": "assistant", "content": "That takes courage. What have you learned about yourself through this situation?"},
        {"role": "user", "content": "That I'd rather be genuinely liked for who I am than fake-liked for who I'm pretending to be. My social energy isn't something to apologize for - it's one of my strengths. I make people feel welcome and included. That's valuable."}
    ]

def create_riley_conversation():
    """Riley's creative block and artistic struggle"""
    return [
        {"role": "user", "content": "I haven't created anything meaningful in months and it's killing me. I used to paint every day, but now I just stare at blank canvases."},
        {"role": "assistant", "content": "Creative blocks can feel devastating when art is such an important part of who you are. What do you think changed?"},
        {"role": "user", "content": "It started when I got rejected from a gallery show I really wanted. The curator said my work was 'technically proficient but lacks emotional depth.' I can't stop thinking about that phrase."},
        {"role": "assistant", "content": "That must have been difficult feedback to receive. How has it affected the way you approach your art?"},
        {"role": "user", "content": "Now every time I pick up a brush, I hear those words. I start second-guessing every stroke, wondering if it's deep enough, meaningful enough. I've started and abandoned fifteen paintings."},
        {"role": "assistant", "content": "It sounds like you're putting enormous pressure on each piece to be profound. What was your relationship with painting like before this feedback?"},
        {"role": "user", "content": "It was my escape, my meditation. I'd lose hours exploring color and texture. I painted landscapes, still lifes, abstract pieces - whatever felt right. Some were terrible, some okay, a few actually pretty good."},
        {"role": "assistant", "content": "That sounds like a much more organic relationship with creativity. What made those 'pretty good' pieces special?"},
        {"role": "user", "content": "They came from somewhere real. Like this painting I did after my grandmother died - just deep blues and purples swirling together, nothing literal. But it captured exactly how grief felt to me."},
        {"role": "assistant", "content": "That painting sounds like it had deep emotional resonance. What was different about your process when you created it?"},
        {"role": "user", "content": "I wasn't trying to make 'art' with a capital A. I was just processing what I was feeling. I remember crying while painting it, getting paint on my face because I was so absorbed."},
        {"role": "assistant", "content": "There's something powerful about creating from necessity rather than obligation. What would it look like to reconnect with that sense of necessity?"},
        {"role": "user", "content": "Maybe I need to stop thinking about galleries and critics and just paint for myself again. But it's hard - once you start wanting external validation, it's difficult to ignore that voice."},
        {"role": "assistant", "content": "That tension between internal motivation and external validation is something many artists struggle with. What draws you to want that recognition?"},
        {"role": "user", "content": "I want to know my art matters to other people, not just me. I want to make a living from creativity someday. And honestly, I want to prove to everyone who said art wasn't a 'real career' that they were wrong."},
        {"role": "assistant", "content": "Those are understandable desires. How might you balance those longer-term goals with the immediate need to reconnect with your creative flow?"},
        {"role": "user", "content": "Maybe I could set aside times for 'practice painting' - work just for me, where I don't worry about being gallery-worthy. And other times for more intentional pieces I might want to show."},
        {"role": "assistant", "content": "That sounds like a way to protect your creative exploration. What would make the 'practice painting' feel safe?"},
        {"role": "user", "content": "Using cheaper materials so I don't feel precious about wasting them. I used to carry a tiny watercolor set everywhere for little studies. I stopped doing that because I decided it wasn't 'serious' enough."},
        {"role": "assistant", "content": "What would it mean to give yourself permission to value that spontaneous, alive feeling again?"},
        {"role": "user", "content": "Maybe that the journey is as important as the destination. Becoming a better artist means allowing myself to play and experiment, not just striving for masterpieces. The curator wanted emotional depth - maybe that comes from trusting my instincts, not overthinking everything."}
    ]

if __name__ == "__main__":
    main() 