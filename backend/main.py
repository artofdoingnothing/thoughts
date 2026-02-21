from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from libs.db_service import ThoughtService, init_database, get_db, PersonaDomain, ConversationDomain, MessageDomain
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
    content: str
    emotions: Optional[List[str]] = []
    is_generated: Optional[bool] = False
    persona_id: Optional[int] = None
    action_orientation: Optional[str] = None
    thought_type: Optional[str] = None

class PersonaCreate(BaseModel):
    name: str # Optional if generated? No, user can generate then submit.
    age: int
    gender: str
    additional_info: Optional[Dict[str, Any]] = None

class PersonaUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None

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
    action_orientation: Optional[str] = None
    thought_type: Optional[str] = None

class ThoughtLinkCreate(BaseModel):
    target_id: int

class DerivePersonaRequest(BaseModel):
    source_persona_id: int
    name_adjective: str
    percentage: int

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


@app.on_event("startup")
def startup():
    pass 
    # init_database() - Handled by Alembic 


@app.get("/")
def read_root():
    return {"message": "Welcome to Thought Aggregator API"}

@app.post("/thoughts/")
def create_thought(thought_data: ThoughtCreate):
    thought = ThoughtService.create_thought(
        content=thought_data.content,
        emotions=thought_data.emotions,
        is_generated=thought_data.is_generated,
        persona_id=thought_data.persona_id,
        action_orientation=thought_data.action_orientation,
        thought_type=thought_data.thought_type
    )
    
    # Enqueue background tasks
    q_distortions = Queue('distortions', connection=redis_conn)
    q_sentiment = Queue('sentiment', connection=redis_conn)
    
    q_distortions.enqueue("workers.tasks.analyze_cognitive_distortions", thought.id)
    q_distortions.enqueue("workers.tasks.analyze_cognitive_distortions", thought.id)
    q_sentiment.enqueue("workers.tasks.analyze_sentiment", thought.id)
    
    # New classifiers
    q_action = Queue('action_orientation', connection=redis_conn)
    q_type = Queue('thought_type', connection=redis_conn)
    q_action.enqueue("workers.tasks.analyze_action_orientation", thought.id)
    q_type.enqueue("workers.tasks.analyze_thought_type", thought.id)

    return thought.dict()

@app.get("/personas/", response_model=List[PersonaDomain])
def list_personas():
    return ThoughtService.list_personas()

@app.post("/personas/", response_model=PersonaDomain)
def create_persona(persona: PersonaCreate):
    return ThoughtService.create_persona(
        name=persona.name,
        age=persona.age,
        gender=persona.gender,
        additional_info=persona.additional_info
    )

@app.put("/personas/{persona_id}", response_model=PersonaDomain)
def update_persona(persona_id: int, persona_update: PersonaUpdate):
    updates = persona_update.dict(exclude_unset=True)
    updated_persona = ThoughtService.update_persona(persona_id, updates)
    if not updated_persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return updated_persona

@app.post("/personas/generate-name")
def generate_persona_name():
    # Simple generation using LLM or just random words. 
    # Since we have GeminiLLM locally in service, we can use it, but exposing it here 
    # requires importing it or adding a service method.
    # Let's add a service method for it or just use a simple list for now if LLM is overkill?
    # User said "auto generate the name... 2 or 3 words long".
    # Using LLM is safer for "good" names.
    from libs.llm_service.gemini import GeminiLLM
    try:
        llm = GeminiLLM()
        prompt = "Generate a single creative persona name consisting of 2 or 3 words. Return ONLY the name."
        name = llm.generate_content(prompt).strip().replace('"', '').replace('.', '')
        return {"name": name}
    except Exception as e:
        # Fallback
        return {"name": "Random Persona"}

@app.delete("/personas/{persona_id}")
def delete_persona(persona_id: int):
    success = ThoughtService.delete_persona(persona_id)
    if not success:
        raise HTTPException(status_code=404, detail="Persona not found")
    return {"message": "Persona deleted successfully"}

