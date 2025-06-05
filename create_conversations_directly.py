#!/usr/bin/env python3
"""Add long conversations directly to database and trigger story generation"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def create_conversations_and_stories():
    print("🗃️ ADDING CONVERSATIONS DIRECTLY TO DATABASE")
    print("=" * 50)
    
    # Clear existing stories first
    print("1️⃣ Clearing existing stories...")
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        existing_stories = response.json()
        for story in existing_stories:
            try:
                requests.delete(f"{BASE_URL}/api/stories/{story['id']}")
                print(f"   🗑️  Deleted: '{story['title']}'")
            except:
                pass
    
    # Create users with their conversations
    users_and_conversations = [
        {
            'user_id': 'maya_deep_thinker',
            'name': 'Maya Rodriguez',
            'email': 'maya.rodriguez@example.com',
            'conversation': create_maya_conversation(),
            'scenario': 'Quarter-life crisis and career uncertainty'
        },
        {
            'user_id': 'jack_social_butterfly', 
            'name': 'Jack Chen',
            'email': 'jack.chen@example.com',
            'conversation': create_jack_conversation(),
            'scenario': 'Friendship drama and authenticity struggles'
        },
        {
            'user_id': 'riley_creative_soul',
            'name': 'Riley Kim', 
            'email': 'riley.kim@example.com',
            'conversation': create_riley_conversation(),
            'scenario': 'Creative block and artistic self-doubt'
        },
        {
            'user_id': 'alex_ambitious_burnout',
            'name': 'Alex Rivera',
            'email': 'alex.rivera@example.com', 
            'conversation': create_alex_conversation(),
            'scenario': 'Work-life balance and relationship issues'
        },
        {
            'user_id': 'sam_anxious_achiever',
            'name': 'Sam Taylor',
            'email': 'sam.taylor@example.com',
            'conversation': create_sam_conversation(),
            'scenario': 'Impostor syndrome and family pressure'
        }
    ]
    
    print(f"2️⃣ Processing {len(users_and_conversations)} users with rich conversations...")
    
    for i, user_data in enumerate(users_and_conversations, 1):
        user_id = user_data['user_id']
        name = user_data['name']
        email = user_data['email']
        conversation = user_data['conversation']
        scenario = user_data['scenario']
        
        print(f"\n💬 Processing {i}: {name}")
        print(f"   📧 Email: {email}")
        print(f"   📖 Scenario: {scenario}")
        print(f"   💭 Messages: {len(conversation)} exchanges")
        
        # Register user
        user_registration = {
            'username': name,
            'email': email,
            'password': 'testpass123'
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/auth/register", json=user_registration)
            if response.status_code in [200, 201]:
                print(f"   ✅ User registered successfully")
            else:
                print(f"   ⚠️  User may already exist")
        except Exception as e:
            print(f"   ⚠️  Registration issue: {e}")
        
        # Store conversation directly in database using debug endpoint
        conversation_data = {
            'user_id': user_id,
            'messages': conversation,
            'scenario': scenario,
            'created_at': time.strftime('%Y-%m-%dT%H:%M:%S')
        }
        
        try:
            # Use the debug endpoint to store conversation directly
            response = requests.post(
                f"{BASE_URL}/api/debug/store-conversation",
                json=conversation_data
            )
            
            if response.status_code == 200:
                print(f"   ✅ Conversation stored in database")
            else:
                print(f"   ❌ Failed to store conversation: {response.status_code}")
                print(f"   📝 Response: {response.text}")
                continue
                
        except Exception as e:
            print(f"   ❌ Error storing conversation: {e}")
            continue
            
        # Small delay between users
        time.sleep(1)
    
    print(f"\n3️⃣ Now triggering story generation through chat messages...")
    
    # Now send a final message to each user to trigger story generation
    for user_data in users_and_conversations:
        user_id = user_data['user_id']
        name = user_data['name']
        
        try:
            print(f"\n📚 Triggering story for {name}...")
            
            # Send a final message that should trigger story creation
            final_message = "Thank you for this conversation. I'd love to reflect on what we've discussed."
            
            response = requests.post(
                f"{BASE_URL}/api/chat/message",
                json={
                    'message': final_message,
                    'user_id': user_id,
                    'force_story_creation': True
                },
                headers={'X-User-ID': user_id}
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                if result.get('story_created'):
                    print(f"   ✅ Story created! ID: {result.get('story_id')}")
                else:
                    print(f"   ⚠️  Story generation triggered, but no story ID returned")
            else:
                print(f"   ❌ Story generation failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error generating story: {e}")
        
        # Delay between story generations
        time.sleep(3)
    
    print(f"\n⏳ Waiting for all stories to be processed...")
    time.sleep(10)
    
    # Check final results
    print(f"\n📖 FINAL RESULTS:")
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        stories = response.json()
        print(f"✅ Generated {len(stories)} stories total")
        
        for story in stories:
            word_count = len(story.get('content', '').split())
            author = story.get('author', 'Unknown')
            title = story.get('title', 'Untitled')
            user_id = story.get('user_id', 'Unknown')
            print(f"   📚 \"{title}\" by {author} ({word_count} words) [User: {user_id}]")
            
        # Show stories from our new users specifically
        our_users = [data['user_id'] for data in users_and_conversations]
        our_stories = [s for s in stories if s.get('user_id') in our_users]
        print(f"\n🎯 Stories from our new conversations: {len(our_stories)}")
        
    else:
        print(f"❌ Failed to retrieve stories: {response.status_code}")

def create_maya_conversation():
    """Maya's deep quarter-life crisis conversation"""
    return [
        {"role": "user", "content": "I've been feeling so lost lately. I graduated college two years ago and still have no idea what I'm doing with my life."},
        {"role": "assistant", "content": "That uncertainty can feel overwhelming. What aspects of feeling lost are weighing on you most right now?"},
        {"role": "user", "content": "Everyone else seems to have their life figured out. My friends are getting promotions, buying houses, getting engaged. I'm still working this random office job that has nothing to do with my degree."},
        {"role": "assistant", "content": "It sounds like you're comparing your internal experience to others' external achievements. What did you imagine your life would look like at this point?"},
        {"role": "user", "content": "I thought I'd be passionate about something by now. In college, I was sure I wanted to be a teacher. But student teaching showed me I hated the classroom management and dealing with administration."},
        {"role": "assistant", "content": "That's a significant realization. It takes courage to acknowledge when something doesn't align with reality. What parts of teaching did you enjoy?"},
        {"role": "user", "content": "I loved the one-on-one moments with students. When you could see something click for them, or when they'd come to me with problems. I liked being someone they could trust."},
        {"role": "assistant", "content": "Those meaningful connections seem really important to you. Have you found ways to have similar impacts in other contexts?"},
        {"role": "user", "content": "Actually, yes. I volunteer at a community center on weekends, helping adults with GED prep. It's completely different energy - these people chose to be there, they want to learn."},
        {"role": "assistant", "content": "That sounds incredibly fulfilling. What does that volunteer experience tell you about what you value in work?"},
        {"role": "user", "content": "I need to feel like I'm actually helping people, not just going through motions. And I need autonomy - I hate being micromanaged. The community center lets me teach however works best for each person."},
        {"role": "assistant", "content": "Those are important insights about your values. What would it look like to find work that honors those needs?"},
        {"role": "user", "content": "I've been thinking about social work or nonprofit management. But I'm scared of more debt when I already have student loans. What if I hate that too?"},
        {"role": "assistant", "content": "Fear of making the 'wrong' choice again makes sense. What small steps could you take to explore these fields without committing to graduate school?"},
        {"role": "user", "content": "I could shadow some social workers, or look into nonprofit jobs that don't require a master's degree. The community center director mentioned creating a coordinator position."},
        {"role": "assistant", "content": "That sounds like a practical way to test your interests. What feels scariest about potentially making a career change?"},
        {"role": "user", "content": "Disappointing my parents. They're immigrants who sacrificed so much for my education. They see teaching as stable and respectable. If I tell them I want to work at a community center..."},
        {"role": "assistant", "content": "Their expectations come from love and their experiences with security. How might you help them understand what fulfillment means to you?"},
        {"role": "user", "content": "Maybe I need to show them rather than tell them. If I can prove this work makes me happy and successful in my own way... They want me to be happy, they just define success differently."},
        {"role": "assistant", "content": "That's a mature perspective. What would success look like to you in five years?"},
        {"role": "user", "content": "Waking up excited about work most days. Having enough money to live comfortably. Making a real difference in people's lives. Maybe running my own program eventually. Feeling proud of my path, even if it's not traditional."}
    ]

