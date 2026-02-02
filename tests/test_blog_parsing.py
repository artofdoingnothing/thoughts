import unittest
from unittest.mock import patch, MagicMock
from workers.tasks import parse_blog_and_generate_thoughts
from libs.db_service import ThoughtService

class TestBlogParsing(unittest.TestCase):
    @patch('workers.tasks.requests.get')
    @patch('workers.tasks.processor.generate_thoughts_from_text')
    @patch('workers.tasks.ThoughtService.create_thought')
    @patch('workers.tasks.Queue')
    @patch('workers.tasks.redis_conn')
    def test_parse_blog_and_generate_thoughts(self, mock_redis, mock_queue, mock_create, mock_generate, mock_get):
        # Mock requests
        mock_response = MagicMock()
        mock_response.content = b"<html><head><title>Test Blog</title></head><body><p>Thought 1 content.</p><p>Thought 2 content.</p></body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Mock generate
        mock_generate.return_value = ["Thought 1", "Thought 2"]

        # Mock create
        mock_thought = MagicMock()
        mock_thought.id = 1
        mock_create.return_value = mock_thought

        # Run task
        parse_blog_and_generate_thoughts("http://test.com", 1)

        # Assertions
        mock_get.assert_called_with("http://test.com", timeout=10)
        mock_generate.assert_called()
        self.assertEqual(mock_create.call_count, 2)
        
        # Check last call args
        call_args_list = mock_create.call_args_list
        self.assertEqual(len(call_args_list), 2)
        
        # Verify first thought creation
        args1, kwargs1 = call_args_list[0]
        self.assertEqual(kwargs1['content'], "Thought 1")
        self.assertEqual(kwargs1['is_generated'], True)
        self.assertEqual(kwargs1['persona_id'], 1)
        self.assertTrue("Test Blog" in kwargs1['title'])

        # Check queue
        # Since Queue is instantiated multiple times, we check if enqueue was called on any instance
        enqueue_called = False
        for call in mock_queue.return_value.method_calls:
             if call[0] == 'enqueue':
                 enqueue_called = True
                 break
        # mock_queue returns a mock instance. 
        # Actually mock_queue.return_value is the instance returned by Queue(...) constructor.
        # We assume queue.enqueue is called.
        self.assertTrue(mock_queue.return_value.enqueue.called)

if __name__ == '__main__':
    unittest.main()
