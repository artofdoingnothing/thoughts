from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from .models import SessionLocal, Conversation, Persona, Message
from .dto import ConversationDomain, MessageDomain
from libs.events.bus import DomainEventBus
from libs.events.conversation_events import ConversationEndedEvent

class ConversationService:
    @staticmethod
    def _map_conversation_to_domain(conversation: Conversation) -> ConversationDomain:
        return ConversationDomain(
            id=conversation.id,
            title=conversation.title,
            context=conversation.context,
            created_at=conversation.created_at,
            messages=[MessageDomain.model_validate(m) for m in conversation.messages],
            personas=[m for m in conversation.personas]  # Handled by Pydantic validation if it's ORM model
        )

    @classmethod
    def create_conversation(cls, title: str, context: str, persona_ids: List[int]) -> Optional[ConversationDomain]:
        try:
            with SessionLocal() as session:
                personas = session.scalars(select(Persona).where(Persona.id.in_(persona_ids))).all()
                if len(personas) != len(persona_ids):
                    return None

                conversation = Conversation(title=title, context=context)
                conversation.personas = personas
                session.add(conversation)
                session.commit()
                
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
                
                if persona in conversation.personas:
                    return True
                
                conversation.personas.append(persona)
                session.commit()
                return True
        except Exception as e:
            print(f"Error adding persona to conversation: {e}")
            return False

    @classmethod
    def end_conversation(cls, conversation_id: int) -> bool:
        try:
            with SessionLocal() as session:
                conversation = session.get(Conversation, conversation_id)
                if not conversation:
                    return False
                
                # Publish the domain event so thoughts are processed asynchronously 
                event = ConversationEndedEvent(conversation_id=conversation_id)
                DomainEventBus.publish("ConversationEndedEvent", event)
                
                return True
        except Exception as e:
            print(f"Error ending conversation: {e}")
            return False
