from unittest.mock import MagicMock, patch
from workers.tasks import analyze_action_orientation, analyze_thought_type
from libs.db_service import ThoughtService, ThoughtDomain

@patch("workers.tasks.ThoughtService")
@patch("workers.tasks.processor")
def test_analyze_action_orientation(mock_processor, mock_thought_service):
    # Setup
    mock_thought = MagicMock(spec=ThoughtDomain)
    mock_thought.content = "I need to plan my day."
    mock_thought_service.get_thought.return_value = mock_thought
    
    mock_processor.analyze_action_orientation.return_value = "Action-oriented"
    
    # Execute
    analyze_action_orientation(1)
    
    # Verify
    mock_thought_service.get_thought.assert_called_with(1)
    mock_processor.analyze_action_orientation.assert_called_with("I need to plan my day.")
    mock_thought_service.update_thought.assert_called_with(1, {"action_orientation": "Action-oriented"})

@patch("workers.tasks.ThoughtService")
@patch("workers.tasks.processor")
def test_analyze_thought_type(mock_processor, mock_thought_service):
    # Setup
    mock_thought = MagicMock(spec=ThoughtDomain)
    mock_thought.content = "Why does this always happen?"
    mock_thought_service.get_thought.return_value = mock_thought
    
    mock_processor.analyze_thought_type.return_value = "Automatic"
    
    # Execute
    analyze_thought_type(1)
    
    # Verify
    mock_thought_service.get_thought.assert_called_with(1)
    mock_processor.analyze_thought_type.assert_called_with("Why does this always happen?")
    mock_thought_service.update_thought.assert_called_with(1, {"thought_type": "Automatic"})
