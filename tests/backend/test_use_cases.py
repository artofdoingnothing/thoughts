from unittest.mock import patch, MagicMock
from libs.use_cases.conversation_use_cases import ConversationUseCases
from libs.use_cases.generation_use_cases import GenerationUseCases
from libs.use_cases.thought_use_cases import ThoughtUseCases

@patch("libs.use_cases.conversation_use_cases.ConversationService")
@patch("libs.use_cases.conversation_use_cases.PersonaService")
@patch("libs.use_cases.conversation_use_cases.ProcessorService")
def test_generate_conversation_message(mock_processor, mock_persona_service, mock_conversation_service):
    mock_conversation = MagicMock()
    mock_conversation.messages = []
    mock_conversation.personas = []
    mock_conversation.context = "Context"
    
    mock_persona = MagicMock()
    mock_persona.name = "Test"
    mock_persona.age = 30
    mock_persona.gender = "male"
    mock_persona.profile = {}
    
    mock_conversation_service.get_conversation.return_value = mock_conversation
    mock_persona_service.get_persona.return_value = mock_persona
    
    mock_proc_instance = MagicMock()
    mock_proc_instance.generate_conversation_message.return_value = ["Test message"]
    mock_processor.return_value = mock_proc_instance
    
    uc = ConversationUseCases()
    result = uc.generate_conversation_message(1, 1)
    
    assert result == ["Test message"]
    mock_conversation_service.add_message.assert_called_once()


@patch("libs.use_cases.generation_use_cases.requests.get")
@patch("libs.use_cases.generation_use_cases.ProcessorService")
def test_parse_blog(mock_processor, mock_requests_get):
    mock_response = MagicMock()
    mock_response.content = b"<html><body><p>Test paragraph</p></body></html>"
    mock_requests_get.return_value = mock_response
    
    uc = GenerationUseCases()
    result = uc.parse_blog("http://example.com")
    
    assert "Test paragraph" in result


@patch("libs.use_cases.generation_use_cases.PersonaService")
@patch("libs.use_cases.generation_use_cases.ProcessorService")
def test_generate_essay(mock_processor, mock_persona_service):
    mock_persona = MagicMock()
    mock_persona.name = "Test"
    mock_persona.age = 30
    mock_persona.gender = "male"
    mock_persona.profile = {"topic": "value"}
    mock_persona_service.get_persona.return_value = mock_persona
    
    mock_proc_instance = MagicMock()
    mock_proc_instance.extract_emotions_from_profile.return_value = ["happy"]
    mock_proc_instance.complete_essay_with_profile.return_value = "Final essay"
    mock_processor.return_value = mock_proc_instance
    
    uc = GenerationUseCases()
    result = uc.generate_essay(1, "Starting text")
    
    assert result == "Final essay"


@patch("libs.use_cases.thought_use_cases.ThoughtService")
@patch("libs.use_cases.thought_use_cases.ProcessorService")
def test_analyze_cognitive_distortions(mock_processor, mock_thought_service):
    mock_thought = MagicMock()
    mock_thought.content = "Test content"
    mock_thought_service.get_thought.return_value = mock_thought
    
    mock_proc_instance = MagicMock()
    mock_proc_instance.analyze_cognitive_distortions.return_value = ["distortion1"]
    mock_processor.return_value = mock_proc_instance
    
    uc = ThoughtUseCases()
    result = uc.analyze_cognitive_distortions(1)
    
    assert result == ["distortion1"]
    mock_thought_service.add_tags.assert_called_once()
    mock_thought_service.update_status.assert_called_once()
