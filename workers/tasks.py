from libs.db_service import ThoughtService
from libs.processor_service import ProcessorService

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
            
    except Exception as e:
        print(f"Error analyzing sentiment for thought {thought_id}: {e}")