def create_jack_conversation():
    """Jack's friendship authenticity conversation"""
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
        {"role": "user", "content": "Exhausting. I spend the whole time monitoring myself - is this too loud? Too silly? Am I talking too much? It's like walking on eggshells. But I thought that's what friendship was - adapting to make others comfortable."},
        {"role": "assistant", "content": "There's a difference between being considerate and completely suppressing your natural way of being. What happens when you're with friends who appreciate your full personality?"},
        {"role": "user", "content": "I feel alive! Last month at my coworker's birthday party, I didn't know anyone. By the end of the night, I had three new Instagram friends and plans to go rock climbing. Everyone was laughing and I felt like myself."},
        {"role": "assistant", "content": "That sounds energizing and fulfilling. What does that tell you about the friendships that work best for you?"},
        {"role": "user", "content": "Maybe I need friends who celebrate my social side instead of making me feel like it's a character flaw. I value deep conversations too, but I shouldn't have to choose between being social and being authentic."},
        {"role": "assistant", "content": "That's a powerful realization. How might this change how you approach your friendship with Sarah?"},
        {"role": "user", "content": "I think I need an honest conversation with her. Tell her that calling me fake really hurt, and explain that my social personality isn't a performance - it's genuinely who I am. If she can't accept that, maybe we're growing in different directions."},
        {"role": "assistant", "content": "That takes courage. What would it mean for your friendship if you showed up as your full self?"},
        {"role": "user", "content": "Either it gets stronger because we're being honest, or we realize we're not as compatible as we thought. Both outcomes are better than pretending to be someone I'm not just to keep the peace."},
        {"role": "assistant", "content": "What have you learned about yourself through this situation?"},
        {"role": "user", "content": "That I'd rather be genuinely liked for who I am than fake-liked for who I'm pretending to be. My social energy isn't something to apologize for - it's one of my strengths. I make people feel welcome and included. That's valuable."}
    ]

