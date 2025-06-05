#!/usr/bin/env python3
"""Create longer, more engaging conversations for rich story generation"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def create_long_engaging_conversations():
    print("📚 CREATING LONGER, MORE ENGAGING CONVERSATIONS")
    print("=" * 55)
    
    # First, clear existing short stories
    print("1️⃣ Clearing existing short stories...")
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        existing_stories = response.json()
        for story in existing_stories:
            user_id = story.get('user_id')
            if user_id and user_id != 'test_user_debug':
                try:
                    requests.delete(f"{BASE_URL}/api/stories/{story['id']}", headers={'X-User-ID': user_id})
                    print(f"   🗑️  Deleted: '{story['title']}'")
                except:
                    pass
    
    # Create new users with distinct personalities
    users = [
        {
            'id': 'deep_thinker_maya',
            'name': 'Maya Rodriguez',
            'email': 'maya.r@example.com',
            'personality': 'introspective, analytical, philosophical',
            'age': 24,
            'scenario': 'quarter-life crisis and career uncertainty'
        },
        {
            'id': 'social_butterfly_jack',
            'name': 'Jack Chen',
            'email': 'jack.c@example.com', 
            'personality': 'outgoing, relationship-focused, emotionally expressive',
            'age': 22,
            'scenario': 'navigating friendship drama and authenticity'
        },
        {
            'id': 'creative_soul_riley',
            'name': 'Riley Kim',
            'email': 'riley.k@example.com',
            'personality': 'artistic, sensitive, perfectionist',
            'age': 26,
            'scenario': 'creative block and self-doubt'
        },
        {
            'id': 'ambitious_alex',
            'name': 'Alex Rivera',
            'email': 'alex.r@example.com',
            'personality': 'driven, ambitious, struggling with burnout',
            'age': 28,
            'scenario': 'work-life balance and relationship issues'
        },
        {
            'id': 'anxious_achiever_sam',
            'name': 'Sam Taylor',
            'email': 'sam.t@example.com',
            'personality': 'high-achieving, anxious, people-pleaser',
            'age': 25,
            'scenario': 'impostor syndrome and family pressure'
        }
    ]
    
    print(f"2️⃣ Creating {len(users)} users with distinct personalities...")
    
    # Register users
    for user in users:
        user_data = {
            'username': user['name'],
            'email': user['email'],
            'password': 'testpass123'
        }
        try:
            response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
            if response.status_code in [200, 201]:
                print(f"   ✅ Created: {user['name']} ({user['personality']})")
        except:
            print(f"   ⚠️  {user['name']} may already exist")
    
    print(f"\n3️⃣ Creating long, engaging conversations...")
    
    # Create much longer, more engaging conversations
    conversations = [
        {
            'user': users[0],  # Maya - deep thinker
            'conversation': create_deep_philosophical_conversation(),
            'title': 'Finding My Direction in the Quarter-Life Maze'
        },
        {
            'user': users[1],  # Jack - social butterfly
            'conversation': create_friendship_drama_conversation(),
            'title': 'Learning Who My Real Friends Are'
        },
        {
            'user': users[2],  # Riley - creative soul
            'conversation': create_creative_struggle_conversation(), 
            'title': 'When Your Art Feels Like It\'s Not Enough'
        },
        {
            'user': users[3],  # Alex - ambitious
            'conversation': create_burnout_conversation(),
            'title': 'Realizing Success Isn\'t Everything'
        },
        {
            'user': users[4],  # Sam - anxious achiever
            'conversation': create_impostor_syndrome_conversation(),
            'title': 'The Day I Stopped Pretending to Be Perfect'
        }
    ]
    
    created_stories = 0
    
    for i, conv_data in enumerate(conversations, 1):
        user = conv_data['user']
        conversation = conv_data['conversation']
        title = conv_data['title']
        
        print(f"\n💬 Creating conversation {i}: {user['name']}")
        print(f"   📖 Scenario: {user['scenario']}")
        print(f"   💭 Messages: {len(conversation)} exchanges")
        
        # Send conversation through chat API to generate story
        auth_headers = {'X-User-ID': user['id']}
        
        try:
            # Send each message in sequence to build up conversation context
            for msg in conversation:
                if msg['role'] == 'user':
                    message_data = {
                        'message': msg['content'],
                        'conversation_history': conversation[:conversation.index(msg)+1]
                    }
                    
                    response = requests.post(
                        f"{BASE_URL}/api/chat/message",
                        json=message_data,
                        headers=auth_headers
                    )
                    
                    # Small delay to simulate natural conversation
                    time.sleep(0.5)
            
            print(f"   ✅ Conversation processed - story should be generated")
            created_stories += 1
            
        except Exception as e:
            print(f"   ❌ Error processing conversation: {e}")
    
    print(f"\n🎉 CONVERSATION CREATION COMPLETE!")
    print(f"   📚 Created {created_stories} rich conversations")
    print(f"   ⏱️  Processing time: ~30 seconds for natural flow")
    
    # Wait a moment for story generation to complete
    print(f"\n⏳ Waiting for story generation to complete...")
    time.sleep(5)
    
    # Check results
    response = requests.get(f"{BASE_URL}/api/stories")
    if response.status_code == 200:
        new_stories = response.json()
        print(f"✅ Generated {len(new_stories)} stories from conversations")
        
        for story in new_stories:
            word_count = len(story.get('content', '').split())
            print(f"   📖 \"{story['title']}\" by {story.get('author', 'Unknown')} ({word_count} words)")

def create_deep_philosophical_conversation():
    """Maya's quarter-life crisis conversation - introspective and analytical"""
    return [
        {'role': 'user', 'content': "I've been feeling so lost lately. Like, I graduated college two years ago and I still have no idea what I'm doing with my life."},
        {'role': 'assistant', 'content': "That uncertainty can feel overwhelming. What aspects of feeling lost are weighing on you most right now?"},
        {'role': 'user', 'content': "It's like everyone else has their life figured out, you know? My friends from college are getting promotions, buying houses, getting engaged. And I'm still working this random office job that has nothing to do with my degree."},
        {'role': 'assistant', 'content': "It sounds like you're comparing your internal experience to others' external achievements. What did you imagine your life would look like at this point?"},
        {'role': 'user', 'content': "I thought I'd be passionate about something by now. In college, I was so sure I wanted to be a teacher. But then I did student teaching and realized I hated the actual classroom management part. The kids were great, but dealing with administration and parents was exhausting."},
        {'role': 'assistant', 'content': "That's a significant realization. It takes courage to acknowledge when something you thought you wanted doesn't align with reality. What parts of teaching did you enjoy?"},
        {'role': 'user', 'content': "I loved the one-on-one moments with students. When you could see something click for them, or when they'd come to you with problems. I liked being someone they could trust. But the system itself just felt so broken."},
        {'role': 'assistant', 'content': "Those meaningful connections seem really important to you. Have you found ways to have similar impacts in other contexts?"},
        {'role': 'user', 'content': "Actually, yeah. I've been volunteering at this community center on weekends, helping adults with their GED prep. It's completely different energy. These people chose to be there, they want to learn. And there's no bureaucracy - just real people working toward real goals."},
        {'role': 'assistant', 'content': "That sounds incredibly fulfilling. What does that volunteer experience tell you about what you value in work?"},
        {'role': 'user', 'content': "I guess I need to feel like I'm actually helping people, not just going through motions. And I need autonomy - I hate being micromanaged or having to follow scripts. The community center lets me teach however I think works best for each person."},
        {'role': 'assistant', 'content': "Those are important insights about your values. What would it look like to find or create work that honors those needs?"},
        {'role': 'user', 'content': "Honestly, I've been thinking about going back to school for social work or maybe nonprofit management. But I'm scared of taking on more debt when I already have student loans. And what if I hate that too?"},
        {'role': 'assistant', 'content': "Fear of making the 'wrong' choice again makes sense after your teaching experience. What small steps could you take to explore these fields without committing to graduate school right away?"},
        {'role': 'user', 'content': "I could probably shadow some social workers, or maybe look into nonprofit jobs that don't require a master's degree. Actually, the community center director has been talking about creating a coordinator position - maybe that's worth exploring."},
        {'role': 'assistant', 'content': "That sounds like a practical way to test your interests. What feels scariest about potentially making a career change?"},
        {'role': 'user', 'content': "Disappointing my parents, honestly. They're immigrants and they sacrificed so much for me to go to college. They see my teaching degree as this stable, respectable career path. If I tell them I want to work at a community center... I don't know how they'll react."},
        {'role': 'assistant', 'content': "Their expectations come from love and their own experiences with security. How might you help them understand what fulfillment means to you?"},
        {'role': 'user', 'content': "Maybe I need to show them rather than just tell them. Like, if I can prove that this work makes me happy and successful in my own way... They want me to be happy, they just define success differently than I do."},
        {'role': 'assistant', 'content': "That's a mature perspective. What would success look like to you in five years?"},
        {'role': 'user', 'content': "Waking up excited about my work most days. Having enough money to live comfortably, but not needing to be rich. Making a real difference in people's lives. Maybe running my own program or center eventually. And feeling proud of the path I chose, even if it's not traditional."}
    ]

