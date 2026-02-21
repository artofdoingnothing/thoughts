from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import thought_router, persona_router, conversation_router, processor_router
from libs.events.handlers import register_handlers

app = FastAPI(title="Thought Aggregator API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    register_handlers()

@app.get("/")
def read_root():
    return {"message": "Welcome to Thought Aggregator API"}

app.include_router(thought_router)
app.include_router(persona_router)
app.include_router(conversation_router)
app.include_router(processor_router)
