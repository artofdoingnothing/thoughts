from typing import List, Optional, Dict, Any
from sqlalchemy import select, func, update, delete
from sqlalchemy.orm import joinedload
from .models import Thought, Tag, ThoughtTag, Emotion, ThoughtEmotion, ThoughtLink, Persona, Topic, ThoughtTopic, SessionLocal
from .dto import ThoughtDomain, EmotionDomain, TagDomain, TopicDomain, PersonaDomain

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
            topics=[TopicDomain(name=tt.topic.name, is_generated=tt.is_generated) for tt in thought.topics],
            links=[tl.target_thought.id for tl in thought.links_from],
            persona=PersonaDomain.model_validate(thought.persona) if thought.persona else None
        )

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
            session.flush() 

            for emotion_name in emotions:
                stmt = select(Emotion).where(Emotion.name == emotion_name.lower())
                emotion = session.scalar(stmt)
                if not emotion:
                    emotion = Emotion(name=emotion_name.lower())
                    session.add(emotion)
                    session.flush()
                
                stmt_te = select(ThoughtEmotion).where(
                    ThoughtEmotion.thought_id == thought.id,
                    ThoughtEmotion.emotion_id == emotion.id
                )
                if not session.scalar(stmt_te):
                    te = ThoughtEmotion(thought_id=thought.id, emotion_id=emotion.id, is_generated=False)
                    session.add(te)

            session.commit()
            
            stmt = select(Thought).where(Thought.id == thought.id).options(
                joinedload(Thought.emotions).joinedload(ThoughtEmotion.emotion),
                joinedload(Thought.tags).joinedload(ThoughtTag.tag),
                joinedload(Thought.topics).joinedload(ThoughtTopic.topic),
                joinedload(Thought.links_from).joinedload(ThoughtLink.target_thought),
                joinedload(Thought.persona)
            )
            thought = session.scalar(stmt)
            return cls._map_to_domain(thought)

    @classmethod
    def list_thoughts(cls, tag: Optional[str] = None, emotion: Optional[str] = None, persona_id: Optional[int] = None, page: int = 1, limit: int = 10):
        with SessionLocal() as session:
            query = select(Thought).options(
                joinedload(Thought.emotions).joinedload(ThoughtEmotion.emotion),
                joinedload(Thought.tags).joinedload(ThoughtTag.tag),
                joinedload(Thought.topics).joinedload(ThoughtTopic.topic),
                joinedload(Thought.links_from).joinedload(ThoughtLink.target_thought),
                joinedload(Thought.persona)
            )
            
            count_query = select(func.count(Thought.id))
            if tag:
                query = query.join(Thought.tags).join(ThoughtTag.tag).where(Tag.name == tag.lower())
                count_query = count_query.join(Thought.tags).join(ThoughtTag.tag).where(Tag.name == tag.lower())
            if emotion:
                query = query.join(Thought.emotions).join(ThoughtEmotion.emotion).where(Emotion.name == emotion.lower())
                count_query = count_query.join(Thought.emotions).join(ThoughtEmotion.emotion).where(Emotion.name == emotion.lower())
            if persona_id:
                query = query.where(Thought.persona_id == persona_id)
                count_query = count_query.where(Thought.persona_id == persona_id)
            
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
                joinedload(Thought.topics).joinedload(ThoughtTopic.topic),
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
    def add_topics(cls, thought_id: int, topics_list: List[str], is_generated: bool = False) -> bool:
        try:
            with SessionLocal() as session:
                thought = session.get(Thought, thought_id)
                if not thought:
                    return False
                
                for topic_name in topics_list:
                    topic = session.scalar(select(Topic).where(Topic.name == topic_name.lower()))
                    if not topic:
                        topic = Topic(name=topic_name.lower())
                        session.add(topic)
                        session.flush()
                    
                    stmt_tt = select(ThoughtTopic).where(
                        ThoughtTopic.thought_id == thought.id,
                        ThoughtTopic.topic_id == topic.id
                    )
                    if not session.scalar(stmt_tt):
                        tt = ThoughtTopic(thought_id=thought.id, topic_id=topic.id, is_generated=is_generated)
                        session.add(tt)
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
                
                link_count = session.scalar(select(func.count(ThoughtLink.id)).where(ThoughtLink.source_id == source_id))
                if link_count >= 3:
                     return False

                existing = session.scalar(select(ThoughtLink).where(ThoughtLink.source_id == source_id, ThoughtLink.target_id == target_id))
                if existing:
                    return True 

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
    def update_thought(cls, thought_id: int, updates: dict) -> Optional[ThoughtDomain]:
        try:
            with SessionLocal() as session:
                valid_updates = {k: v for k, v in updates.items() if k not in ['content', 'id', 'created_at']}
                
                if not valid_updates and not updates:
                     thought = session.get(Thought, thought_id)
                     return cls._map_to_domain(thought) if thought else None

                stmt = update(Thought).where(Thought.id == thought_id).values(**valid_updates)
                result = session.execute(stmt)
                session.commit()
                
                if result.rowcount == 0:
                    return None
                    
                updated = session.get(Thought, thought_id)
                return cls._map_to_domain(updated)
        except Exception:
            return None

    @classmethod
    def find_closest_thought_by_tags(cls, tags: List[str], persona_id: int) -> Optional[ThoughtDomain]:
        if not tags:
            return None
            
        try:
            with SessionLocal() as session:
                stmt = (
                    select(Thought)
                    .join(ThoughtTag)
                    .join(Tag)
                    .where(
                        Thought.persona_id == persona_id,
                        Tag.name.in_([t.lower() for t in tags])
                    )
                    .group_by(Thought.id)
                    .order_by(func.count(ThoughtTag.id).desc())
                    .limit(1)
                    .options(
                        joinedload(Thought.emotions).joinedload(ThoughtEmotion.emotion),
                        joinedload(Thought.tags).joinedload(ThoughtTag.tag),
                        joinedload(Thought.topics).joinedload(ThoughtTopic.topic),
                        joinedload(Thought.links_from).joinedload(ThoughtLink.target_thought),
                        joinedload(Thought.persona)
                    )
                )
                
                thought = session.scalar(stmt)
                return cls._map_to_domain(thought) if thought else None
        except Exception as e:
            print(f"Error finding closest thought: {e}")
            return None

def init_database():
    pass

def get_db():
    return SessionLocal