@app.post("/personas/{persona_id}/regenerate", response_model=PersonaDomain)
def regenerate_persona(persona_id: int):
    updated_persona = ThoughtService.regenerate_persona(persona_id)
    if not updated_persona:
         raise HTTPException(status_code=400, detail="Could not regenerate persona. Ensure persona exists and has thoughts.")
    return updated_persona

@app.post("/personas/derive", response_model=PersonaDomain)
def derive_persona(request: DerivePersonaRequest):
    new_persona = ThoughtService.derive_persona(
        source_persona_id=request.source_persona_id,
        name_adjective=request.name_adjective,
        percentage=request.percentage
    )
    if not new_persona:
        raise HTTPException(status_code=400, detail="Could not derive persona. Ensure source persona has thoughts.")
    return new_persona


@app.post("/generate-thoughts/")
def generate_thoughts(request: GenerateThoughtsRequest):
    q_generation = Queue('generation', connection=redis_conn)
    print(f"Received request to generate thoughts for {len(request.urls)} URLs: {request.urls}")
    for url in request.urls:
        print(f"Enqueuing task for {url}")
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
    if 'content' in thought_update:
        # Check if only unrestricted fields are being updated
        pass # Actually service handles mapping, but here we were restricting. allow other fields.
        raise HTTPException(status_code=400, detail="Cannot update content")
    
    updated_thought = ThoughtService.update_thought(thought_id, thought_update)
    if not updated_thought:
        raise HTTPException(status_code=404, detail="Thought not found")
    return updated_thought.dict()

@app.post("/conversations/", response_model=ConversationDomain)
def create_conversation(conversation: ConversationCreate):
    new_conversation = ThoughtService.create_conversation(
        title=conversation.title,
        context=conversation.context,
        persona_ids=conversation.persona_ids
    )
    if not new_conversation:
         raise HTTPException(status_code=400, detail="Could not create conversation. Check persona IDs.")
    return new_conversation

@app.get("/conversations/", response_model=List[ConversationDomain])
def list_conversations():
    return ThoughtService.list_conversations()

@app.get("/conversations/{conversation_id}", response_model=ConversationDomain)
def get_conversation(conversation_id: int):
    conversation = ThoughtService.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@app.post("/conversations/{conversation_id}/generate")
def generate_message(conversation_id: int, request: GenerateMessageRequest):
    conversation = ThoughtService.get_conversation(conversation_id)
    if not conversation:
         raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Enqueue task
    q_generation = Queue('generation', connection=redis_conn)
    q_generation.enqueue("workers.tasks.generate_conversation_message", conversation_id, request.persona_id)
    
    return {"message": "Message generation passed to worker"}

@app.post("/conversations/{conversation_id}/generate_sequence")
def generate_sequence(conversation_id: int, request: GenerateSequenceRequest):
    conversation = ThoughtService.get_conversation(conversation_id)
    if not conversation:
         raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Enqueue task
    q_generation = Queue('generation', connection=redis_conn)
    q_generation.enqueue("workers.tasks.generate_conversation_sequence", conversation_id, request.persona_ids)
    
    return {"message": "Message sequence generation passed to worker"}


@app.post("/conversations/{conversation_id}/personas")
def add_persona_to_conversation(conversation_id: int, request: AddPersonaToConversationRequest):
    success = ThoughtService.add_persona_to_conversation(conversation_id, request.persona_id)
    if not success:
         raise HTTPException(status_code=400, detail="Could not add persona to conversation. Check IDs.")
    return {"message": "Persona added successfully"}

@app.post("/conversations/{conversation_id}/end")
def end_conversation(conversation_id: int):
    success = ThoughtService.end_conversation(conversation_id)
    if not success:
         raise HTTPException(status_code=400, detail="Could not end conversation.")
    return {"message": "Conversation ended and thoughts created"}
