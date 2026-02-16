from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import create_engine, select, func, update, delete
from sqlalchemy.orm import sessionmaker, Session, joinedload
from pydantic import BaseModel as PydanticBaseModel
from .models import Thought, Tag, ThoughtTag, Emotion, ThoughtEmotion, ThoughtLink, Persona, Topic, ThoughtTopic, SessionLocal, Conversation, Message
import random
import json
from libs.llm_service.gemini import GeminiLLM

# Domain models (DTOs)
class TagDomain(PydanticBaseModel):
    name: str
    is_generated: bool

class EmotionDomain(PydanticBaseModel):
    name: str
    is_generated: bool

class TopicDomain(PydanticBaseModel):
    name: str
    is_generated: bool

class PersonaDomain(PydanticBaseModel):
    id: int
    name: str
    age: int
    gender: str
    profile: Optional[Dict[str, Any]] = None
    additional_info: Optional[Dict[str, Any]] = None

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
    topics: List[TopicDomain] = []
    links: List[int] = []
    persona: Optional[PersonaDomain] = None

    class Config:
        from_attributes = True

class MessageDomain(PydanticBaseModel):
    id: int
    content: str
    is_generated: bool
    created_at: datetime
    persona_id: int
    conversation_id: int
    persona: Optional[PersonaDomain] = None

    class Config:
        from_attributes = True

class ConversationDomain(PydanticBaseModel):
    id: int
    title: str
    context: Optional[str] = None
    created_at: datetime
    messages: List[MessageDomain] = []
    personas: List[PersonaDomain] = []

    class Config:
        from_attributes = True

