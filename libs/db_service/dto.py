from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel

class TagDomain(PydanticBaseModel):
    name: str
    is_generated: bool

class EmotionDomain(PydanticBaseModel):
    name: str
    is_generated: bool

class TopicDomain(PydanticBaseModel):
    name: str
    is_generated: bool

class PersonaDomain(PydanticBaseModel):
    id: int
    name: str
    age: int
    gender: str
    profile: Optional[Dict[str, Any]] = None
    additional_info: Optional[Dict[str, Any]] = None
    source: Optional[str] = "manual"
    class Config:
        from_attributes = True

class ThoughtDomain(PydanticBaseModel):
    id: int
    content: str
    status: str
    is_generated: bool
    action_orientation: Optional[str] = None
    thought_type: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    emotions: List[EmotionDomain] = []
    tags: List[TagDomain] = []
    topics: List[TopicDomain] = []
    links: List[int] = []
    persona: Optional[PersonaDomain] = None

    class Config:
        from_attributes = True

class MessageDomain(PydanticBaseModel):
    id: int
    content: str
    is_generated: bool
    created_at: datetime
    persona_id: int
    conversation_id: int
    persona: Optional[PersonaDomain] = None

    class Config:
        from_attributes = True

class ConversationDomain(PydanticBaseModel):
    id: int
    title: str
    context: Optional[str] = None
    created_at: datetime
    messages: List[MessageDomain] = []
    personas: List[PersonaDomain] = []

    class Config:
        from_attributes = True
