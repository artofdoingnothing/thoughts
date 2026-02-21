from redis import Redis
from rq import Queue
import os
from .bus import DomainEventBus
from .conversation_events import ConversationEndedEvent

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
q = Queue('generation', connection=redis_conn)

def handle_conversation_ended(event: ConversationEndedEvent):
    # Enqueue a job to process the thoughts from this conversation
    # We will define this task in workers/tasks.py
    q.enqueue("workers.tasks.process_conversation_thoughts", event.conversation_id)

def register_handlers():
    DomainEventBus.subscribe("ConversationEndedEvent", handle_conversation_ended)
