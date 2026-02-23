from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table, create_engine, JSON
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from sqlalchemy.sql import func
import os
import datetime

# Database setup
DB_URL = os.getenv("DATABASE_URL", "sqlite:///thoughts.db")

# Sync engine
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

conversation_persona = Table(
    "conversation_persona",
    Base.metadata,
    Column("conversation_id", Integer, ForeignKey("conversation.id"), primary_key=True),
    Column("persona_id", Integer, ForeignKey("persona.id"), primary_key=True)
)

class Persona(Base):
    __tablename__ = "persona"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    profile = Column(JSON, nullable=True)
    additional_info = Column(JSON, nullable=True)
    source = Column(String, default="manual") # manual, derived, movie_generated
    origin_description = Column(String, nullable=True) # character from movie(year)(rating)
    
    thoughts = relationship("Thought", back_populates="persona", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="persona", cascade="all, delete-orphan")
    conversations = relationship("Conversation", secondary=conversation_persona, back_populates="personas")

class Thought(Base):
    __tablename__ = "thought"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    status = Column(String, default="pending")
    is_generated = Column(Boolean, default=False)
    action_orientation = Column(String, nullable=True)
    thought_type = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    persona_id = Column(Integer, ForeignKey("persona.id"), nullable=True)
    
    persona = relationship("Persona", back_populates="thoughts")
    
    # Relationships
    tags = relationship("ThoughtTag", back_populates="thought", cascade="all, delete-orphan")
    emotions = relationship("ThoughtEmotion", back_populates="thought", cascade="all, delete-orphan")
    topics = relationship("ThoughtTopic", back_populates="thought", cascade="all, delete-orphan")
    
    # Self-referential relationship for links
    links_from = relationship(
        "ThoughtLink",
        foreign_keys="ThoughtLink.source_id",
        back_populates="source_thought",
        cascade="all, delete-orphan"
    )
    links_to = relationship(
        "ThoughtLink",
        foreign_keys="ThoughtLink.target_id",
        back_populates="target_thought",
        cascade="all, delete-orphan"
    )

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    thoughts = relationship("ThoughtTag", back_populates="tag")

class ThoughtTag(Base):
    __tablename__ = "thought_tag"
    id = Column(Integer, primary_key=True, index=True)
    thought_id = Column(Integer, ForeignKey("thought.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))
    is_generated = Column(Boolean, default=False)
    
    thought = relationship("Thought", back_populates="tags")
    tag = relationship("Tag", back_populates="thoughts")

class Emotion(Base):
    __tablename__ = "emotion"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    thoughts = relationship("ThoughtEmotion", back_populates="emotion")

class ThoughtEmotion(Base):
    __tablename__ = "thought_emotion"
    id = Column(Integer, primary_key=True, index=True)
    thought_id = Column(Integer, ForeignKey("thought.id"))
    emotion_id = Column(Integer, ForeignKey("emotion.id"))
    is_generated = Column(Boolean, default=False)
    
    thought = relationship("Thought", back_populates="emotions")
    emotion = relationship("Emotion", back_populates="thoughts")

class ThoughtLink(Base):
    __tablename__ = "thought_link"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("thought.id"))
    target_id = Column(Integer, ForeignKey("thought.id"))
    
    source_thought = relationship("Thought", foreign_keys=[source_id], back_populates="links_from")
    target_thought = relationship("Thought", foreign_keys=[target_id], back_populates="links_to")

class Topic(Base):
    __tablename__ = "topic"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    thoughts = relationship("ThoughtTopic", back_populates="topic")

class ThoughtTopic(Base):
    __tablename__ = "thought_topic"
    id = Column(Integer, primary_key=True, index=True)
    thought_id = Column(Integer, ForeignKey("thought.id"))
    topic_id = Column(Integer, ForeignKey("topic.id"))
    is_generated = Column(Boolean, default=False)
    
    thought = relationship("Thought", back_populates="topics")
    topic = relationship("Topic", back_populates="thoughts")

class Conversation(Base):
    __tablename__ = "conversation"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    context = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    personas = relationship("Persona", secondary=conversation_persona, back_populates="conversations")

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    is_generated = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    conversation_id = Column(Integer, ForeignKey("conversation.id"))
    persona_id = Column(Integer, ForeignKey("persona.id"))
    
    conversation = relationship("Conversation", back_populates="messages")
    persona = relationship("Persona", back_populates="messages")

def init_db():
    Base.metadata.create_all(bind=engine)
