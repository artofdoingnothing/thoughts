import pytest
from unittest.mock import patch, MagicMock
from libs.processor_service.service import ProcessorService

@patch("libs.processor_service.service.LLMFactory.get_llm")
def test_processor_service_init(mock_get_llm):
    mock_llm = MagicMock()
    mock_get_llm.return_value = mock_llm
    service = ProcessorService()
    assert service.llm == mock_llm

def test_parse_list_output():
    service = ProcessorService()
    
    # Test valid JSON list
    assert service._parse_list_output('["a", "b"]') == ["a", "b"]
    
    # Test valid ast literal
    assert service._parse_list_output("['a', 'b']") == ["a", "b"]
    
    # Test markdown code block
    assert service._parse_list_output('```json\n["a", "b"]\n```') == ["a", "b"]
    
    # Test invalid content
    assert service._parse_list_output("not a list") == []

@patch("libs.processor_service.service.LLMFactory.get_llm")
def test_analyze_cognitive_distortions(mock_get_llm):
    mock_llm = MagicMock()
    mock_llm.generate_content.return_value = '["Distortion1"]'
    mock_get_llm.return_value = mock_llm
    
    service = ProcessorService()
    result = service.analyze_cognitive_distortions("I am terrible")
    
    assert result == ["Distortion1"]
    mock_llm.generate_content.assert_called_once()

@patch("libs.processor_service.service.LLMFactory.get_llm")
def test_analyze_action_orientation(mock_get_llm):
    mock_llm = MagicMock()
    mock_llm.generate_content.return_value = 'Action-oriented'
    mock_get_llm.return_value = mock_llm
    
    service = ProcessorService()
    result = service.analyze_action_orientation("Let's do this")
    
    assert result == "Action-oriented"
    mock_llm.generate_content.assert_called_once()

@patch("libs.processor_service.service.LLMFactory.get_llm")
def test_generate_conversation_message(mock_get_llm):
    mock_llm = MagicMock()
    mock_llm.generate_content.return_value = '{"messages": [{"content": "Hello"}]}'
    mock_get_llm.return_value = mock_llm
    
    service = ProcessorService()
    result = service.generate_conversation_message("Name", 30, "Male", {}, "Context", [], "Other Info")
    
    assert result == ["Hello"]
    mock_llm.generate_content.assert_called_once()
