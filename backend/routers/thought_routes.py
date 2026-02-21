from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from libs.db_service import ThoughtService
from redis import Redis
from rq import Queue
import os

router = APIRouter(prefix="/thoughts", tags=["Thoughts"])

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)

class ThoughtCreate(BaseModel):
    content: str
    emotions: Optional[List[str]] = []
    is_generated: Optional[bool] = False
    persona_id: Optional[int] = None
    action_orientation: Optional[str] = None
    thought_type: Optional[str] = None

class ThoughtUpdate(BaseModel):
    status: Optional[str] = None
    emotions: Optional[List[str]] = None
    is_generated: Optional[bool] = None
    action_orientation: Optional[str] = None
    thought_type: Optional[str] = None

class ThoughtLinkCreate(BaseModel):
    target_id: int

@router.post("/")
def create_thought(thought_data: ThoughtCreate):
    thought = ThoughtService.create_thought(
        content=thought_data.content,
        emotions=thought_data.emotions,
        is_generated=thought_data.is_generated,
        persona_id=thought_data.persona_id,
        action_orientation=thought_data.action_orientation,
        thought_type=thought_data.thought_type
    )
    
    q_distortions = Queue('distortions', connection=redis_conn)
    q_sentiment = Queue('sentiment', connection=redis_conn)
    
    q_distortions.enqueue("workers.tasks.analyze_cognitive_distortions", thought.id)
    q_sentiment.enqueue("workers.tasks.analyze_sentiment", thought.id)
    
    q_action = Queue('action_orientation', connection=redis_conn)
    q_type = Queue('thought_type', connection=redis_conn)
    q_action.enqueue("workers.tasks.analyze_action_orientation", thought.id)
    q_type.enqueue("workers.tasks.analyze_thought_type", thought.id)

    return thought.dict()

@router.get("/")
def list_thoughts(
    tag: Optional[str] = None, 
    emotion: Optional[str] = None, 
    persona_id: Optional[int] = None,
    page: int = 1, 
    limit: int = 10
):
    result = ThoughtService.list_thoughts(tag=tag, emotion=emotion, persona_id=persona_id, page=page, limit=limit)
    
    return {
        "total": result["total"],
        "page": page,
        "limit": limit,
        "items": [t.dict() for t in result["items"]]
    }

@router.post("/{thought_id}/links")
def link_thought(thought_id: int, link_data: ThoughtLinkCreate):
    success = ThoughtService.link_thoughts(thought_id, link_data.target_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot link thoughts. Check if thought exists, is linked to itself, or exceeds limit.")
    return {"message": "Linked successfully"}

@router.get("/{thought_id}")
def get_thought(thought_id: int):
    thought = ThoughtService.get_thought(thought_id)
    if not thought:
        raise HTTPException(status_code=404, detail="Thought not found")
    return thought.dict()

@router.delete("/{thought_id}")
def delete_thought(thought_id: int):
    success = ThoughtService.delete_thought(thought_id)
    if not success:
        raise HTTPException(status_code=404, detail="Thought not found")
    return {"message": "Thought deleted successfully"}

@router.put("/{thought_id}")
def update_thought(thought_id: int, thought_update: dict):
    if 'content' in thought_update:
        raise HTTPException(status_code=400, detail="Cannot update content")
    
    updated_thought = ThoughtService.update_thought(thought_id, thought_update)
    if not updated_thought:
        raise HTTPException(status_code=404, detail="Thought not found")
    return updated_thought.dict()
