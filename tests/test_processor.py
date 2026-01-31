import unittest
from unittest.mock import MagicMock, patch
from libs.processor_service.service import ProcessorService
from libs.llm_service.base import BaseLLM

class TestProcessorService(unittest.TestCase):
    @patch('libs.processor_service.service.LLMFactory')
    def test_analyze_cognitive_distortions(self, MockLLMFactory):
        # Setup mock LLM
        mock_llm = MagicMock(spec=BaseLLM)
        mock_llm.generate_content.return_value = '["All-or-nothing thinking", "Overgeneralization"]'
        MockLLMFactory.get_llm.return_value = mock_llm

        processor = ProcessorService()
        result = processor.analyze_cognitive_distortions("Everything is terrible")
        
        self.assertEqual(result, ["All-or-nothing thinking", "Overgeneralization"])
        mock_llm.generate_content.assert_called_once()

    @patch('libs.processor_service.service.LLMFactory')
    def test_analyze_sentiment(self, MockLLMFactory):
        # Setup mock LLM
        mock_llm = MagicMock(spec=BaseLLM)
        mock_llm.generate_content.return_value = '["Sad", "Anxious"]'
        MockLLMFactory.get_llm.return_value = mock_llm

        processor = ProcessorService()
        result = processor.analyze_sentiment("I feel blue")
        
        self.assertEqual(result, ["Sad", "Anxious"])
        mock_llm.generate_content.assert_called_once()
    
    @patch('libs.processor_service.service.LLMFactory')
    def test_parse_list_output_markdown(self, MockLLMFactory):
        mock_llm = MagicMock(spec=BaseLLM)
        # Test markdown code block removal
        mock_llm.generate_content.return_value = '```python\n["Distortion"]\n```'
        MockLLMFactory.get_llm.return_value = mock_llm
        
        processor = ProcessorService()
        result = processor.analyze_cognitive_distortions("text")
        self.assertEqual(result, ["Distortion"])

if __name__ == '__main__':
    unittest.main()
