from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel as PydanticBaseModel
from .models import Thought, Tag, ThoughtTag, Emotion, ThoughtEmotion, ThoughtLink, Persona, db as peewee_db

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
    title: str
    content: str
    status: str
    is_generated: bool
    created_at: datetime
    updated_at: datetime
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
            title=thought.title,
            content=thought.content,
            status=thought.status,
            is_generated=thought.is_generated,
            created_at=thought.created_at,
            updated_at=thought.updated_at,
            emotions=[EmotionDomain(name=te.emotion.name, is_generated=te.is_generated) for te in thought.emotions],
            tags=[TagDomain(name=tt.tag.name, is_generated=tt.is_generated) for tt in thought.tags],
            links=[tl.target.id for tl in thought.links_from],
            persona=PersonaDomain.from_orm(thought.persona) if thought.persona else None
        )

    @classmethod
    def create_persona(cls, name: str, age: int, gender: str) -> PersonaDomain:
        persona = Persona.create(name=name, age=age, gender=gender)
        return PersonaDomain.from_orm(persona)

    @classmethod
    def list_personas(cls) -> List[PersonaDomain]:
        personas = Persona.select()
        return [PersonaDomain.from_orm(p) for p in personas]

    @classmethod
    def get_persona(cls, persona_id: int) -> Optional[PersonaDomain]:
        try:
            persona = Persona.get_by_id(persona_id)
            return PersonaDomain.from_orm(persona)
        except Persona.DoesNotExist:
            return None

    @classmethod
    def create_thought(cls, title: str, content: str, emotions: List[str] = [], is_generated: bool = False, persona_id: Optional[int] = None) -> ThoughtDomain:
        with peewee_db.atomic():
            persona = None
            if persona_id:
                try:
                    persona = Persona.get_by_id(persona_id)
                except Persona.DoesNotExist:
                    pass

            thought = Thought.create(
                title=title,
                content=content,
                is_generated=is_generated,
                persona=persona
            )
            for emotion_name in emotions:
                emotion, _ = Emotion.get_or_create(name=emotion_name.lower())
                ThoughtEmotion.create(thought=thought, emotion=emotion, is_generated=False)
            return cls._map_to_domain(thought)

    @classmethod
    def list_thoughts(cls, tag: Optional[str] = None, emotion: Optional[str] = None, page: int = 1, limit: int = 10):
        query = Thought.select()
        if tag:
            query = query.join(ThoughtTag).join(Tag).where(Tag.name == tag.lower())
        if emotion:
            query = query.join(ThoughtEmotion, on=(Thought.id == ThoughtEmotion.thought)).join(Emotion).where(Emotion.name == emotion.lower())
        
        total_count = query.count()
        thoughts = query.order_by(Thought.created_at.desc()).paginate(page, limit)
        
        return {
            "total": total_count,
            "items": [cls._map_to_domain(t) for t in thoughts]
        }

    @classmethod
    def get_thought(cls, thought_id: int) -> Optional[ThoughtDomain]:
        try:
            thought = Thought.get_by_id(thought_id)
            return cls._map_to_domain(thought)
        except Thought.DoesNotExist:
            return None

    @classmethod
    def add_tags(cls, thought_id: int, tags_list: List[str], is_generated: bool = False) -> bool:
        try:
            with peewee_db.atomic():
                thought = Thought.get_by_id(thought_id)
                for tag_name in tags_list:
                    tag, _ = Tag.get_or_create(name=tag_name.lower())
                    ThoughtTag.get_or_create(thought=thought, tag=tag, defaults={'is_generated': is_generated})
                return True
        except Exception:
            return False

    @classmethod
    def add_emotions(cls, thought_id: int, emotions_list: List[str], is_generated: bool = False) -> bool:
        try:
            with peewee_db.atomic():
                thought = Thought.get_by_id(thought_id)
                for emotion_name in emotions_list:
                    emotion, _ = Emotion.get_or_create(name=emotion_name.lower())
                    ThoughtEmotion.get_or_create(thought=thought, emotion=emotion, defaults={'is_generated': is_generated})
                return True
        except Exception:
            return False

    @classmethod
    def link_thoughts(cls, source_id: int, target_id: int) -> bool:
        try:
            source = Thought.get_by_id(source_id)
            target = Thought.get_by_id(target_id)
            
            if source.id == target.id:
                return False
            
            if source.links_from.count() >= 3:
                return False
                
            ThoughtLink.get_or_create(source=source, target=target)
            return True
        except Thought.DoesNotExist:
            return False

    @classmethod
    def update_status(cls, thought_id: int, status: str) -> bool:
        try:
            if peewee_db.is_closed():
                peewee_db.connect()
            
            thought = Thought.get_by_id(thought_id)
            thought.status = status
            thought.save()
            return True
        except Thought.DoesNotExist:
            return False

    @classmethod
    def delete_thought(cls, thought_id: int) -> bool:
        try:
            with peewee_db.atomic():
                thought = Thought.get_by_id(thought_id)
                # Dependencies like tags/emotions/links are handled by foreign key constraints
                # or we can manually delete if cascade is not set. 
                # Assuming cascade or simple delete for now. 
                # Peewee default is CASCADE for ForeignKeyField if on_delete is not specified? No, usually RESTRICT.
                # Use recursive delete to be safe or rely on DB.
                # Because we didn't specify on_delete='CASCADE', we might need to delete related items manually
                # But let's try simple delete first.
                thought.delete_instance(recursive=True) 
                return True
        except Thought.DoesNotExist:
            return False

    @classmethod
    def update_thought(cls, thought_id: int, updates: dict) -> Optional[ThoughtDomain]:
        try:
            with peewee_db.atomic():
                thought = Thought.get_by_id(thought_id)
                
                # Check for restricted fields just in case, though handled layer above usually
                # But service layer should be robust.
                # However, requirements say "Updating a thought should not allow changes to the content or the title"
                # so we can filter here too.
                
                valid_updates = {k: v for k, v in updates.items() if k not in ['title', 'content', 'id', 'created_at']}
                
                if not valid_updates and not updates:
                     # no valid updates
                     return cls._map_to_domain(thought)

                query = Thought.update(**valid_updates).where(Thought.id == thought_id)
                query.execute()
                
                # Refresh
                thought = Thought.get_by_id(thought_id)
                return cls._map_to_domain(thought)
        except Thought.DoesNotExist:
            return None

def init_database():
    from .models import init_db
    init_db()

def get_db():
    return peewee_db
