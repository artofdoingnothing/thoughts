from unittest.mock import MagicMock, patch
from workers.tasks import analyze_action_orientation, analyze_thought_type
from libs.db_service.dto import ThoughtDomain

@patch("libs.use_cases.thought_use_cases.ThoughtService")
@patch("libs.use_cases.thought_use_cases.ProcessorService")
def test_analyze_action_orientation(MockProcessorService, mock_thought_service):
    # Setup
    mock_thought = MagicMock(spec=ThoughtDomain)
    mock_thought.content = "I need to plan my day."
    mock_thought_service.get_thought.return_value = mock_thought
    
    mock_processor_instance = MagicMock()
    mock_processor_instance.analyze_action_orientation.return_value = "Action-oriented"
    MockProcessorService.return_value = mock_processor_instance
    
    # Needs to reset thought_uc processor because it is already instantiated in tasks
    from workers.tasks import thought_uc
    thought_uc.processor = mock_processor_instance
    
    # Execute
    analyze_action_orientation(1)
    
    # Verify
    mock_thought_service.get_thought.assert_called_with(1)
    mock_processor_instance.analyze_action_orientation.assert_called_with("I need to plan my day.")
    mock_thought_service.update_thought.assert_called_with(1, {"action_orientation": "Action-oriented"})

@patch("libs.use_cases.thought_use_cases.ThoughtService")
@patch("libs.use_cases.thought_use_cases.ProcessorService")
def test_analyze_thought_type(MockProcessorService, mock_thought_service):
    # Setup
    mock_thought = MagicMock(spec=ThoughtDomain)
    mock_thought.content = "Why does this always happen?"
    mock_thought_service.get_thought.return_value = mock_thought
    
    mock_processor_instance = MagicMock()
    mock_processor_instance.analyze_thought_type.return_value = "Automatic"
    MockProcessorService.return_value = mock_processor_instance
    
    from workers.tasks import thought_uc
    thought_uc.processor = mock_processor_instance
    
    # Execute
    analyze_thought_type(1)
    
    # Verify
    mock_thought_service.get_thought.assert_called_with(1)
    mock_processor_instance.analyze_thought_type.assert_called_with("Why does this always happen?")
    mock_thought_service.update_thought.assert_called_with(1, {"thought_type": "Automatic"})
