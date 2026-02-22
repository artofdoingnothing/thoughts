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

@patch("libs.dataset_service.movie_dataset_service.MovieDatasetService")
@patch("libs.use_cases.generation_use_cases.ProcessorService")
@patch("libs.use_cases.thought_use_cases.ThoughtUseCases")
@patch("libs.use_cases.generation_use_cases.PersonaService")
def test_generate_persona_from_movie_characters(
    mock_persona_service, mock_thought_uc_class, mock_processor_class, mock_movie_service_class
):
    # Mock movie service
    mock_movie_service = MagicMock()
    mock_movie_service.get_character_dialogues.return_value = [["Hello", "World"]]
    mock_movie_service_class.return_value = mock_movie_service
    
    # Mock processor
    mock_processor = MagicMock()
    mock_processor.generate_thoughts_from_character_dialogue.return_value = ["Thought 1"]
    mock_processor.synthesize_persona_from_thoughts.return_value = {
        "name": "Derived Persona",
        "age": 25,
        "gender": "Female",
        "profile": {"background": "Test"}
    }
    mock_processor_class.return_value = mock_processor
    
    # Mock PersonaService
    mock_persona = MagicMock()
    mock_persona.id = 99
    mock_persona_service.create_persona.return_value = mock_persona
    
    # Mock ThoughtUseCases
    mock_thought_uc = MagicMock()
    
    mock_thought = MagicMock()
    mock_thought.id = 101
    mock_thought_uc.create_thought.return_value = mock_thought
    
    mock_thought_uc_class.return_value = mock_thought_uc
    
    # Execute Use Case
    uc = GenerationUseCases()
    result = uc.generate_persona_from_movie_characters(["char1"])
    
    assert result["persona_id"] == 99
    assert len(result["thoughts"]) == 1
    assert result["thoughts"][0] == "Thought 1"
    
    mock_movie_service.get_character_dialogues.assert_called_once_with("char1", limit=100)
    mock_processor.generate_thoughts_from_character_dialogue.assert_called_once()
    mock_processor.synthesize_persona_from_thoughts.assert_called_once_with(["Thought 1"])
    mock_persona_service.create_persona.assert_called_once()
