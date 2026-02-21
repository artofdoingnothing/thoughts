from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from redis import Redis
from rq import Queue
import os

router = APIRouter(tags=["Processor"])

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)

class GenerateThoughtsRequest(BaseModel):
    urls: List[str]
    persona_id: int

class EssayGenerateRequest(BaseModel):
    starting_text: str
    persona_id: int


@router.post("/generate-thoughts/")
def generate_thoughts(request: GenerateThoughtsRequest):
    q_generation = Queue('generation', connection=redis_conn)
    print(f"Received request to generate thoughts for {len(request.urls)} URLs: {request.urls}")
    for url in request.urls:
        print(f"Enqueuing task for {url}")
        q_generation.enqueue("workers.tasks.parse_blog_and_generate_thoughts", url, request.persona_id)
    return {"message": f"{len(request.urls)} thought generation tasks have been queued"}

@router.post("/essay/generate")
def generate_essay_endpoint(request: EssayGenerateRequest):
    q_essay = Queue('essay', connection=redis_conn)
    job = q_essay.enqueue("workers.tasks.generate_essay", request.persona_id, request.starting_text, job_timeout=600)
    return {"job_id": job.id}

@router.get("/essay/status/{job_id}")
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
