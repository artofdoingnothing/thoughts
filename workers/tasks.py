from libs.db_service import ThoughtService
from libs.processor_service import ProcessorService
import requests
from bs4 import BeautifulSoup
from redis import Redis
from rq import Queue
import os
import re


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

def generate_essay(persona_id, starting_text):
    print(f"Generating essay for persona {persona_id}...")
    persona = ThoughtService.get_persona(persona_id)
    if not persona:
            print(f"Persona {persona_id} not found.")
            return "Error: Persona not found"

    metrics = ThoughtService.get_persona_metrics(persona_id)
    
    persona_details = f"Name: {persona.name}, Age: {persona.age}, Gender: {persona.gender}"
    
    essay = processor.generate_essay(
        starting_text=starting_text,
        persona_details=persona_details,
        emotions=metrics['top_emotions'],
        tags=metrics['top_tags']
    )
    print(f"Generated essay of length {len(essay)}")
    return essay

