from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from libs.db_service import ThoughtService, init_database, get_db
from redis import Redis
from rq import Queue
import os

app = FastAPI(title="Thought Aggregator API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis setup
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
q = Queue(connection=redis_conn)

class ThoughtCreate(BaseModel):
    title: str
    content: str
    emotions: Optional[List[str]] = []
    is_generated: Optional[bool] = False

class ThoughtLinkCreate(BaseModel):
    target_id: int

@app.on_event("startup")
def startup():
    init_database()

@app.get("/")
def read_root():
    return {"message": "Welcome to Thought Aggregator API"}

@app.post("/thoughts/")
def create_thought(thought_data: ThoughtCreate):
    thought = ThoughtService.create_thought(
        title=thought_data.title,
        content=thought_data.content,
        emotions=thought_data.emotions,
        is_generated=thought_data.is_generated
    )
    
    # Enqueue background tasks
    q_distortions = Queue('distortions', connection=redis_conn)
    q_sentiment = Queue('sentiment', connection=redis_conn)
    
    q_distortions.enqueue("workers.tasks.analyze_cognitive_distortions", thought.id)
    q_sentiment.enqueue("workers.tasks.analyze_sentiment", thought.id)
    return thought.dict()

@app.get("/thoughts/")
def list_thoughts(
    tag: Optional[str] = None, 
    emotion: Optional[str] = None, 
    page: int = 1, 
    limit: int = 10
):
    result = ThoughtService.list_thoughts(tag=tag, emotion=emotion, page=page, limit=limit)
    
    return {
        "total": result["total"],
        "page": page,
        "limit": limit,
        "items": [t.dict() for t in result["items"]]
    }

@app.post("/thoughts/{thought_id}/links")
def link_thought(thought_id: int, link_data: ThoughtLinkCreate):
    success = ThoughtService.link_thoughts(thought_id, link_data.target_id)
    if not success:
        # We don't have detailed error reasons from the service yet, 
        # but we can improve this if needed.
        raise HTTPException(status_code=400, detail="Cannot link thoughts. Check if thought exists, is linked to itself, or exceeds limit.")
    return {"message": "Linked successfully"}

@app.get("/thoughts/{thought_id}")
def get_thought(thought_id: int):
    thought = ThoughtService.get_thought(thought_id)
    if not thought:
        raise HTTPException(status_code=404, detail="Thought not found")
    return thought.dict()
