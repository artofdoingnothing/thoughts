import os

from redis import Redis
from rq import Queue

from libs.use_cases import ConversationUseCases, GenerationUseCases, ThoughtUseCases

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)

thought_uc = ThoughtUseCases()
conversation_uc = ConversationUseCases()
generation_uc = GenerationUseCases()


def analyze_cognitive_distortions(thought_id):
    print(f"Analyzing cognitive distortions for thought {thought_id}...")
    distortions = thought_uc.analyze_cognitive_distortions(thought_id)
    if not distortions:
        print(f"Thought {thought_id} not found or no distortions.")
        return
    print(f"Identified distortions: {distortions}")
    print(f"Added distortion tags to thought {thought_id}")


def analyze_sentiment(thought_id):
    print(f"Analyzing sentiment for thought {thought_id}...")
    emotions = thought_uc.analyze_sentiment(thought_id)
    if not emotions:
        print(f"Thought {thought_id} not found or no emotions.")
        return
    print(f"Identified emotions: {emotions}")
    print(f"Added emotions to thought {thought_id}")


def analyze_action_orientation(thought_id):
    print(f"Analyzing action orientation for thought {thought_id}...")
    result = thought_uc.analyze_action_orientation(thought_id)
    if not result:
        print(f"Thought {thought_id} not found.")
        return
    print(f"Identified action orientation: {result}")
    print(f"Updated thought {thought_id} with action orientation")


def analyze_thought_type(thought_id):
    print(f"Analyzing thought type for thought {thought_id}...")
    result = thought_uc.analyze_thought_type(thought_id)
    if not result:
        print(f"Thought {thought_id} not found.")
        return
    print(f"Identified thought type: {result}")
    print(f"Updated thought {thought_id} with thought type")


def analyze_topics(thought_id):
    print(f"Analyzing topics for thought {thought_id}...")
    topics = thought_uc.analyze_topics(thought_id)
    if not topics:
        print(f"Thought {thought_id} not found or no topics.")
        return
    print(f"Identified topics: {topics}")
    print(f"Added topics to thought {thought_id}")


def parse_blog_and_generate_thoughts(url, persona_id):
    print(f"STARTING: Parsing blog {url} for persona {persona_id}...")

    text_content = generation_uc.parse_blog(url)
    thoughts = generation_uc.generate_thoughts_from_text(text_content)
    print(f"Generated {len(thoughts)} thoughts from blog.")

    q_distortions = Queue("distortions", connection=redis_conn)
    q_sentiment = Queue("sentiment", connection=redis_conn)
    q_action = Queue("action_orientation", connection=redis_conn)
    q_type = Queue("thought_type", connection=redis_conn)
    q_topics = Queue("topics", connection=redis_conn)

    for content in thoughts:
        thought = thought_uc.create_thought(
            content=content, is_generated=True, persona_id=persona_id
        )
        print(f"Created thought {thought.id}")

        q_distortions.enqueue("workers.tasks.analyze_cognitive_distortions", thought.id)
        q_sentiment.enqueue("workers.tasks.analyze_sentiment", thought.id)
        q_action.enqueue("workers.tasks.analyze_action_orientation", thought.id)
        q_type.enqueue("workers.tasks.analyze_thought_type", thought.id)
        q_topics.enqueue("workers.tasks.analyze_topics", thought.id)


def generate_essay(persona_id, starting_text):
    print(f"Generating essay for persona {persona_id}...")
    final_essay = generation_uc.generate_essay(persona_id, starting_text)
    print(f"Final essay length: {len(final_essay)}")
    return final_essay


def generate_conversation_message(conversation_id, persona_id):
    print(
        f"Generating conversation message for conversation {conversation_id}, persona {persona_id}..."
    )
    message_contents = conversation_uc.generate_conversation_message(
        conversation_id, persona_id
    )
    if not message_contents:
        print("Conversation or Persona not found, or generation failed.")
        return
    print(f"Generated {len(message_contents)} message(s): {message_contents}")
    print(f"{len(message_contents)} message(s) added to conversation.")


def generate_conversation_sequence(conversation_id: int, persona_ids: list):
    print(
        f"Generating conversation sequence for conversation {conversation_id}, personas {persona_ids}..."
    )
    for persona_id in persona_ids:
        print(f"Sequence step: Generating message for persona {persona_id}")
        generate_conversation_message(conversation_id, persona_id)
    print(
        f"Completed conversation sequence generation for conversation {conversation_id}."
    )


def process_conversation_thoughts(conversation_id: int):
    print(f"Processing thoughts for ended conversation {conversation_id}...")
    conversation_uc.process_conversation_thoughts(conversation_id)
    print(f"Completed processing thoughts for conversation {conversation_id}.")


def generate_persona_from_movie_characters(character_ids: list):
    print(f"STARTING: Generating persona from character IDs: {character_ids}")

    result = generation_uc.generate_persona_from_movie_characters(character_ids)
    persona_id = result["persona_id"]
    thoughts = result["thoughts"]
    print(f"Generated persona {persona_id} with {len(thoughts)} thoughts.")

    q_distortions = Queue("distortions", connection=redis_conn)
    q_sentiment = Queue("sentiment", connection=redis_conn)
    q_action = Queue("action_orientation", connection=redis_conn)
    q_type = Queue("thought_type", connection=redis_conn)
    q_topics = Queue("topics", connection=redis_conn)

    for content in thoughts:
        thought = thought_uc.create_thought(
            content=content, is_generated=True, persona_id=persona_id
        )
        print(f"Created thought {thought.id} for persona {persona_id}")

        q_distortions.enqueue("workers.tasks.analyze_cognitive_distortions", thought.id)
        q_sentiment.enqueue("workers.tasks.analyze_sentiment", thought.id)
        q_action.enqueue("workers.tasks.analyze_action_orientation", thought.id)
        q_type.enqueue("workers.tasks.analyze_thought_type", thought.id)
        q_topics.enqueue("workers.tasks.analyze_topics", thought.id)
