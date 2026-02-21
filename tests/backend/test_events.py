from unittest.mock import patch, MagicMock
from libs.events.bus import DomainEventBus
from libs.events.handlers import handle_conversation_ended, register_handlers
from libs.events.conversation_events import ConversationEndedEvent

def test_event_bus():
    # Clear subscribers for testing
    DomainEventBus._subscribers = {}
    
    mock_handler = MagicMock()
    DomainEventBus.subscribe("TestEvent", mock_handler)
    
    # Test publishing
    DomainEventBus.publish("TestEvent", "data")
    mock_handler.assert_called_once_with("data")
    
    # Test error handling in publish
    def bad_handler(data):
        raise ValueError("Error")
    DomainEventBus.subscribe("ErrorEvent", bad_handler)
    DomainEventBus.publish("ErrorEvent", "data") # Should not raise exception
    
@patch("libs.events.handlers.q")
def test_handle_conversation_ended(mock_q):
    event = ConversationEndedEvent(conversation_id=1)
    handle_conversation_ended(event)
    mock_q.enqueue.assert_called_once_with("workers.tasks.process_conversation_thoughts", 1)

@patch("libs.events.handlers.DomainEventBus")
def test_register_handlers(mock_bus):
    register_handlers()
    mock_bus.subscribe.assert_called_once_with("ConversationEndedEvent", handle_conversation_ended)
