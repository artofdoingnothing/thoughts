import pytest
from unittest.mock import patch, MagicMock
from libs.llm_service.base import BaseLLM
from libs.llm_service.gemini import GeminiLLM
import os

class DummyLLM(BaseLLM):
    def generate_content(self, prompt: str) -> str:
        return "Dummy response"

def test_base_llm():
    dummy = DummyLLM()
    assert dummy.generate_content("test") == "Dummy response"

@patch("libs.llm_service.gemini.genai.Client")
def test_gemini_llm_initialization(mock_client):
    llm = GeminiLLM(api_key="test_key")
    assert llm.api_key == "test_key"
    mock_client.assert_called_once_with(api_key="test_key")

def test_gemini_llm_missing_key():
    with patch.dict(os.environ, {}, clear=True):
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
        with pytest.raises(ValueError, match="GEMINI_API_KEY is not set."):
            GeminiLLM()

@patch("libs.llm_service.gemini.genai.Client")
def test_gemini_llm_generate_content(mock_client_class):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Generated text"
    mock_client.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_client
    
    llm = GeminiLLM(api_key="test_key")
    result = llm.generate_content("prompt")
    
    assert result == "Generated text"
    mock_client.models.generate_content.assert_called_once_with(model="gemini-2.0-flash", contents="prompt")
