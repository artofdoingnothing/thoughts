import unittest
from unittest.mock import patch, MagicMock
from workers.tasks import parse_blog_and_generate_thoughts

class TestBlogParsing(unittest.TestCase):
    @patch('libs.use_cases.generation_use_cases.requests.get')
    @patch('libs.use_cases.generation_use_cases.ProcessorService')
    @patch('workers.tasks.thought_uc.create_thought')
    @patch('workers.tasks.Queue')
    @patch('workers.tasks.redis_conn')
    def test_parse_blog_and_generate_thoughts(self, mock_redis, mock_queue, mock_create, MockProcessorService, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><head><title>Test Blog</title></head><body><p>Thought 1 content.</p><p>Thought 2 content.</p></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        mock_processor_instance = MagicMock()
        mock_processor_instance.generate_thoughts_from_text.return_value = ["Thought 1", "Thought 2"]
        MockProcessorService.return_value = mock_processor_instance
        
        from workers.tasks import generation_uc
        generation_uc.processor = mock_processor_instance

        mock_thought = MagicMock()
        mock_thought.id = 1
        mock_create.return_value = mock_thought

        parse_blog_and_generate_thoughts("http://test.com", 1)

        mock_get.assert_called_with("http://test.com", timeout=10)
        mock_processor_instance.generate_thoughts_from_text.assert_called()
        self.assertEqual(mock_create.call_count, 2)
        
        call_args_list = mock_create.call_args_list
        self.assertEqual(len(call_args_list), 2)
        
        args1, kwargs1 = call_args_list[0]
        self.assertEqual(kwargs1['content'], "Thought 1")
        self.assertEqual(kwargs1['is_generated'], True)
        self.assertEqual(kwargs1['persona_id'], 1)

        self.assertTrue(mock_queue.return_value.enqueue.called)

if __name__ == '__main__':
    unittest.main()
