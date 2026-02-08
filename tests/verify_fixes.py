import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import json

# Mock dependencies that might be missing in API container or strictly needed for unit test isolation
sys.modules['google'] = MagicMock()
sys.modules['google.genai'] = MagicMock()
sys.modules['redis'] = MagicMock()
sys.modules['rq'] = MagicMock()

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from libs.processor_service.service import ProcessorService
from backend.main import generate_thoughts, GenerateThoughtsRequest

class TestFixes(unittest.TestCase):
    def setUp(self):
        self.processor = ProcessorService()

    def test_parse_list_output_json(self):
        """Test parsing valid JSON output"""
        output = '["Happy", "Sad"]'
        result = self.processor._parse_list_output(output)
        self.assertEqual(result, ["Happy", "Sad"])

    def test_parse_list_output_json_markdown(self):
        """Test parsing JSON inside markdown"""
        output = '```json\n["Happy", "Sad"]\n```'
        result = self.processor._parse_list_output(output)
        self.assertEqual(result, ["Happy", "Sad"])

    def test_parse_list_output_json_markdown_multiline(self):
        """Test parsing multi-line JSON inside markdown"""
        output = '```json\n[\n  "Happy",\n  "Sad"\n]\n```'
        result = self.processor._parse_list_output(output)
        self.assertEqual(result, ["Happy", "Sad"])

    def test_parse_list_output_python_fallback(self):
        """Test fallback to ast.literal_eval"""
        output = "['Happy', 'Sad']"
        result = self.processor._parse_list_output(output)
        self.assertEqual(result, ["Happy", "Sad"])

    def test_parse_list_output_malformed(self):
        """Test malformed output returns empty list"""
        output = "Not a list"
        result = self.processor._parse_list_output(output)
        self.assertEqual(result, [])

    @patch('backend.main.Queue')
    def test_generate_thoughts_multiple_urls(self, MockQueue):
        """Test that generate_thoughts enqueues multiple jobs"""
        mock_queue_instance = MagicMock()
        MockQueue.return_value = mock_queue_instance
        
        request = GenerateThoughtsRequest(urls=["http://url1.com", "http://url2.com"], persona_id=1)
        generate_thoughts(request)
        
        self.assertEqual(mock_queue_instance.enqueue.call_count, 2)
        # Verify calls
        calls = mock_queue_instance.enqueue.call_args_list
        self.assertEqual(calls[0][0][1], "http://url1.com")
        self.assertEqual(calls[1][0][1], "http://url2.com")

if __name__ == '__main__':
    unittest.main()