def create_friendship_drama_conversation():
    """Jack's friendship authenticity conversation - emotional and relational"""
    return [
        {'role': 'user', 'content': "I'm dealing with some serious friend drama right now and I don't know what to do. My best friend since high school basically called me fake to my face."},
        {'role': 'assistant', 'content': "That must have been really hurtful to hear. What led to that conversation?"},
        {'role': 'user', 'content': "We were at this party last weekend, and I was being my usual social self - talking to everyone, making jokes, being the life of the party, you know? Later, when we were walking home, she said I was 'performing' and asked why I can't just be real."},
        {'role': 'assistant', 'content': "How did that land for you when she said that?"},
        {'role': 'user', 'content': "It honestly crushed me. Like, that IS me being real. I genuinely enjoy meeting people and making them laugh. But then I started second-guessing everything. Am I actually fake? Have I been lying to myself about who I am?"},
        {'role': 'assistant', 'content': "It sounds like her comment made you question your authentic self. What feels true to you about how you show up in social situations?"},
        {'role': 'user', 'content': "I mean, I do get energy from making people happy. When someone laughs at my joke or when I can help someone feel included in a conversation, that genuinely makes me feel good. But Sarah - my friend - she's always been more introverted. Maybe she doesn't get it."},
        {'role': 'assistant', 'content': "Different people express authenticity in different ways. What do you think Sarah means when she talks about being 'real'?"},
        {'role': 'user', 'content': "She's the type who only talks when she has something meaningful to say. She hates small talk, rolls her eyes at what she calls 'surface-level interactions.' For her, being real means sharing deep thoughts and feelings, not chatting about weekend plans or complimenting someone's outfit."},
        {'role': 'assistant', 'content': "It sounds like you two have different styles of connecting with people. Have there been times when you've felt pressure to be different than you naturally are?"},
        {'role': 'user', 'content': "Actually, yes. When I'm around Sarah and her other friends, I do tone myself down. They're all really intellectual and serious, and sometimes I feel like my humor or enthusiasm is too much for them. So I try to match their energy."},
        {'role': 'assistant', 'content': "That's an interesting observation. How does it feel when you're adjusting yourself in those situations?"},
        {'role': 'user', 'content': "Exhausting, honestly. I spend the whole time monitoring myself - is this too loud? Too silly? Am I talking too much? It's like I'm walking on eggshells. But I thought that's what friendship was - adapting to make others comfortable."},
        {'role': 'assistant', 'content': "There's a difference between being considerate and completely suppressing your natural way of being. What happens when you're with friends who appreciate your full personality?"},
        {'role': 'user', 'content': "I feel alive! Like, last month I went to my coworker's birthday party and I didn't know anyone there. By the end of the night, I had three new Instagram friends and plans to go rock climbing with two people. Everyone was laughing and having fun, and I felt like myself."},
        {'role': 'assistant', 'content': "That sounds energizing and fulfilling. What does that tell you about the kind of friendships that work best for you?"},
        {'role': 'user', 'content': "Maybe I need friends who celebrate my social side instead of making me feel like it's a character flaw. Don't get me wrong - I value deep conversations too. But I shouldn't have to choose between being social and being authentic."},
        {'role': 'assistant', 'content': "That's a powerful realization. How might this change how you approach your friendship with Sarah?"},
        {'role': 'user', 'content': "I think I need to have an honest conversation with her. Tell her that calling me fake really hurt, and explain that my social personality isn't a performance - it's genuinely who I am. If she can't accept that part of me, maybe we're just growing in different directions."},
        {'role': 'assistant', 'content': "That takes a lot of courage. What would it mean for your friendship if you showed up as your full self?"},
        {'role': 'user', 'content': "Either it gets stronger because we're being honest with each other, or we realize we're not as compatible as we thought. And honestly? Both outcomes are better than me pretending to be someone I'm not just to keep the peace."},
        {'role': 'assistant', 'content': "What have you learned about yourself through this situation?"},
        {'role': 'user', 'content': "That I'd rather be genuinely liked for who I am than fake-liked for who I'm pretending to be. And that my social energy isn't something to apologize for - it's actually one of my strengths. I make people feel welcome and included. That's valuable."}
    ]

