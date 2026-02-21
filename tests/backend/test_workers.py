from unittest.mock import patch, MagicMock
from workers.tasks import (
    analyze_cognitive_distortions,
    analyze_sentiment,
    parse_blog_and_generate_thoughts,
    generate_essay,
    generate_conversation_sequence,
    process_conversation_thoughts
)
from workers.worker import run_worker

@patch("workers.tasks.thought_uc")
def test_analyze_cognitive_distortions_task(mock_thought_uc):
    mock_thought_uc.analyze_cognitive_distortions.return_value = ["dist1"]
    analyze_cognitive_distortions(1)
    mock_thought_uc.analyze_cognitive_distortions.assert_called_once_with(1)

@patch("workers.tasks.thought_uc")
def test_analyze_sentiment_task(mock_thought_uc):
    mock_thought_uc.analyze_sentiment.return_value = ["happy"]
    analyze_sentiment(1)
    mock_thought_uc.analyze_sentiment.assert_called_once_with(1)

@patch("workers.tasks.Queue")
@patch("workers.tasks.thought_uc")
@patch("workers.tasks.generation_uc")
def test_parse_blog_and_generate_thoughts_task(mock_generation_uc, mock_thought_uc, mock_queue):
    mock_generation_uc.parse_blog.return_value = "Content"
    mock_generation_uc.generate_thoughts_from_text.return_value = ["thought1"]
    
    mock_thought = MagicMock()
    mock_thought.id = 1
    mock_thought_uc.create_thought.return_value = mock_thought
    
    mock_q_instance = MagicMock()
    mock_queue.return_value = mock_q_instance
    
    parse_blog_and_generate_thoughts("http://test.com", 1)
    mock_generation_uc.parse_blog.assert_called_once_with("http://test.com")
    mock_thought_uc.create_thought.assert_called_once()
    assert mock_queue.call_count == 5

@patch("workers.tasks.generation_uc")
def test_generate_essay_task(mock_generation_uc):
    mock_generation_uc.generate_essay.return_value = "Final essay content"
    result = generate_essay(1, "start")
    
    assert result == "Final essay content"
    mock_generation_uc.generate_essay.assert_called_once_with(1, "start")

@patch("workers.tasks.conversation_uc")
def test_generate_conversation_sequence_task(mock_conversation_uc):
    mock_conversation_uc.generate_conversation_message.return_value = ["message1"]
    
    generate_conversation_sequence(1, [1, 2])
    
    assert mock_conversation_uc.generate_conversation_message.call_count == 2

@patch("workers.tasks.conversation_uc")
def test_process_conversation_thoughts_task(mock_conversation_uc):
    process_conversation_thoughts(1)
    mock_conversation_uc.process_conversation_thoughts.assert_called_once_with(1)

@patch("workers.worker.Worker")
@patch("workers.worker.Queue")
@patch("workers.worker.init_database")
def test_run_worker(mock_init_db, mock_queue, mock_worker_cls):
    mock_worker_instance = MagicMock()
    mock_worker_cls.return_value = mock_worker_instance
    
    run_worker()
    
    mock_init_db.assert_called_once()
    mock_worker_instance.work.assert_called_once()
