from pydantic import BaseModel

class ConversationEndedEvent(BaseModel):
    conversation_id: int