def create_riley_conversation():
    """Riley's creative block conversation"""
    return [
        {"role": "user", "content": "I haven't created anything meaningful in months and it's killing me. I used to paint every day, but now I just stare at blank canvases."},
        {"role": "assistant", "content": "Creative blocks can feel devastating when art is such an important part of who you are. What do you think changed?"},
        {"role": "user", "content": "It started when I got rejected from a gallery show I really wanted. The curator said my work was 'technically proficient but lacks emotional depth.' I can't stop thinking about that phrase."},
        {"role": "assistant", "content": "That must have been difficult feedback to receive. How has it affected the way you approach your art?"},
        {"role": "user", "content": "Now every time I pick up a brush, I hear those words. I start second-guessing every stroke, wondering if it's deep enough, meaningful enough. I've started and abandoned fifteen paintings because none feel important enough."},
        {"role": "assistant", "content": "It sounds like you're putting enormous pressure on each piece to be profound. What was your relationship with painting like before this feedback?"},
        {"role": "user", "content": "It was my escape, my meditation. I'd lose hours exploring color and texture. I painted landscapes, still lifes, abstract pieces - whatever felt right. Some were terrible, some okay, a few actually pretty good."},
        {"role": "assistant", "content": "That sounds like a much more organic relationship with creativity. What made those 'pretty good' pieces special?"},
        {"role": "user", "content": "They came from somewhere real. Like this painting I did after my grandmother died - just deep blues and purples swirling together, nothing literal. But it captured exactly how grief felt to me. My family still talks about that one."},
        {"role": "assistant", "content": "That painting sounds like it had deep emotional resonance. What was different about your process when you created it?"},
        {"role": "user", "content": "I wasn't trying to make 'art' with a capital A. I was just processing what I was feeling. I remember crying while painting it, getting paint on my face because I was so absorbed. It felt necessary, not optional."},
        {"role": "assistant", "content": "There's something powerful about creating from necessity rather than obligation. What would it look like to reconnect with that sense of necessity?"},
        {"role": "user", "content": "Maybe I need to stop thinking about galleries and critics and just paint for myself again. But it's hard - once you start wanting external validation, it's difficult to ignore that voice."},
        {"role": "assistant", "content": "That tension between internal motivation and external validation is something many artists struggle with. What draws you to want that recognition?"},
        {"role": "user", "content": "I want to know my art matters to other people, not just me. I want to make a living from creativity someday. And honestly, I want to prove to everyone who said art wasn't a 'real career' that they were wrong."},
        {"role": "assistant", "content": "Those are understandable desires. How might you balance those longer-term goals with the immediate need to reconnect with your creative flow?"},
        {"role": "user", "content": "Maybe I could set aside times for 'practice painting' - work just for me, where I don't worry about being gallery-worthy. And other times for more intentional pieces I might want to show."},
        {"role": "assistant", "content": "That sounds like a way to protect your creative exploration while working toward professional goals. What would make the 'practice painting' feel safe?"},
        {"role": "user", "content": "Using cheaper materials so I don't feel precious about wasting them. Or painting in sketchbooks instead of canvases. I used to carry a tiny watercolor set everywhere for little studies. I stopped doing that."},
        {"role": "assistant", "content": "What happened to that practice?"},
        {"role": "user", "content": "I decided it wasn't 'serious' enough. I thought I needed to work big and bold to be taken seriously. But those little studies were some of my favorite work. They felt spontaneous and alive."},
        {"role": "assistant", "content": "What would it mean to give yourself permission to value that spontaneous, alive feeling again?"},
        {"role": "user", "content": "Maybe that the journey is as important as the destination. Becoming a better artist means allowing myself to play and experiment, not just striving for masterpieces. The curator wanted emotional depth - maybe that comes from trusting my instincts, not overthinking everything."}
    ]

