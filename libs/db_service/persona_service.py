from typing import List, Optional, Dict, Any
from sqlalchemy import select, func, update, delete
from sqlalchemy.orm import joinedload
import json
import random
from libs.llm_service.gemini import GeminiLLM
from .models import Persona, SessionLocal, Thought, ThoughtEmotion, ThoughtTag, Emotion, Tag
from .dto import PersonaDomain

class PersonaService:
    @classmethod
    def create_persona(cls, name: str, age: int, gender: str, profile: Optional[Dict[str, Any]] = None, additional_info: Optional[Dict[str, Any]] = None, source: str = "manual") -> PersonaDomain:
        with SessionLocal() as session:
            persona = Persona(name=name, age=age, gender=gender, profile=profile, additional_info=additional_info, source=source)
            session.add(persona)
            session.commit()
            session.refresh(persona)
            return PersonaDomain.model_validate(persona)

    @classmethod
    def list_personas(cls) -> List[PersonaDomain]:
        with SessionLocal() as session:
            personas = session.scalars(select(Persona)).all()
            return [PersonaDomain.model_validate(p) for p in personas]

    @classmethod
    def get_persona(cls, persona_id: int) -> Optional[PersonaDomain]:
        with SessionLocal() as session:
            persona = session.get(Persona, persona_id)
            return PersonaDomain.model_validate(persona) if persona else None

    @classmethod
    def delete_persona(cls, persona_id: int) -> bool:
        try:
            with SessionLocal() as session:
                persona = session.get(Persona, persona_id)
                if not persona:
                    return False
                session.delete(persona)
                session.commit()
                return True
        except Exception:
            return False

    @classmethod
    def update_persona(cls, persona_id: int, updates: dict) -> Optional[PersonaDomain]:
        try:
            with SessionLocal() as session:
                valid_updates = {k: v for k, v in updates.items() if k in ['name', 'age', 'gender', 'additional_info']}
                
                stmt = update(Persona).where(Persona.id == persona_id).values(**valid_updates)
                result = session.execute(stmt)
                session.commit()
                
                if result.rowcount == 0:
                    return None
                    
                persona = session.get(Persona, persona_id)
                return PersonaDomain.model_validate(persona)
        except Exception as e:
            print(f"Error updating persona: {e}")
            return None

    @classmethod
    def get_persona_metrics(cls, persona_id: int) -> dict:
        try:
            with SessionLocal() as session:
                persona = session.get(Persona, persona_id)
                if not persona:
                     return {"top_emotions": [], "top_tags": []}

                stmt_emotions = (
                    select(Emotion.name, func.count(ThoughtEmotion.id).label('count'))
                    .join(ThoughtEmotion)
                    .join(Thought)
                    .where(Thought.persona_id == persona_id)
                    .group_by(Emotion.name)
                    .order_by(func.count(ThoughtEmotion.id).desc())
                    .limit(5)
                )
                emotions = session.execute(stmt_emotions).all()

                stmt_tags = (
                    select(Tag.name, func.count(ThoughtTag.id).label('count'))
                    .join(ThoughtTag)
                    .join(Thought)
                    .where(Thought.persona_id == persona_id)
                    .group_by(Tag.name)
                    .order_by(func.count(ThoughtTag.id).desc())
                    .limit(5)
                )
                tags = session.execute(stmt_tags).all()

                return {
                    "top_emotions": [e.name for e in emotions],
                    "top_tags": [t.name for t in tags]
                }
        except Exception:
             return {"top_emotions": [], "top_tags": []}

    @classmethod
    def get_persona_unique_attributes(cls, persona_id: int) -> dict:
        try:
            with SessionLocal() as session:
                stmt_types = select(Thought.thought_type).where(Thought.persona_id == persona_id).distinct()
                stmt_actions = select(Thought.action_orientation).where(Thought.persona_id == persona_id).distinct()
                
                types = session.scalars(stmt_types).all()
                actions = session.scalars(stmt_actions).all()
                
                return {
                    "thought_types": [t for t in types if t],
                    "action_orientations": [a for a in actions if a]
                }
        except Exception:
            return {"thought_types": [], "action_orientations": []}

    @classmethod
    def derive_persona(cls, source_persona_id: int, name_adjective: str, percentage: int) -> Optional[PersonaDomain]:
        try:
            with SessionLocal() as session:
                source_persona = session.get(Persona, source_persona_id)
                if not source_persona:
                    return None

                thoughts = session.scalars(select(Thought).where(Thought.persona_id == source_persona_id)).all()
                if not thoughts:
                    return None 

                k = int(len(thoughts) * (percentage / 100))
                if k < 1 and percentage > 0: k = 1
                sampled_thoughts = random.sample(thoughts, min(k, len(thoughts)))

                if not sampled_thoughts:
                     thought_texts = []
                else:
                    thought_texts = [t.content for t in sampled_thoughts]
                
                profile_data = cls._generate_profile_from_thoughts(thought_texts)
                if not profile_data:
                     return None

                new_name = f"{name_adjective} {source_persona.name}"
                
                new_persona = Persona(
                    name=new_name,
                    age=source_persona.age,
                    gender=source_persona.gender,
                    profile=profile_data,
                    additional_info=source_persona.additional_info,
                    source="derived"
                )
                session.add(new_persona)
                session.commit()
                session.refresh(new_persona)
                
                return PersonaDomain.model_validate(new_persona)

        except Exception as e:
            print(f"Error deriving persona: {e}")
            return None

    @classmethod
    def regenerate_persona(cls, persona_id: int) -> Optional[PersonaDomain]:
        try:
            with SessionLocal() as session:
                persona = session.get(Persona, persona_id)
                if not persona:
                    return None
                
                thoughts = session.scalars(select(Thought).where(Thought.persona_id == persona_id)).all()
                if not thoughts:
                    return None
                
                thought_texts = [t.content for t in thoughts]
                
                new_profile = cls._generate_profile_from_thoughts(thought_texts)
                if not new_profile:
                     return None
                
                persona.profile = new_profile
                session.add(persona)
                session.commit()
                session.refresh(persona)
                
                return PersonaDomain.model_validate(persona)
        except Exception as e:
            print(f"Error regenerating persona: {e}")
            return None

    @classmethod
    def _generate_profile_from_thoughts(cls, thought_texts: List[str]) -> Optional[Dict[str, Any]]:
        try:
            llm = GeminiLLM()
            prompt = f"""
            Analyze the following thoughts from a persona:
            {json.dumps(thought_texts)}

            Create a generalized profile for a new persona based on these thoughts.
            The specific topics should be merged into broader, generalized topics.
            Map the emotions from the thoughts to these new generalized topics.
            Limit to at most 5 generalized topics.

            Return ONLY a valid JSON object with the following structure:
            {{
                "topics": [
                    {{
                        "name": "Generalized Topic Name",
                        "emotions": ["emotion1", "emotion2"]
                    }}
                ],
                "thought_patterns": "Brief summary of thought patterns",
                "tags": ["tag1", "tag2", "tag3"],
                "thought_type": "Automatic/Deliberate/etc.",
                "action_orientation": "Action-oriented/Ruminative/etc."
            }}
            """
            
            response_text = llm.generate_content(prompt)
            
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            return json.loads(response_text)
        except Exception as e:
            print(f"Error generating profile: {e}")
            return None
