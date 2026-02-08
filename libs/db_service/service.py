from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import create_engine, select, func, update, delete
from sqlalchemy.orm import sessionmaker, Session, joinedload
from pydantic import BaseModel as PydanticBaseModel
from .models import Thought, Tag, ThoughtTag, Emotion, ThoughtEmotion, ThoughtLink, Persona, SessionLocal

# Domain models (DTOs)
class TagDomain(PydanticBaseModel):
    name: str
    is_generated: bool

class EmotionDomain(PydanticBaseModel):
    name: str
    is_generated: bool

class PersonaDomain(PydanticBaseModel):
    id: int
    name: str
    age: int
    gender: str

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
    links: List[int] = []
    persona: Optional[PersonaDomain] = None

    class Config:
        from_attributes = True

class ThoughtService:
    @staticmethod
    def _map_to_domain(thought: Thought) -> ThoughtDomain:
        return ThoughtDomain(
            id=thought.id,
            content=thought.content,
            status=thought.status,
            is_generated=thought.is_generated,
            action_orientation=thought.action_orientation,
            thought_type=thought.thought_type,
            created_at=thought.created_at,
            updated_at=thought.updated_at,
            emotions=[EmotionDomain(name=te.emotion.name, is_generated=te.is_generated) for te in thought.emotions],
            tags=[TagDomain(name=tt.tag.name, is_generated=tt.is_generated) for tt in thought.tags],
            links=[tl.target_thought.id for tl in thought.links_from],
            persona=PersonaDomain.model_validate(thought.persona) if thought.persona else None
        )

    @classmethod
    def create_persona(cls, name: str, age: int, gender: str) -> PersonaDomain:
        with SessionLocal() as session:
            persona = Persona(name=name, age=age, gender=gender)
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
    def create_thought(
        cls, 
        content: str, 
        emotions: List[str] = [], 
        is_generated: bool = False, 
        persona_id: Optional[int] = None,
        action_orientation: Optional[str] = None,
        thought_type: Optional[str] = None
    ) -> ThoughtDomain:
        with SessionLocal() as session:
            persona = None
            if persona_id:
                persona = session.get(Persona, persona_id)

            thought = Thought(
                content=content,
                is_generated=is_generated,
                persona_id=persona.id if persona else None,
                action_orientation=action_orientation,
                thought_type=thought_type
            )
            session.add(thought)
            session.flush() # Flush to get ID

            for emotion_name in emotions:
                stmt = select(Emotion).where(Emotion.name == emotion_name.lower())
                emotion = session.scalar(stmt)
                if not emotion:
                    emotion = Emotion(name=emotion_name.lower())
                    session.add(emotion)
                    session.flush()
                
                # Check if exists
                stmt_te = select(ThoughtEmotion).where(
                    ThoughtEmotion.thought_id == thought.id,
                    ThoughtEmotion.emotion_id == emotion.id
                )
                if not session.scalar(stmt_te):
                    te = ThoughtEmotion(thought_id=thought.id, emotion_id=emotion.id, is_generated=False)
                    session.add(te)

            session.commit()
            
            # Re-fetch with relationships for domain mapping
            # We need to eager load purely for the map_to_domain to work without session issues if we were passing objects around
            # But since we map inside the session context here, it's fine.
            # Ideally we should use session.refresh or a new query.
            stmt = select(Thought).where(Thought.id == thought.id).options(
                joinedload(Thought.emotions).joinedload(ThoughtEmotion.emotion),
                joinedload(Thought.tags).joinedload(ThoughtTag.tag),
                joinedload(Thought.links_from).joinedload(ThoughtLink.target_thought),
                joinedload(Thought.persona)
            )
            thought = session.scalar(stmt)
            return cls._map_to_domain(thought)

    @classmethod
    def list_thoughts(cls, tag: Optional[str] = None, emotion: Optional[str] = None, page: int = 1, limit: int = 10):
        with SessionLocal() as session:
            query = select(Thought).options(
                joinedload(Thought.emotions).joinedload(ThoughtEmotion.emotion),
                joinedload(Thought.tags).joinedload(ThoughtTag.tag),
                joinedload(Thought.links_from).joinedload(ThoughtLink.target_thought),
                joinedload(Thought.persona)
            )
            
            if tag:
                query = query.join(Thought.tags).join(ThoughtTag.tag).where(Tag.name == tag.lower())
            if emotion:
                query = query.join(Thought.emotions).join(ThoughtEmotion.emotion).where(Emotion.name == emotion.lower())
            
            # Count
            # Optimized count: select(func.count()).select_from(query.subquery())
            # Simple list fetch for now
            # Note: Pagination in SQLAlchemy with joins can be tricky for total count.
            # Let's do a separate count query.
            # Using subquery for count correctnes with joins
            
            # Actually easier to use session.scalar(select(func.count()).where(...)) but we need to duplicate logic
            # For simplicity let's execute the filtered query without pagination to count (not efficient but safe for small data)
            # Or construct a count query.
            
            # Building predicates first
            predicates = []
            if tag:
                # This logic is slightly different than above, constructing it manually
                # Join is needed for filtering
                pass 

            # Let's stick to the join construction
            count_query = select(func.count(Thought.id))
            if tag:
                count_query = count_query.join(Thought.tags).join(ThoughtTag.tag).where(Tag.name == tag.lower())
            if emotion:
                count_query = count_query.join(Thought.emotions).join(ThoughtEmotion.emotion).where(Emotion.name == emotion.lower())
            
            total_count = session.scalar(count_query)

            query = query.order_by(Thought.created_at.desc()).offset((page - 1) * limit).limit(limit)
            thoughts = session.scalars(query).unique().all()
            
            return {
                "total": total_count,
                "items": [cls._map_to_domain(t) for t in thoughts]
            }

    @classmethod
    def get_thought(cls, thought_id: int) -> Optional[ThoughtDomain]:
        with SessionLocal() as session:
            stmt = select(Thought).where(Thought.id == thought_id).options(
                joinedload(Thought.emotions).joinedload(ThoughtEmotion.emotion),
                joinedload(Thought.tags).joinedload(ThoughtTag.tag),
                joinedload(Thought.links_from).joinedload(ThoughtLink.target_thought),
                joinedload(Thought.persona)
            )
            thought = session.scalar(stmt)
            return cls._map_to_domain(thought) if thought else None

    @classmethod
    def add_tags(cls, thought_id: int, tags_list: List[str], is_generated: bool = False) -> bool:
        try:
            with SessionLocal() as session:
                thought = session.get(Thought, thought_id)
                if not thought:
                    return False
                
                for tag_name in tags_list:
                    tag = session.scalar(select(Tag).where(Tag.name == tag_name.lower()))
                    if not tag:
                        tag = Tag(name=tag_name.lower())
                        session.add(tag)
                        session.flush()
                    
                    stmt_tt = select(ThoughtTag).where(
                        ThoughtTag.thought_id == thought.id,
                        ThoughtTag.tag_id == tag.id
                    )
                    if not session.scalar(stmt_tt):
                        tt = ThoughtTag(thought_id=thought.id, tag_id=tag.id, is_generated=is_generated)
                        session.add(tt)
                session.commit()
                return True
        except Exception:
            return False

    @classmethod
    def add_emotions(cls, thought_id: int, emotions_list: List[str], is_generated: bool = False) -> bool:
        try:
            with SessionLocal() as session:
                thought = session.get(Thought, thought_id)
                if not thought:
                    return False

                for emotion_name in emotions_list:
                    emotion = session.scalar(select(Emotion).where(Emotion.name == emotion_name.lower()))
                    if not emotion:
                        emotion = Emotion(name=emotion_name.lower())
                        session.add(emotion)
                        session.flush()

                    stmt_te = select(ThoughtEmotion).where(
                        ThoughtEmotion.thought_id == thought.id,
                        ThoughtEmotion.emotion_id == emotion.id
                    )
                    if not session.scalar(stmt_te):
                        te = ThoughtEmotion(thought_id=thought.id, emotion_id=emotion.id, is_generated=is_generated)
                        session.add(te)
                session.commit()
                return True
        except Exception:
            return False

    @classmethod
    def link_thoughts(cls, source_id: int, target_id: int) -> bool:
        if source_id == target_id:
            return False
            
        try:
            with SessionLocal() as session:
                source = session.get(Thought, source_id)
                target = session.get(Thought, target_id)
                
                if not source or not target:
                    return False
                
                # Check link count
                # Need to count existing links_from
                link_count = session.scalar(select(func.count(ThoughtLink.id)).where(ThoughtLink.source_id == source_id))
                if link_count >= 3:
                     return False

                # Check existing link
                existing = session.scalar(select(ThoughtLink).where(ThoughtLink.source_id == source_id, ThoughtLink.target_id == target_id))
                if existing:
                    return True # Idempotent

                link = ThoughtLink(source_id=source_id, target_id=target_id)
                session.add(link)
                session.commit()
                return True
        except Exception:
            return False

    @classmethod
    def update_status(cls, thought_id: int, status: str) -> bool:
        try:
            with SessionLocal() as session:
                stmt = update(Thought).where(Thought.id == thought_id).values(status=status)
                result = session.execute(stmt)
                session.commit()
                return result.rowcount > 0
        except Exception:
            return False

    @classmethod
    def delete_thought(cls, thought_id: int) -> bool:
        try:
            with SessionLocal() as session:
                thought = session.get(Thought, thought_id)
                if not thought:
                    return False
                session.delete(thought)
                session.commit()
                return True
        except Exception:
            return False

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
    def update_thought(cls, thought_id: int, updates: dict) -> Optional[ThoughtDomain]:
        try:
            with SessionLocal() as session:
                valid_updates = {k: v for k, v in updates.items() if k not in ['content', 'id', 'created_at']}
                
                if not valid_updates and not updates:
                     # Just return current
                     thought = session.get(Thought, thought_id)
                     return cls._map_to_domain(thought) if thought else None

                stmt = update(Thought).where(Thought.id == thought_id).values(**valid_updates)
                result = session.execute(stmt)
                session.commit()
                
                if result.rowcount == 0:
                    return None
                    
                # Fetch updated
                updated = session.get(Thought, thought_id)
                return cls._map_to_domain(updated)
        except Exception:
            return None

    @classmethod
    def get_persona_metrics(cls, persona_id: int) -> dict:
        try:
            with SessionLocal() as session:
                persona = session.get(Persona, persona_id)
                if not persona:
                     return {"top_emotions": [], "top_tags": []}

                # Top emotions
                # Select emotion.name, count() from emotion join thoughtemotion join thought where thought.persona_id = ... group by emotion.name order by count desc
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

                # Top tags
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

def init_database():
    # from .models import init_db
    # init_db()
    pass

def get_db():
    return SessionLocal
