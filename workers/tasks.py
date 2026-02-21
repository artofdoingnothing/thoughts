from libs.db_service import ThoughtService
from libs.processor_service import ProcessorService
import requests
from bs4 import BeautifulSoup
from redis import Redis
from rq import Queue
import os
import re
import random


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)

processor = ProcessorService()

def analyze_cognitive_distortions(thought_id):
    print(f"Analyzing cognitive distortions for thought {thought_id}...")
    thought = ThoughtService.get_thought(thought_id)
    if not thought:
        print(f"Thought {thought_id} not found.")
        return

    distortions = processor.analyze_cognitive_distortions(thought.content)
    print(f"Identified distortions: {distortions}")
    
    if distortions:
            # Add tags inferred by LLM
        ThoughtService.add_tags(thought_id, distortions, is_generated=True)
        print(f"Added distortion tags to thought {thought_id}")
    
    ThoughtService.update_status(thought_id, "completed")

def analyze_sentiment(thought_id):
    print(f"Analyzing sentiment for thought {thought_id}...")
    thought = ThoughtService.get_thought(thought_id)
    if not thought:
        print(f"Thought {thought_id} not found.")
        return

    emotions = processor.analyze_sentiment(thought.content)
    print(f"Identified emotions: {emotions}")
    
    if emotions:
            # Add emotions inferred by LLM
        ThoughtService.add_emotions(thought_id, emotions, is_generated=True)
        print(f"Added emotions to thought {thought_id}")
        
    ThoughtService.update_status(thought_id, "completed")

def analyze_action_orientation(thought_id):
    print(f"Analyzing action orientation for thought {thought_id}...")
    thought = ThoughtService.get_thought(thought_id)
    if not thought:
        print(f"Thought {thought_id} not found.")
        return

    result = processor.analyze_action_orientation(thought.content)
    print(f"Identified action orientation: {result}")
    
    ThoughtService.update_thought(thought_id, {"action_orientation": result})
    print(f"Updated thought {thought_id} with action orientation")

def analyze_thought_type(thought_id):
    print(f"Analyzing thought type for thought {thought_id}...")
    thought = ThoughtService.get_thought(thought_id)
    if not thought:
        print(f"Thought {thought_id} not found.")
        return

    result = processor.analyze_thought_type(thought.content)
    print(f"Identified thought type: {result}")
    
    ThoughtService.update_thought(thought_id, {"thought_type": result})
    print(f"Updated thought {thought_id} with thought type")

def analyze_topics(thought_id):
    print(f"Analyzing topics for thought {thought_id}...")
    thought = ThoughtService.get_thought(thought_id)
    if not thought:
        print(f"Thought {thought_id} not found.")
        return

    topics = processor.analyze_topics(thought.content)
    print(f"Identified topics: {topics}")
    
    if topics:
        ThoughtService.add_topics(thought_id, topics, is_generated=True)
        print(f"Added topics to thought {thought_id}")
    
    ThoughtService.update_status(thought_id, "completed")

