from libs.db_service import ThoughtService
from libs.processor_service import ProcessorService
import requests
from bs4 import BeautifulSoup
from redis import Redis
from rq import Queue
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)

processor = ProcessorService()

def analyze_cognitive_distortions(thought_id):
    print(f"Analyzing cognitive distortions for thought {thought_id}...")
    try:
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
        
    except Exception as e:
        print(f"Error analyzing distortions for thought {thought_id}: {e}")

def analyze_sentiment(thought_id):
    print(f"Analyzing sentiment for thought {thought_id}...")
    try:
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
            
    except Exception as e:
        print(f"Error analyzing sentiment for thought {thought_id}: {e}")

def parse_blog_and_generate_thoughts(url, persona_id):
    print(f"Parsing blog {url} for persona {persona_id}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        page_title = soup.title.string.strip() if soup.title and soup.title.string else "Blog Post"
        
        # Simple extraction of text
        # Getting all p tags might be better than whole text to avoid script/style noise
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        text_content = "\n".join(paragraphs)
        
        # If text content is too small, fallback to get_text
        if len(text_content) < 100:
             text_content = soup.get_text()

        thoughts = processor.generate_thoughts_from_text(text_content)
        print(f"Generated {len(thoughts)} thoughts from blog.")

        q_distortions = Queue('distortions', connection=redis_conn)
        q_sentiment = Queue('sentiment', connection=redis_conn)

        for i, content in enumerate(thoughts):
            thought_title = f"{page_title} - {i+1}"
            
            # Create thought
            thought = ThoughtService.create_thought(
                title=thought_title,
                content=content,
                is_generated=True,
                persona_id=persona_id
            )
            print(f"Created thought {thought.id}: {thought_title}")

            # Enqueue for analysis
            q_distortions.enqueue("workers.tasks.analyze_cognitive_distortions", thought.id)
            q_sentiment.enqueue("workers.tasks.analyze_sentiment", thought.id)
            
    except Exception as e:
        print(f"Error parsing blog or generating thoughts: {e}")