def create_creative_struggle_conversation():
    """Riley's creative block conversation - artistic and perfectionist"""
    return [
        {'role': 'user', 'content': "I haven't created anything meaningful in months and it's killing me. I used to paint every day, but now I just stare at blank canvases."},
        {'role': 'assistant', 'content': "Creative blocks can feel devastating when art is such an important part of who you are. What do you think changed?"},
        {'role': 'user', 'content': "I think it started when I got rejected from that gallery show I really wanted. The curator said my work was 'technically proficient but lacks emotional depth.' I can't stop thinking about that phrase."},
        {'role': 'assistant', 'content': "That must have been difficult feedback to receive. How has it affected the way you approach your art?"},
        {'role': 'user', 'content': "Now every time I pick up a brush, I hear those words. I start second-guessing every stroke, wondering if it's deep enough, meaningful enough. I've started and abandoned like fifteen paintings because none of them feel important enough."},
        {'role': 'assistant', 'content': "It sounds like you're putting enormous pressure on each piece to be profound. What was your relationship with painting like before this feedback?"},
        {'role': 'user', 'content': "It was my escape, my meditation. I'd lose hours just exploring color and texture. I painted landscapes, still lifes, abstract pieces - whatever felt right in the moment. Some were terrible, some were okay, a few were actually pretty good."},
        {'role': 'assistant', 'content': "That sounds like a much more organic relationship with your creativity. What made those 'pretty good' pieces special?"},
        {'role': 'user', 'content': "They came from somewhere real, you know? Like, there was this painting I did after my grandmother died - it was just these deep blues and purples swirling together, nothing literal. But it captured exactly how grief felt to me. My family still talks about that one."},
        {'role': 'assistant', 'content': "That painting sounds like it had deep emotional resonance. What was different about your process when you created it?"},
        {'role': 'user', 'content': "I wasn't trying to make 'art' with a capital A. I was just trying to process what I was feeling. I remember crying while I painted it, getting paint on my face because I was so absorbed in the work. It felt necessary, not optional."},
        {'role': 'assistant', 'content': "There's something powerful about creating from necessity rather than obligation. What would it look like to reconnect with that sense of necessity?"},
        {'role': 'user', 'content': "Maybe I need to stop thinking about galleries and critics and just paint for myself again. But it's hard - once you start wanting external validation, it's difficult to ignore that voice."},
        {'role': 'assistant', 'content': "That tension between internal motivation and external validation is something many artists struggle with. What draws you to want that recognition?"},
        {'role': 'user', 'content': "I want to know that my art matters to other people, not just me. I want to make a living from my creativity someday. And honestly, I want to prove to everyone who said art wasn't a 'real career' that they were wrong."},
        {'role': 'assistant', 'content': "Those are understandable desires. How might you balance those longer-term goals with the immediate need to reconnect with your creative flow?"},
        {'role': 'user', 'content': "Maybe I could set aside certain times for 'practice painting' - work that's just for me, where I don't worry about whether it's gallery-worthy. And then other times for more intentional pieces that I might want to show."},
        {'role': 'assistant', 'content': "That sounds like a way to protect your creative exploration while still working toward your professional goals. What would make the 'practice painting' feel safe?"},
        {'role': 'user', 'content': "Maybe using cheaper materials so I don't feel precious about wasting them. Or painting in a sketchbook instead of on canvases. Actually, I used to carry a tiny watercolor set everywhere and do little studies of things I noticed. I stopped doing that."},
        {'role': 'assistant', 'content': "What happened to that practice?"},
        {'role': 'user', 'content': "I decided it wasn't 'serious' enough. I thought I needed to be working big and bold to be taken seriously as an artist. But those little studies were some of my favorite work. They felt spontaneous and alive."},
        {'role': 'assistant', 'content': "What would it mean to give yourself permission to value that spontaneous, alive feeling again?"},
        {'role': 'user', 'content': "Maybe that the journey is as important as the destination. That becoming a better artist means allowing myself to play and experiment, not just striving for masterpieces. The curator wanted emotional depth - maybe that comes from trusting my instincts, not overthinking everything."}
    ]