def parse_blog_and_generate_thoughts(url, persona_id):
    print(f"STARTING: Parsing blog {url} for persona {persona_id}...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Simple extraction of text
    # Getting all p tags might be better than whole text to avoid script/style noise
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    text_content = "\\n".join(paragraphs)
    
    # If text content is too small, fallback to get_text
    if len(text_content) < 100:
            text_content = soup.get_text()



    thoughts = processor.generate_thoughts_from_text(text_content)
    print(f"Generated {len(thoughts)} thoughts from blog.")

    q_distortions = Queue('distortions', connection=redis_conn)
    q_sentiment = Queue('sentiment', connection=redis_conn)
    q_action = Queue('action_orientation', connection=redis_conn)
    q_type = Queue('thought_type', connection=redis_conn)
    q_topics = Queue('topics', connection=redis_conn)

    for i, content in enumerate(thoughts):
        
        # Create thought
        thought = ThoughtService.create_thought(
            content=content,
            is_generated=True,
            persona_id=persona_id
        )
        print(f"Created thought {thought.id}")

        # Enqueue for analysis
        q_distortions.enqueue("workers.tasks.analyze_cognitive_distortions", thought.id)
        q_sentiment.enqueue("workers.tasks.analyze_sentiment", thought.id)
        q_action.enqueue("workers.tasks.analyze_action_orientation", thought.id)
        q_type.enqueue("workers.tasks.analyze_thought_type", thought.id)
        q_topics.enqueue("workers.tasks.analyze_topics", thought.id)

def generate_essay(persona_id, starting_text):
    print(f"Generating essay for persona {persona_id}...")
    persona = ThoughtService.get_persona(persona_id)
    if not persona:
            print(f"Persona {persona_id} not found.")
            return "Error: Persona not found"

    persona_details = f"Name: {persona.name}, Age: {persona.age}, Gender: {persona.gender}"
    
    # Check if persona has a profile (derived persona)
    if persona.profile:
        print(f"Persona {persona_id} has a profile. Using profile-based generation.")
        
        # Step 1: Extract relevant emotions from profile based on starting text
        emotions = processor.extract_emotions_from_profile(starting_text, persona.profile)
        print(f"Extracted emotions from profile: {emotions}")
        
        # Step 2: Complete essay using profile context
        final_essay = processor.complete_essay_with_profile(
            starting_text=starting_text,
            persona_details=persona_details,
            emotions=emotions
        )
    else:
        print(f"Persona {persona_id} has no profile. Using standard generation.")
        unique_attrs = ThoughtService.get_persona_unique_attributes(persona_id)
        
        thought_types = unique_attrs.get("thought_types", [])
        action_orientations = unique_attrs.get("action_orientations", [])
        
        selected_type = random.choice(thought_types) if thought_types else "Automatic"
        selected_action = random.choice(action_orientations) if action_orientations else "Ruminative"
        
        print(f"Selected attributes: Type={selected_type}, Action={selected_action}")
        
        # Step 1: Generate draft and tags
        draft_result = processor.generate_essay_draft_and_tags(
            starting_text=starting_text,
            persona_details=persona_details,
            thought_type=selected_type,
            action_orientation=selected_action
        )
        
        draft_essay = draft_result.get("essay", "")
        generated_tags = draft_result.get("tags", [])
        print(f"Generated draft essay length: {len(draft_essay)}. Tags: {generated_tags}")
        
        final_essay = draft_essay
        
        # Step 2: Find closest thought and modify
        if generated_tags:
            closest_thought = ThoughtService.find_closest_thought_by_tags(generated_tags, persona_id)
            if closest_thought:
                print(f"Found closest thought: {closest_thought.id}")
                # Extract emotion names
                emotions = [e.name for e in closest_thought.emotions]
                if emotions:
                     print(f"Modifying essay with emotions: {emotions}")
                     final_essay = processor.modify_essay(draft_essay, emotions)
            else:
                print("No closest thought found.")
            
    print(f"Final essay length: {len(final_essay)}")
    return final_essay

def generate_conversation_message(conversation_id, persona_id):
    print(f"Generating conversation message for conversation {conversation_id}, persona {persona_id}...")
    conversation = ThoughtService.get_conversation(conversation_id)
    persona = ThoughtService.get_persona(persona_id)
    
    if not conversation or not persona:
        print("Conversation or Persona not found.")
        return

    # Get recent messages (last 5)
    sorted_messages = sorted(conversation.messages, key=lambda m: m.created_at)
    recent = sorted_messages[-5:]
    
    recent_messages_data = [
        {"persona": m.persona.name if m.persona else "Unknown", "content": m.content}
        for m in recent
    ]

    # Gather info about all personas in conversation
    other_personas_info = ""
    for p in conversation.personas:
        if p.id != persona_id:
             other_personas_info += f"- Name: {p.name}, Age: {p.age}, Gender: {p.gender}\n"
    
    if not other_personas_info:
        other_personas_info = "None"

    message_contents = processor.generate_conversation_message(
        persona_name=persona.name,
        persona_age=persona.age,
        persona_gender=persona.gender,
        persona_profile=persona.profile,
        conversation_context=conversation.context or conversation.title,
        recent_messages=recent_messages_data,
        other_personas_info=other_personas_info
    )
    
    print(f"Generated {len(message_contents)} message(s): {message_contents}")
    
    for content in message_contents:
        ThoughtService.add_message(
            conversation_id=conversation_id, 
            persona_id=persona_id, 
            content=content, 
            is_generated=True
        )
    print(f"{len(message_contents)} message(s) added to conversation.")


def generate_conversation_sequence(conversation_id: int, persona_ids: list):
    print(f"Generating conversation sequence for conversation {conversation_id}, personas {persona_ids}...")
    conversation = ThoughtService.get_conversation(conversation_id)
    
    if not conversation:
        print("Conversation not found.")
        return

    # Sequentially call generate_conversation_message to build the context properly over time
    for persona_id in persona_ids:
        print(f"Sequence step: Generating message for persona {persona_id}")
        generate_conversation_message(conversation_id, persona_id)
        
    print(f"Completed conversation sequence generation for conversation {conversation_id}.")