def create_alex_conversation():
    """Alex's burnout conversation"""
    return [
        {"role": "user", "content": "I think I'm burning out and I don't know how to stop. I've been working 70-hour weeks for months and my relationship is falling apart."},
        {"role": "assistant", "content": "That sounds incredibly overwhelming. What's driving the long hours right now?"},
        {"role": "user", "content": "I got promoted to team lead six months ago and feel like I have to prove I deserve it. My boss keeps loading more projects on my plate, and I can't say no. Plus half my team is new, so I'm constantly training people."},
        {"role": "assistant", "content": "It sounds like you're taking on multiple roles - your work, management, and training. What happens when you consider delegating or setting boundaries?"},
        {"role": "user", "content": "I tell myself I will, but then I see how much the new people struggle and it's faster to just do it myself. My boss says things like 'I know I can count on you' and 'you're the only one who gets our vision.' It feels impossible to disappoint him."},
        {"role": "assistant", "content": "That recognition feels good, but it sounds like it's also trapping you. What's the cost of being indispensable?"},
        {"role": "user", "content": "My girlfriend and I barely see each other anymore. When I get home, I'm exhausted and irritable. She tried to plan a weekend trip for our anniversary and I had to cancel because of a client emergency. She was so hurt."},
        {"role": "assistant", "content": "How did that conversation go?"},
        {"role": "user", "content": "Not well. She said she feels like she's dating my job, not me. That stung because work used to be something I was passionate about, but now it feels like this monster consuming everything else."},
        {"role": "assistant", "content": "What was your relationship with work like before this promotion?"},
        {"role": "user", "content": "I loved it! I was a senior developer solving interesting problems all day. I had clear deliverables, and when I finished, I was done. I had hobbies - played guitar, went hiking, cooked elaborate meals for my girlfriend."},
        {"role": "assistant", "content": "That sounds like a much more balanced life. What's different about the management role that makes boundaries harder?"},
        {"role": "user", "content": "Everything feels urgent and like my responsibility. When someone on my team struggles, their stress becomes my stress. When clients are unhappy, that's on me. My boss has an open-door policy that basically means I'm available 24/7."},
        {"role": "assistant", "content": "You've taken on a lot of emotional responsibility for things that might not entirely be within your control. What would change if you saw your role differently?"},
        {"role": "user", "content": "What do you mean?"},
        {"role": "assistant", "content": "Instead of being responsible for preventing all problems and stress, what if your job was to help people solve problems and manage stress?"},
        {"role": "user", "content": "That's... actually really different. Like, instead of taking on their problems, I'd be teaching them how to handle problems themselves. But what if they fail? What if projects don't get done right?"},
        {"role": "assistant", "content": "What happens long term if you continue doing everything yourself versus investing time in developing your team's capabilities?"},
        {"role": "user", "content": "If I keep doing everything myself, I'll definitely burn out. Probably quit or get fired for being impossible to work with. If I train my team properly... it might be rocky at first, but eventually I'd have a team that doesn't need me to micromanage everything."},
        {"role": "assistant", "content": "That sounds more sustainable. What would you need to make that shift?"},
        {"role": "user", "content": "I'd need to get comfortable with things not being perfect right away. And I'd need to talk with my boss about realistic expectations. Maybe propose a timeline for transitioning to a more autonomous team structure."},
        {"role": "assistant", "content": "What feels most challenging about having that conversation?"},
        {"role": "user", "content": "Admitting I can't handle everything. I've built this reputation as the person who gets things done, and I'm afraid if I set boundaries, they'll think I'm not committed or capable."},
        {"role": "assistant", "content": "What would a truly capable leader do in this situation?"},
        {"role": "user", "content": "A capable leader would build systems that don't depend entirely on them. They'd develop their team and create sustainable processes. They'd probably work normal hours and still deliver great results because they built something bigger than just their individual effort."},
        {"role": "assistant", "content": "That sounds like leadership worth aspiring to. What's one small step you could take this week toward that vision?"},
        {"role": "user", "content": "I could stop checking email after 8 PM. Maybe schedule dedicated training time instead of just fixing problems as they come up. Actually... I should probably have a serious conversation with my girlfriend too. She deserves to know I'm working on this."}
    ]