def create_burnout_conversation():
    """Alex's work-life balance conversation - ambitious but struggling"""
    return [
        {'role': 'user', 'content': "I think I'm burning out and I don't know how to stop. I've been working 70-hour weeks for months and my relationship is falling apart."},
        {'role': 'assistant', 'content': "That sounds incredibly overwhelming. What's driving the long hours right now?"},
        {'role': 'user', 'content': "I got promoted to team lead six months ago and I feel like I have to prove I deserve it. My boss keeps loading more projects on my plate, and I can't seem to say no. Plus half my team is new, so I'm constantly training people."},
        {'role': 'assistant', 'content': "It sounds like you're taking on multiple roles - your own work, management responsibilities, and training. What happens when you consider delegating or setting boundaries?"},
        {'role': 'user', 'content': "I tell myself I will, but then I see how much the new people are struggling and it's faster to just do it myself. And my boss keeps saying things like 'I know I can count on you' and 'you're the only one who really gets our vision.' It feels impossible to disappoint him."},
        {'role': 'assistant', 'content': "That recognition feels good, but it sounds like it's also trapping you. What's the cost of being indispensable?"},
        {'role': 'user', 'content': "My girlfriend and I barely see each other anymore. When I do get home, I'm exhausted and irritable. She tried to plan a weekend trip for our anniversary and I had to cancel because of a client emergency. She was so hurt."},
        {'role': 'assistant', 'content': "How did that conversation go?"},
        {'role': 'user', 'content': "Not well. She said she feels like she's dating my job, not me. That really stung because work used to be something I was passionate about, but now it just feels like this monster that's consuming everything else."},
        {'role': 'assistant', 'content': "What was your relationship with work like before this promotion?"},
        {'role': 'user', 'content': "I loved it! I was a senior developer and I got to solve interesting problems all day. I had clear deliverables, and when I finished my work, I was done. I actually had hobbies - I played guitar, went hiking, cooked elaborate meals for my girlfriend."},
        {'role': 'assistant', 'content': "That sounds like a much more balanced life. What's different about the management role that makes boundaries harder?"},
        {'role': 'user', 'content': "Everything feels urgent and everything feels like my responsibility. When someone on my team struggles, their stress becomes my stress. When clients are unhappy, that's on me. And my boss has this open-door policy that basically means I'm available 24/7."},
        {'role': 'assistant', 'content': "You've taken on a lot of emotional responsibility for things that might not entirely be within your control. What would change if you saw your role differently?"},
        {'role': 'user', 'content': "What do you mean?"},
        {'role': 'assistant', 'content': "Instead of being responsible for preventing all problems and stress, what if your job was to help people solve problems and manage stress?"},
        {'role': 'user', 'content': "That's... actually really different. Like, instead of taking on their problems, I'd be teaching them how to handle problems themselves. But what if they fail? What if the projects don't get done right?"},
        {'role': 'assistant', 'content': "What happens in the long term if you continue to do everything yourself versus if you invest time in developing your team's capabilities?"},
        {'role': 'user', 'content': "If I keep doing everything myself, I'll definitely burn out. Probably quit or get fired for being impossible to work with. If I actually train my team properly... it might be rocky at first, but eventually I'd have a team that doesn't need me to micromanage everything."},
        {'role': 'assistant', 'content': "That sounds like a more sustainable approach. What would you need to make that shift?"},
        {'role': 'user', 'content': "I'd need to get comfortable with things not being perfect right away. And I'd need to have a conversation with my boss about realistic expectations. Maybe propose a timeline for transitioning to a more autonomous team structure."},
        {'role': 'assistant', 'content': "What feels most challenging about having that conversation?"},
        {'role': 'user', 'content': "Admitting that I can't handle everything. I've built this reputation as the person who gets things done, and I'm afraid that if I set boundaries, they'll think I'm not committed or capable."},
        {'role': 'assistant', 'content': "What would a truly capable leader do in this situation?"},
        {'role': 'user', 'content': "A capable leader would build systems that don't depend entirely on them. They'd develop their team and create sustainable processes. They'd... probably work normal hours and still deliver great results because they'd built something bigger than just their individual effort."},
        {'role': 'assistant', 'content': "That sounds like leadership worth aspiring to. What's one small step you could take this week toward that vision?"},
        {'role': 'user', 'content': "I could stop checking email after 8 PM. And maybe schedule dedicated training time instead of just fixing problems as they come up. Actually... I should probably have a serious conversation with my girlfriend too. She deserves to know that I'm working on this."}
    ]

