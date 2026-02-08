from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table, create_engine
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

class Persona(Base):
    __tablename__ = "persona"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    
    thoughts = relationship("Thought", back_populates="persona", cascade="all, delete-orphan")

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

def init_db():
    Base.metadata.create_all(bind=engine)
