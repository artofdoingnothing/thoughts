from unittest.mock import MagicMock, patch
from libs.db_service import ThoughtService
from libs.db_service.models import Persona, Thought



# Checking existing tests might be better to align style.
# But for now let's write a service layer test using sql alchemy mocks or temporary db.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from libs.db_service.models import Base

# Setup in-memory DB
engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

def setup_module(module):
    Base.metadata.create_all(engine)

def teardown_module(module):
    Base.metadata.drop_all(engine)

def test_delete_persona_cascades():
    session = Session()
    
    # Create persona
    p = Persona(name="Test", age=30, gender="M")
    session.add(p)
    session.commit()
    
    # Create thought linked to persona
    t = Thought(title="T1", content="C1", persona_id=p.id)
    session.add(t)
    session.commit()
    
    assert session.query(Persona).count() == 1
    assert session.query(Thought).count() == 1
    
    # Delete persona
    session.delete(p)
    session.commit()
    
    assert session.query(Persona).count() == 0
    assert session.query(Thought).count() == 0 # Verification of cascade
    
    session.close()