def create_impostor_syndrome_conversation():
    """Sam's impostor syndrome conversation - anxious achiever with family pressure"""
    return [
        {'role': 'user', 'content': "I got into medical school and instead of being excited, I'm terrified that they're going to realize they made a mistake accepting me."},
        {'role': 'assistant', 'content': "That's such a huge accomplishment - congratulations! What's making you feel like you don't belong there?"},
        {'role': 'user', 'content': "Everyone else seems so much smarter and more prepared. In our pre-orientation group chat, people are talking about research they've published and volunteer work in other countries. I feel like such a fraud."},
        {'role': 'assistant', 'content': "It sounds like you're comparing your internal doubts to other people's highlight reels. What did you bring to your application that got you accepted?"},
        {'role': 'user', 'content': "I mean, I had good grades and test scores. I volunteered at a free clinic for two years. But nothing as impressive as what these other people are doing. My parents keep telling everyone they know that their daughter is going to be a doctor, and I'm scared I'm going to disappoint them."},
        {'role': 'assistant', 'content': "There's a lot of pressure in that expectation. What drew you to medicine in the first place?"},
        {'role': 'user', 'content': "Honestly? I've wanted to be a doctor since I was eight years old. My little brother has diabetes, and I watched how the doctors at the children's hospital took care of him. They were so knowledgeable and compassionate. I wanted to be able to help families like mine."},
        {'role': 'assistant', 'content': "That's a powerful motivation. How does that eight-year-old's dream connect to where you are now?"},
        {'role': 'user', 'content': "I guess I've lost sight of that. Somewhere along the way, it became more about achieving and proving myself than about actually helping people. The pressure to be perfect has been overwhelming."},
        {'role': 'assistant', 'content': "When did that shift happen for you?"},
        {'role': 'user', 'content': "Probably in high school when I realized how competitive pre-med was going to be. My parents started monitoring my grades obsessively, asking about everyone else's test scores. It became less about learning and more about being the best."},
        {'role': 'assistant', 'content': "That sounds exhausting. How has that pressure affected your relationship with learning?"},
        {'role': 'user', 'content': "I study constantly but I never feel like I know enough. Even when I ace an exam, I'm already worried about the next one. I can't enjoy my successes because I'm always focused on what I might fail at next."},
        {'role': 'assistant', 'content': "What would it look like to study from curiosity rather than fear?"},
        {'role': 'user', 'content': "I actually remember that feeling! In my anatomy class last year, there was this one lecture about how the heart develops in utero. It was so fascinating that I went down a rabbit hole reading research papers for hours, not because I had to, but because I wanted to understand."},
        {'role': 'assistant', 'content': "What was different about that experience?"},
        {'role': 'user', 'content': "I wasn't thinking about grades or competition. I was just genuinely amazed by how complex and elegant the human body is. I felt like I was discovering something magical instead of cramming information into my brain."},
        {'role': 'assistant', 'content': "That sense of wonder sounds like it connects back to what originally drew you to medicine. How might you cultivate more of that feeling?"},
        {'role': 'user', 'content': "Maybe I need to remember that everyone in my med school class is there because they earned it, including me. We're all going to be learning together. It doesn't have to be a competition - we could actually help each other."},
        {'role': 'assistant', 'content': "What would change if you approached medical school as collaboration rather than competition?"},
        {'role': 'user', 'content': "I'd probably learn better, honestly. I've always understood things better when I can discuss them with other people. And I'd be less stressed if I wasn't constantly comparing myself to everyone else."},
        {'role': 'assistant', 'content': "How do you think your family would respond if you shared some of these feelings with them?"},
        {'role': 'user', 'content': "My parents... they mean well, but they see my achievements as validation of their sacrifices. They immigrated here so I could have opportunities they never had. When I succeed, it feels like proof that it was all worth it."},
        {'role': 'assistant', 'content': "That's a lot of weight to carry. What would it mean to honor their sacrifices while also taking care of your own well-being?"},
        {'role': 'user', 'content': "Maybe succeeding isn't just about grades and accolades. Maybe it's about becoming the kind of doctor they'd be proud of - one who genuinely cares about patients and never stops learning. That might matter more than being at the top of my class."},
        {'role': 'assistant', 'content': "What kind of doctor do you want to become?"},
        {'role': 'user', 'content': "Someone like the doctors who took care of my brother. They were brilliant, yes, but they were also kind. They took time to explain things to my scared parents. They saw my brother as a whole person, not just a medical case. If I can become that kind of doctor, then I'll have truly succeeded."},
        {'role': 'assistant', 'content': "That sounds like a meaningful definition of success. How does that change how you think about starting medical school?"},
        {'role': 'user', 'content': "It makes it feel less scary, honestly. Instead of worrying about proving I belong there, I can focus on becoming the person I want to be. The skills will come, the knowledge will come, but the compassion - that's something I can start practicing right now."}
    ]

if __name__ == "__main__":
    try:
        create_long_engaging_conversations()
    except KeyboardInterrupt:
        print("\n👋 Conversation creation interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc() 