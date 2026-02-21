from libs.db_service import ThoughtService, PersonaService
from libs.processor_service import ProcessorService
import requests
from bs4 import BeautifulSoup
import random

class GenerationUseCases:
    def __init__(self):
        self.processor = ProcessorService()

    def parse_blog(self, url: str) -> str:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = [p.get_text() for p in soup.find_all('p')]
        text_content = "\\n".join(paragraphs)
        
        if len(text_content) < 100:
            text_content = soup.get_text()
            
        return text_content

    def generate_thoughts_from_text(self, text_content: str) -> list[str]:
        return self.processor.generate_thoughts_from_text(text_content)

    def generate_essay(self, persona_id: int, starting_text: str) -> str:
        persona = PersonaService.get_persona(persona_id)
        if not persona:
            return "Error: Persona not found"

        persona_details = f"Name: {persona.name}, Age: {persona.age}, Gender: {persona.gender}"
        
        if persona.profile:
            emotions = self.processor.extract_emotions_from_profile(starting_text, persona.profile)
            return self.processor.complete_essay_with_profile(
                starting_text=starting_text,
                persona_details=persona_details,
                emotions=emotions
            )
        else:
            unique_attrs = PersonaService.get_persona_unique_attributes(persona_id)
            thought_types = unique_attrs.get("thought_types", [])
            action_orientations = unique_attrs.get("action_orientations", [])
            
            selected_type = random.choice(thought_types) if thought_types else "Automatic"
            selected_action = random.choice(action_orientations) if action_orientations else "Ruminative"
            
            draft_result = self.processor.generate_essay_draft_and_tags(
                starting_text=starting_text,
                persona_details=persona_details,
                thought_type=selected_type,
                action_orientation=selected_action
            )
            
            draft_essay = draft_result.get("essay", "")
            generated_tags = draft_result.get("tags", [])
            
            final_essay = draft_essay
            
            if generated_tags:
                closest_thought = ThoughtService.find_closest_thought_by_tags(generated_tags, persona_id)
                if closest_thought:
                    emotions = [e.name for e in closest_thought.emotions]
                    if emotions:
                        final_essay = self.processor.modify_essay(draft_essay, emotions)
                
        return final_essay
