from unittest.mock import patch, MagicMock
from libs.db_service.conversation_service import ConversationService
from libs.db_service.persona_service import PersonaService
from libs.db_service.service import ThoughtService
from libs.db_service.models import Conversation, Persona, Thought
from datetime import datetime

p = Persona(id=1, name="Test Persona", age=30, gender="male", source="manual")
p.created_at = datetime.utcnow()
p.updated_at = datetime.utcnow()
p.profile = {}
p.additional_info = {}

c = Conversation(id=1, title="Test", context="Context")
c.created_at = datetime.utcnow()
c.personas = []
c.messages = []

t = Thought(id=1, persona_id=1, content="Test thought")
t.created_at = datetime.utcnow()
t.updated_at = datetime.utcnow()
t.emotions = []
t.tags = []
t.topics = []
t.links_from = []
t.persona = p
t.status = "new"
t.is_generated = False
t.action_orientation = "none"
t.thought_type = "none"

mock_persona_db = p
mock_conversation_db = c
mock_thought_db = t


@patch("libs.db_service.conversation_service.SessionLocal")
def test_create_conversation(mock_session_local):
    mock_session = MagicMock()
    mock_session_local.return_value.__enter__.return_value = mock_session
    mock_session.scalars.return_value.all.return_value = [mock_persona_db]
    mock_session.scalar.return_value = mock_conversation_db

    result = ConversationService.create_conversation("Title", "Context", [1])
    assert result is not None
    assert result.id == 1
    assert mock_session.commit.called


@patch("libs.db_service.conversation_service.SessionLocal")
def test_list_conversations(mock_session_local):
    mock_session = MagicMock()
    mock_session_local.return_value.__enter__.return_value = mock_session
    mock_session.scalars.return_value.unique.return_value.all.return_value = [mock_conversation_db]

    result = ConversationService.list_conversations()
    assert len(result) == 1
    assert result[0].id == 1


@patch("libs.db_service.persona_service.Persona")
@patch("libs.db_service.persona_service.SessionLocal")
def test_create_persona(mock_session_local, mock_persona_cls):
    mock_session = MagicMock()
    mock_session_local.return_value.__enter__.return_value = mock_session
    mock_persona_cls.return_value = mock_persona_db
    
    PersonaService.create_persona(name="Test", age=25, gender="female")
    assert mock_session.commit.called
    assert mock_session.add.called


@patch("libs.db_service.persona_service.SessionLocal")
def test_list_personas(mock_session_local):
    mock_session = MagicMock()
    mock_session_local.return_value.__enter__.return_value = mock_session
    mock_session.scalars.return_value.all.return_value = [mock_persona_db]

    result = PersonaService.list_personas()
    assert len(result) == 1


@patch("libs.db_service.service.SessionLocal")
def test_create_thought(mock_session_local):
    mock_session = MagicMock()
    mock_session_local.return_value.__enter__.return_value = mock_session
    mock_session.scalar.return_value = mock_thought_db

    result = ThoughtService.create_thought(content="Test", emotions=[])
    assert result is not None
    assert mock_session.commit.called


@patch("libs.db_service.service.SessionLocal")
def test_list_thoughts(mock_session_local):
    mock_session = MagicMock()
    mock_session_local.return_value.__enter__.return_value = mock_session
    mock_session.scalar.return_value = 1
    mock_session.scalars.return_value.unique.return_value.all.return_value = [mock_thought_db]

    result = ThoughtService.list_thoughts()
    assert result["total"] == 1
    assert len(result["items"]) == 1
