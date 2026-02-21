from libs.db_service import ThoughtService, PersonaService
from libs.processor_service import ProcessorService
from typing import List, Dict, Any, Optional
from libs.db_service.dto import ThoughtDomain, PersonaDomain

class ThoughtUseCases:
    def __init__(self):
        self.processor = ProcessorService()

    def analyze_cognitive_distortions(self, thought_id: int) -> Optional[List[str]]:
        thought = ThoughtService.get_thought(thought_id)
        if not thought: return None
        distortions = self.processor.analyze_cognitive_distortions(thought.content)
        if distortions:
            ThoughtService.add_tags(thought_id, distortions, is_generated=True)
        ThoughtService.update_status(thought_id, "completed")
        return distortions

    def analyze_sentiment(self, thought_id: int) -> Optional[List[str]]:
        thought = ThoughtService.get_thought(thought_id)
        if not thought: return None
        emotions = self.processor.analyze_sentiment(thought.content)
        if emotions:
            ThoughtService.add_emotions(thought_id, emotions, is_generated=True)
        ThoughtService.update_status(thought_id, "completed")
        return emotions

    def analyze_action_orientation(self, thought_id: int) -> Optional[str]:
        thought = ThoughtService.get_thought(thought_id)
        if not thought: return None
        result = self.processor.analyze_action_orientation(thought.content)
        ThoughtService.update_thought(thought_id, {"action_orientation": result})
        return result

    def analyze_thought_type(self, thought_id: int) -> Optional[str]:
        thought = ThoughtService.get_thought(thought_id)
        if not thought: return None
        result = self.processor.analyze_thought_type(thought.content)
        ThoughtService.update_thought(thought_id, {"thought_type": result})
        return result

    def analyze_topics(self, thought_id: int) -> Optional[List[str]]:
        thought = ThoughtService.get_thought(thought_id)
        if not thought: return None
        topics = self.processor.analyze_topics(thought.content)
        if topics:
            ThoughtService.add_topics(thought_id, topics, is_generated=True)
        ThoughtService.update_status(thought_id, "completed")
        return topics

    def create_thought(self, content: str, persona_id: int, is_generated: bool) -> ThoughtDomain:
        return ThoughtService.create_thought(content=content, persona_id=persona_id, is_generated=is_generated)
