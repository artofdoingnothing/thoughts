from typing import Callable, Dict, List, Any

class DomainEventBus:
    _subscribers: Dict[str, List[Callable]] = {}

    @classmethod
    def subscribe(cls, event_type: str, handler: Callable):
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []
        cls._subscribers[event_type].append(handler)

    @classmethod
    def publish(cls, event_type: str, event_data: Any):
        if event_type in cls._subscribers:
            for handler in cls._subscribers[event_type]:
                try:
                    handler(event_data)
                except Exception as e:
                    print(f"Error handling event {event_type}: {e}")
