import random

import requests
from bs4 import BeautifulSoup

from libs.db_service import PersonaService, ThoughtService
from libs.processor_service import ProcessorService


class GenerationUseCases:
    def __init__(self):
        self.processor = ProcessorService()

    def parse_blog(self, url: str) -> str:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
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

        persona_details = (
            f"Name: {persona.name}, Age: {persona.age}, Gender: {persona.gender}"
        )

        if persona.profile:
            emotions = self.processor.extract_emotions_from_profile(
                starting_text, persona.profile
            )
            return self.processor.complete_essay_with_profile(
                starting_text=starting_text,
                persona_details=persona_details,
                emotions=emotions,
            )
        else:
            unique_attrs = PersonaService.get_persona_unique_attributes(persona_id)
            thought_types = unique_attrs.get("thought_types", [])
            action_orientations = unique_attrs.get("action_orientations", [])

            selected_type = (
                random.choice(thought_types) if thought_types else "Automatic"
            )
            selected_action = (
                random.choice(action_orientations)
                if action_orientations
                else "Ruminative"
            )

            draft_result = self.processor.generate_essay_draft_and_tags(
                starting_text=starting_text,
                persona_details=persona_details,
                thought_type=selected_type,
                action_orientation=selected_action,
            )

            draft_essay = draft_result.get("essay", "")
            generated_tags = draft_result.get("tags", [])

            final_essay = draft_essay

            if generated_tags:
                closest_thought = ThoughtService.find_closest_thought_by_tags(
                    generated_tags, persona_id
                )
                if closest_thought:
                    emotions = [e.name for e in closest_thought.emotions]
                    if emotions:
                        final_essay = self.processor.modify_essay(draft_essay, emotions)

        return final_essay

    def generate_persona_from_movie_characters(self, character_ids: list[str]) -> dict:
        from libs.dataset_service.movie_dataset_service import MovieDatasetService

        movie_service = MovieDatasetService()

        total_dialogues_limit = 500
        total_thoughts_limit = 50
        n = len(character_ids)
        
        all_thoughts = []
        for i, character_id in enumerate(character_ids):
            # Calculate limits for this character
            limit_dialogues = total_dialogues_limit // n
            limit_thoughts = total_thoughts_limit // n
            if i == n - 1: # Add remainder to last character
                limit_thoughts += total_thoughts_limit % n

            # 1. Extract dialogues for this character
            dialogues_nested = movie_service.get_character_dialogues(
                character_id, limit=limit_dialogues
            )

            conversations = []
            for conversation in dialogues_nested:
                conversations.append(" ".join(conversation))

            if len(conversations) > limit_dialogues:
                conversations = random.sample(conversations, limit_dialogues)

            if conversations:
                # 2. Invoke AI Processing to generate thoughts for this character
                thoughts = self.processor.generate_thoughts_from_character_dialogue(
                    conversations, count=limit_thoughts
                )
                all_thoughts.extend(thoughts)

        if not all_thoughts:
            raise ValueError(
                "Failed to generate any thoughts from the selected characters' dialogues"
            )

        # 3. Synthesize ONE Persona profile based on the ENTIRE collection of generated thoughts
        persona_data = self.processor.synthesize_persona_from_thoughts(all_thoughts)

        # 4. Generate origin description
        origins = []
        for char_id in character_ids:
            char_meta = movie_service.get_character_by_id(char_id)
            if char_meta:
                origins.append(f"{char_meta.get('character_name')} from {char_meta.get('movie_title')}({char_meta.get('movie_year')})({char_meta.get('movie_imdb_rating')})")
        origin_str = ", ".join(origins)

        # 5. Save the new Persona
        new_persona = PersonaService.create_persona(
            name=persona_data.get("name", "Unknown Derived Character"),
            age=persona_data.get("age", 30),
            gender=persona_data.get("gender", "Unknown"),
            profile=persona_data.get("profile", {}),
            source="movie_generated",
            origin_description=origin_str
        )

        # We return the data so a worker can enqueue the other analyzes
        return {"persona_id": new_persona.id, "thoughts": all_thoughts}

    def enrich_persona_from_movie_characters(self, persona_id: int, character_ids: list[str]) -> dict:
        from libs.dataset_service.movie_dataset_service import MovieDatasetService

        persona = PersonaService.get_persona(persona_id)
        if not persona:
            raise ValueError(f"Persona with ID {persona_id} not found")

        movie_service = MovieDatasetService()

        total_dialogues_limit = 500
        total_thoughts_limit = 50
        n = len(character_ids)
        
        all_new_thoughts = []
        for i, character_id in enumerate(character_ids):
            limit_dialogues = total_dialogues_limit // n
            limit_thoughts = total_thoughts_limit // n
            if i == n - 1:
                limit_thoughts += total_thoughts_limit % n

            dialogues_nested = movie_service.get_character_dialogues(
                character_id, limit=limit_dialogues
            )

            conversations = []
            for conversation in dialogues_nested:
                conversations.append(" ".join(conversation))

            if conversations:
                thoughts = self.processor.generate_thoughts_from_character_dialogue(
                    conversations, count=limit_thoughts
                )
                all_new_thoughts.extend(thoughts)

        if not all_new_thoughts:
            raise ValueError("Failed to generate any new thoughts from selected characters")

        # After generating and returning thoughts (which will be saved by worker), 
        # the persona profile needs to be regenerated.
        # However, the regeneration happens AFTER thoughts are saved to DB.
        # But this use case returns the thoughts to the worker.
        # So the worker should probably trigger the regeneration or this use case should do it after thoughts are saved?
        # The worker currently saves thoughts. Let's let the worker handle it or update the persona here if we save them ourselves.
        # Better: return the thoughts, and the worker will handle saving and triggering regeneration.
        
        return {"persona_id": persona.id, "thoughts": all_new_thoughts}
