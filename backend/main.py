from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from libs.db_service import ThoughtService, init_database, get_db, PersonaDomain
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
    persona_id: Optional[int] = None

class PersonaCreate(BaseModel):
    name: str
    age: int
    gender: str

class GenerateThoughtsRequest(BaseModel):
    urls: List[str]
    persona_id: int

class EssayGenerateRequest(BaseModel):
    starting_text: str
    persona_id: int

class ThoughtUpdate(BaseModel):
    status: Optional[str] = None
    emotions: Optional[List[str]] = None
    is_generated: Optional[bool] = None

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
        is_generated=thought_data.is_generated,
        persona_id=thought_data.persona_id
    )
    
    # Enqueue background tasks
    q_distortions = Queue('distortions', connection=redis_conn)
    q_sentiment = Queue('sentiment', connection=redis_conn)
    
    q_distortions.enqueue("workers.tasks.analyze_cognitive_distortions", thought.id)
    q_sentiment.enqueue("workers.tasks.analyze_sentiment", thought.id)
    return thought.dict()

@app.get("/personas/", response_model=List[PersonaDomain])
def list_personas():
    return ThoughtService.list_personas()

@app.post("/personas/", response_model=PersonaDomain)
def create_persona(persona: PersonaCreate):
    return ThoughtService.create_persona(
        name=persona.name,
        age=persona.age,
        gender=persona.gender
    )

@app.post("/generate-thoughts/")
def generate_thoughts(request: GenerateThoughtsRequest):
    q_generation = Queue('generation', connection=redis_conn)
    for url in request.urls:
        q_generation.enqueue("workers.tasks.parse_blog_and_generate_thoughts", url, request.persona_id)
    return {"message": f"{len(request.urls)} thought generation tasks have been queued"}

@app.post("/essay/generate")
def generate_essay_endpoint(request: EssayGenerateRequest):
    q_essay = Queue('essay', connection=redis_conn)
    job = q_essay.enqueue("workers.tasks.generate_essay", request.persona_id, request.starting_text, job_timeout=600)
    return {"job_id": job.id}

@app.get("/essay/status/{job_id}")
def get_essay_status(job_id: str):
    q_essay = Queue('essay', connection=redis_conn)
    job = q_essay.fetch_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return {
        "job_id": job.id,
        "status": job.get_status(),
        "result": job.result,
        "error": str(job.exc_info) if job.exc_info else None
    }

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

@app.delete("/thoughts/{thought_id}")
def delete_thought(thought_id: int):
    success = ThoughtService.delete_thought(thought_id)
    if not success:
        raise HTTPException(status_code=404, detail="Thought not found")
    return {"message": "Thought deleted successfully"}

@app.put("/thoughts/{thought_id}")
def update_thought(thought_id: int, thought_update: dict):
    # Manually check for restricted fields
    if 'title' in thought_update or 'content' in thought_update:
        raise HTTPException(status_code=400, detail="Cannot update title or content")
    
    updated_thought = ThoughtService.update_thought(thought_id, thought_update)
    if not updated_thought:
        raise HTTPException(status_code=404, detail="Thought not found")
    return updated_thought.dict()