class ThoughtService:
    @staticmethod
    def _map_conversation_to_domain(conversation: Conversation) -> ConversationDomain:
        return ConversationDomain(
            id=conversation.id,
            title=conversation.title,
            context=conversation.context,
            created_at=conversation.created_at,
            messages=[MessageDomain.model_validate(m) for m in conversation.messages],
            personas=[PersonaDomain.model_validate(p) for p in conversation.personas]
        )

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
    def create_persona(cls, name: str, age: int, gender: str, additional_info: Optional[Dict[str, Any]] = None) -> PersonaDomain:
        with SessionLocal() as session:
            persona = Persona(name=name, age=age, gender=gender, additional_info=additional_info)
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
            
            if tag:
                query = query.join(Thought.tags).join(ThoughtTag.tag).where(Tag.name == tag.lower())
            if emotion:
                query = query.join(Thought.emotions).join(ThoughtEmotion.emotion).where(Emotion.name == emotion.lower())
            if persona_id:
                query = query.where(Thought.persona_id == persona_id)
            
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
            if persona_id:
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

    @classmethod
    def get_persona_unique_attributes(cls, persona_id: int) -> dict:
        try:
            with SessionLocal() as session:
                # Get distinct values
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
    def find_closest_thought_by_tags(cls, tags: List[str], persona_id: int) -> Optional[ThoughtDomain]:
        if not tags:
            return None
            
        try:
            with SessionLocal() as session:
                # Find thought with most matching tags
                # Select thought_id, count(tag_id) from thought_tag join tag where tag.name in tags group by thought_id order by count desc limit 1
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

    @classmethod
    def derive_persona(cls, source_persona_id: int, name_adjective: str, percentage: int) -> Optional[PersonaDomain]:
        try:
            with SessionLocal() as session:
                source_persona = session.get(Persona, source_persona_id)
                if not source_persona:
                    return None

                # Fetch all thoughts
                thoughts = session.scalars(select(Thought).where(Thought.persona_id == source_persona_id)).all()
                if not thoughts:
                    # Allow deriving even if no thoughts, maybe? But the requirement says "from a limited set of random thoughts"
                    # If no thoughts, we can't derive based on thoughts.
                    # But maybe we just clone with new name?
                    # Let's return None for now as it seems to rely on thoughts.
                    return None 

                # Sample thoughts
                k = int(len(thoughts) * (percentage / 100))
                # Ensure at least 1 thought if available, or if percentage is 0, then 0?
                # User inputs percentage.
                if k < 1 and percentage > 0: k = 1
                sampled_thoughts = random.sample(thoughts, min(k, len(thoughts)))

                if not sampled_thoughts:
                     thought_texts = []
                else:
                    thought_texts = [t.content for t in sampled_thoughts]
                
                profile_data = cls._generate_profile_from_thoughts(thought_texts)
                if not profile_data:
                     # Fallback or error?
                     # Let's proceed with empty profile or try again?
                     # For now, if LLM fails, we might return None or empty dict.
                     # derive_persona expects a profile.
                     return None

                new_name = f"{name_adjective} {source_persona.name}"
                
                new_persona = Persona(
                    name=new_name,
                    age=source_persona.age,
                    gender=source_persona.gender,
                    profile=profile_data,
                    additional_info=source_persona.additional_info
                )
                session.add(new_persona)
                session.commit()
                session.refresh(new_persona)
                
                return PersonaDomain.model_validate(new_persona)

        except Exception as e:
            print(f"Error deriving persona: {e}")
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
            
            # Cleanup potential markdown formatting
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0].strip()
            
            return json.loads(response_text)
        except Exception as e:
            print(f"Error generating profile: {e}")
            return None

    @classmethod
    def regenerate_persona(cls, persona_id: int) -> Optional[PersonaDomain]:
        try:
            with SessionLocal() as session:
                persona = session.get(Persona, persona_id)
                if not persona:
                    return None
                
                # Fetch all thoughts
                thoughts = session.scalars(select(Thought).where(Thought.persona_id == persona_id)).all()
                if not thoughts:
                    # No thoughts to regenerate from?
                    return None
                
                thought_texts = [t.content for t in thoughts]
                
                new_profile = cls._generate_profile_from_thoughts(thought_texts)
                if not new_profile:
                     return None
                
                # Update persona
                persona.profile = new_profile
                session.add(persona)
                session.commit()
                session.refresh(persona)
                
                return PersonaDomain.model_validate(persona)
        except Exception as e:
            print(f"Error regenerating persona: {e}")
            return None

    @classmethod
    def create_conversation(cls, title: str, context: str, persona_ids: List[int]) -> Optional[ConversationDomain]:
        try:
            with SessionLocal() as session:
                personas = session.scalars(select(Persona).where(Persona.id.in_(persona_ids))).all()
                if len(personas) != len(persona_ids):
                    return None # Some personas not found

                conversation = Conversation(title=title, context=context)
                conversation.personas = personas
                session.add(conversation)
                session.commit()
                
                # Fetch with relationships
                stmt = select(Conversation).where(Conversation.id == conversation.id).options(
                    joinedload(Conversation.personas),
                    joinedload(Conversation.messages)
                )
                conversation = session.scalar(stmt)
                return cls._map_conversation_to_domain(conversation)
        except Exception as e:
            print(f"Error creating conversation: {e}")
            return None

    @classmethod
    def list_conversations(cls) -> List[ConversationDomain]:
        try:
            with SessionLocal() as session:
                conversations = session.scalars(
                    select(Conversation).order_by(Conversation.created_at.desc()).options(
                        joinedload(Conversation.personas),
                         joinedload(Conversation.messages).joinedload(Message.persona)
                    )
                ).unique().all()
                return [cls._map_conversation_to_domain(c) for c in conversations]
        except Exception as e:
            print(f"Error listing conversations: {e}")
            return []

    @classmethod
    def get_conversation(cls, conversation_id: int) -> Optional[ConversationDomain]:
        try:
            with SessionLocal() as session:
                stmt = select(Conversation).where(Conversation.id == conversation_id).options(
                    joinedload(Conversation.personas),
                    joinedload(Conversation.messages).joinedload(Message.persona)
                )
                conversation = session.scalar(stmt)
                return cls._map_conversation_to_domain(conversation) if conversation else None
        except Exception as e:
            print(f"Error getting conversation: {e}")
            return None

    @classmethod
    def add_message(cls, conversation_id: int, persona_id: int, content: str, is_generated: bool = False) -> Optional[MessageDomain]:
        try:
            with SessionLocal() as session:
                conversation = session.get(Conversation, conversation_id)
                persona = session.get(Persona, persona_id)
                if not conversation or not persona:
                    return None

                message = Message(
                    conversation_id=conversation_id,
                    persona_id=persona_id,
                    content=content,
                    is_generated=is_generated
                )
                session.add(message)
                session.commit()
                session.refresh(message)
                # Ensure persona is loaded for return
                stmt = select(Message).where(Message.id == message.id).options(joinedload(Message.persona))
                message = session.scalar(stmt)
                return MessageDomain.model_validate(message)
        except Exception as e:
            print(f"Error adding message: {e}")
            return None

    @classmethod
    def add_persona_to_conversation(cls, conversation_id: int, persona_id: int) -> bool:
        try:
            with SessionLocal() as session:
                conversation = session.get(Conversation, conversation_id)
                persona = session.get(Persona, persona_id)
                if not conversation or not persona:
                    return False
                
                # Check if already in conversation
                if persona in conversation.personas:
                    return True # Idempotent
                
                conversation.personas.append(persona)
                session.commit()
                return True
        except Exception as e:
            print(f"Error adding persona to conversation: {e}")
            return False

    @classmethod
    def end_conversation(cls, conversation_id: int) -> bool:
        """
        Ends a conversation by converting all messages into Thoughts for the respective personas.
        """
        try:
            with SessionLocal() as session:
                conversation = session.get(Conversation, conversation_id)
                if not conversation:
                    return False
                
                # Iterate through messages
                # We need to ensure we don't duplicate thoughts if this is called multiple times?
                # The requirement says "On ending...". Maybe we should look if thought already exists?
                # But messages might be identical.
                # Let's assume this is an explicit action.
                # We could add a flag to conversation "ended" or "archived"? 
                # The model doesn't have it. I'll just convert.
                
                messages = conversation.messages
                thoughts_created = 0
                
                for msg in messages:
                    if not msg.persona_id:
                        continue
                        
                    # Create thought
                    thought = Thought(
                        content=msg.content,
                        persona_id=msg.persona_id,
                        is_generated=msg.is_generated,
                        status="completed", # Auto-complete?
                        thought_type="Conversation", # maybe a new type?
                        created_at=msg.created_at # Preserve timestamp?
                    )
                    session.add(thought)
                    thoughts_created += 1
                
                session.commit()
                print(f"Ended conversation {conversation_id}. Created {thoughts_created} thoughts.")
                # Optionally delete conversation? Requirement says "Add an end conversation button... messages will be added as thoughts". 
                # Doesn't explicitly say delete. I'll keep it for now.
                return True
        except Exception as e:
            print(f"Error ending conversation: {e}")
            return False

def init_database():
    # from .models import init_db
    # init_db()
    pass

def get_db():
    return SessionLocal
