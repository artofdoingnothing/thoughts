from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from libs.db_service import PersonaService, PersonaDomain

router = APIRouter(prefix="/personas", tags=["Personas"])

class PersonaCreate(BaseModel):
    name: str 
    age: int
    gender: str
    additional_info: Optional[Dict[str, Any]] = None

class PersonaUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None

class DerivePersonaRequest(BaseModel):
    source_persona_id: int
    name_adjective: str
    percentage: int

@router.get("/", response_model=List[PersonaDomain])
def list_personas():
    return PersonaService.list_personas()

@router.post("/", response_model=PersonaDomain)
def create_persona(persona: PersonaCreate):
    return PersonaService.create_persona(
        name=persona.name,
        age=persona.age,
        gender=persona.gender,
        additional_info=persona.additional_info
    )

@router.put("/{persona_id}", response_model=PersonaDomain)
def update_persona(persona_id: int, persona_update: PersonaUpdate):
    updates = persona_update.dict(exclude_unset=True)
    updated_persona = PersonaService.update_persona(persona_id, updates)
    if not updated_persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return updated_persona

@router.post("/generate-name")
def generate_persona_name():
    from faker import Faker
    try:
        fake = Faker()
        name = fake.name()
        return {"name": name}
    except Exception as e:
        return {"name": "Random Persona"}

@router.delete("/{persona_id}")
def delete_persona(persona_id: int):
    success = PersonaService.delete_persona(persona_id)
    if not success:
        raise HTTPException(status_code=404, detail="Persona not found")
    return {"message": "Persona deleted successfully"}

@router.post("/{persona_id}/regenerate", response_model=PersonaDomain)
def regenerate_persona(persona_id: int):
    updated_persona = PersonaService.regenerate_persona(persona_id)
    if not updated_persona:
         raise HTTPException(status_code=400, detail="Could not regenerate persona. Ensure persona exists and has thoughts.")
    return updated_persona

@router.post("/derive", response_model=PersonaDomain)
def derive_persona(request: DerivePersonaRequest):
    new_persona = PersonaService.derive_persona(
        source_persona_id=request.source_persona_id,
        name_adjective=request.name_adjective,
        percentage=request.percentage
    )
    if not new_persona:
        raise HTTPException(status_code=400, detail="Could not derive persona. Ensure source persona has thoughts.")
    return new_persona
