from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from libs.db_service import ConversationService, ConversationDomain
from redis import Redis
from rq import Queue
import os

router = APIRouter(prefix="/conversations", tags=["Conversations"])

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)

class ConversationCreate(BaseModel):
    title: str
    context: str
    persona_ids: List[int]

class GenerateMessageRequest(BaseModel):
    persona_id: int

class AddPersonaToConversationRequest(BaseModel):
    persona_id: int

class GenerateSequenceRequest(BaseModel):
    persona_ids: List[int]

@router.post("/", response_model=ConversationDomain)
def create_conversation(conversation: ConversationCreate):
    new_conversation = ConversationService.create_conversation(
        title=conversation.title,
        context=conversation.context,
        persona_ids=conversation.persona_ids
    )
    if not new_conversation:
         raise HTTPException(status_code=400, detail="Could not create conversation. Check persona IDs.")
    return new_conversation

@router.get("/", response_model=List[ConversationDomain])
def list_conversations():
    return ConversationService.list_conversations()

@router.get("/{conversation_id}", response_model=ConversationDomain)
def get_conversation(conversation_id: int):
    conversation = ConversationService.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post("/{conversation_id}/generate")
def generate_message(conversation_id: int, request: GenerateMessageRequest):
    conversation = ConversationService.get_conversation(conversation_id)
    if not conversation:
         raise HTTPException(status_code=404, detail="Conversation not found")
    
    q_generation = Queue('generation', connection=redis_conn)
    q_generation.enqueue("workers.tasks.generate_conversation_message", conversation_id, request.persona_id)
    
    return {"message": "Message generation passed to worker"}

@router.post("/{conversation_id}/generate_sequence")
def generate_sequence(conversation_id: int, request: GenerateSequenceRequest):
    conversation = ConversationService.get_conversation(conversation_id)
    if not conversation:
         raise HTTPException(status_code=404, detail="Conversation not found")
    
    q_generation = Queue('generation', connection=redis_conn)
    q_generation.enqueue("workers.tasks.generate_conversation_sequence", conversation_id, request.persona_ids)
    
    return {"message": "Message sequence generation passed to worker"}


@router.post("/{conversation_id}/personas")
def add_persona_to_conversation(conversation_id: int, request: AddPersonaToConversationRequest):
    success = ConversationService.add_persona_to_conversation(conversation_id, request.persona_id)
    if not success:
         raise HTTPException(status_code=400, detail="Could not add persona to conversation. Check IDs.")
    return {"message": "Persona added successfully"}

@router.post("/{conversation_id}/end")
def end_conversation(conversation_id: int):
    success = ConversationService.end_conversation(conversation_id)
    if not success:
         raise HTTPException(status_code=400, detail="Could not end conversation.")
    return {"message": "Conversation ended and thoughts created"}