def create_sam_conversation():
    """Sam's impostor syndrome conversation"""
    return [
        {"role": "user", "content": "I got into medical school and instead of being excited, I'm terrified they're going to realize they made a mistake accepting me."},
        {"role": "assistant", "content": "That's such a huge accomplishment - congratulations! What's making you feel like you don't belong there?"},
        {"role": "user", "content": "Everyone else seems so much smarter and more prepared. In our pre-orientation group chat, people are talking about research they've published and volunteer work in other countries. I feel like such a fraud."},
        {"role": "assistant", "content": "It sounds like you're comparing your internal doubts to other people's highlight reels. What did you bring to your application that got you accepted?"},
        {"role": "user", "content": "I had good grades and test scores. I volunteered at a free clinic for two years. But nothing as impressive as what these other people are doing. My parents keep telling everyone their daughter is going to be a doctor, and I'm scared I'll disappoint them."},
        {"role": "assistant", "content": "There's a lot of pressure in that expectation. What drew you to medicine in the first place?"},
        {"role": "user", "content": "I've wanted to be a doctor since I was eight. My little brother has diabetes, and I watched how the doctors at the children's hospital took care of him. They were so knowledgeable and compassionate. I wanted to help families like mine."},
        {"role": "assistant", "content": "That's a powerful motivation. How does that eight-year-old's dream connect to where you are now?"},
        {"role": "user", "content": "I guess I've lost sight of that. Somewhere along the way, it became more about achieving and proving myself than actually helping people. The pressure to be perfect has been overwhelming."},
        {"role": "assistant", "content": "When did that shift happen for you?"},
        {"role": "user", "content": "Probably in high school when I realized how competitive pre-med would be. My parents started monitoring my grades obsessively, asking about everyone else's test scores. It became less about learning and more about being the best."},
        {"role": "assistant", "content": "That sounds exhausting. How has that pressure affected your relationship with learning?"},
        {"role": "user", "content": "I study constantly but never feel like I know enough. Even when I ace an exam, I'm already worried about the next one. I can't enjoy my successes because I'm always focused on what I might fail at next."},
        {"role": "assistant", "content": "What would it look like to study from curiosity rather than fear?"},
        {"role": "user", "content": "I actually remember that feeling! In my anatomy class last year, there was this lecture about how the heart develops in utero. It was so fascinating that I went down a rabbit hole reading research papers for hours, not because I had to, but because I wanted to understand."},
        {"role": "assistant", "content": "What was different about that experience?"},
        {"role": "user", "content": "I wasn't thinking about grades or competition. I was just genuinely amazed by how complex and elegant the human body is. I felt like I was discovering something magical instead of cramming information into my brain."},
        {"role": "assistant", "content": "That sense of wonder sounds like it connects back to what originally drew you to medicine. How might you cultivate more of that feeling?"},
        {"role": "user", "content": "Maybe I need to remember that everyone in my med school class is there because they earned it, including me. We're all learning together. It doesn't have to be competition - we could actually help each other."},
        {"role": "assistant", "content": "What would change if you approached medical school as collaboration rather than competition?"},
        {"role": "user", "content": "I'd probably learn better. I've always understood things better when I can discuss them with other people. And I'd be less stressed if I wasn't constantly comparing myself to everyone else."},
        {"role": "assistant", "content": "How do you think your family would respond if you shared some of these feelings with them?"},
        {"role": "user", "content": "My parents mean well, but they see my achievements as validation of their sacrifices. They immigrated here so I could have opportunities they never had. When I succeed, it feels like proof that it was all worth it."},
        {"role": "assistant", "content": "That's a lot of weight to carry. What would it mean to honor their sacrifices while also taking care of your own well-being?"},
        {"role": "user", "content": "Maybe succeeding isn't just about grades and accolades. Maybe it's about becoming the kind of doctor they'd be proud of - one who genuinely cares about patients and never stops learning. That might matter more than being at the top of my class."},
        {"role": "assistant", "content": "What kind of doctor do you want to become?"},
        {"role": "user", "content": "Someone like the doctors who took care of my brother. They were brilliant, yes, but they were also kind. They took time to explain things to my scared parents. They saw my brother as a whole person, not just a medical case. If I can become that kind of doctor, then I'll have truly succeeded."},
        {"role": "assistant", "content": "That sounds like a meaningful definition of success. How does that change how you think about starting medical school?"},
        {"role": "user", "content": "It makes it feel less scary. Instead of worrying about proving I belong there, I can focus on becoming the person I want to be. The skills will come, the knowledge will come, but the compassion - that's something I can start practicing right now."}
    ]

if __name__ == "__main__":
    try:
        create_conversations_and_stories()
    except KeyboardInterrupt:
        print("\n👋 Process interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc() 