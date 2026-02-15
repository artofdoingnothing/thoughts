import json
import ast
import random
import re
from typing import List, Dict, Any
from libs.llm_service import LLMFactory
from .prompts import COGNITIVE_DISTORTION_PROMPT, SENTIMENT_ANALYSIS_PROMPT, THOUGHT_GENERATION_PROMPT, ACTION_ORIENTATION_PROMPT, THOUGHT_TYPE_PROMPT, ESSAY_DRAFT_AND_TAG_PROMPT, ESSAY_MODIFICATION_PROMPT, TOPIC_ANALYSIS_PROMPT, PROFILE_EMOTION_EXTRACTION_PROMPT, ESSAY_COMPLETION_FROM_PROFILE_PROMPT, CONVERSATION_MESSAGE_GENERATION_PROMPT

class ProcessorService:
    def __init__(self):
        self.llm = LLMFactory.get_llm()

    def _parse_list_output(self, output: str) -> List[str]:
        """Parses the LLM output which is expected to be a string representation of a list."""
        try:
            # First clean up any potential markdown code blocks
            output = output.strip()
            # Use regex to extract content from markdown code blocks
            # Matches ``` followed by optional language identifier, then content, then ```
            # re.DOTALL allows . to match newlines
            match = re.search(r"```(?:\w+)?\s*(.*?)```", output, re.DOTALL)
            if match:
                output = match.group(1).strip()
            
            output = output.strip()
            
            # Try JSON parsing first as it is safer and standard
            try:
                result = json.loads(output)
                if isinstance(result, list):
                    return [str(item) for item in result]
            except json.JSONDecodeError:
                pass

            # Fallback to ast.literal_eval for python-like list strings
            result = ast.literal_eval(output)
            if isinstance(result, list):
                return [str(item) for item in result]
            return []
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing LLM output: {output}. Error: {e}")
            return []

    def analyze_cognitive_distortions(self, thought_content: str) -> List[str]:
        prompt = COGNITIVE_DISTORTION_PROMPT.format(thought_content=thought_content)
        result = self.llm.generate_content(prompt)
        return self._parse_list_output(result)

    def analyze_sentiment(self, thought_content: str) -> List[str]:
        prompt = SENTIMENT_ANALYSIS_PROMPT.format(thought_content=thought_content)
        result = self.llm.generate_content(prompt)
        return self._parse_list_output(result)

    def analyze_topics(self, thought_content: str) -> List[str]:
        prompt = TOPIC_ANALYSIS_PROMPT.format(thought_content=thought_content)
        result = self.llm.generate_content(prompt)
        return self._parse_list_output(result)

    def generate_thoughts_from_text(self, text: str) -> List[str]:
        prompt = THOUGHT_GENERATION_PROMPT.format(blog_content=text)
        result = self.llm.generate_content(prompt)
        return self._parse_list_output(result)

    def analyze_action_orientation(self, thought_content: str) -> str:
        prompt = ACTION_ORIENTATION_PROMPT.format(thought_content=thought_content)
        result = self.llm.generate_content(prompt)
        cleaned = result.strip().replace('"', '').replace("'", "")
        # Basic validation
        if "Action-oriented" in cleaned:
             return "Action-oriented"
        if "Ruminative" in cleaned:
             return "Ruminative"
        return cleaned

    def analyze_thought_type(self, thought_content: str) -> str:
        prompt = THOUGHT_TYPE_PROMPT.format(thought_content=thought_content)
        result = self.llm.generate_content(prompt)
        cleaned = result.strip().replace('"', '').replace("'", "")
        if "Automatic" in cleaned:
             return "Automatic"
        if "Deliberate" in cleaned:
             return "Deliberate"
        return cleaned

    def generate_essay_draft_and_tags(
        self, 
        starting_text: str, 
        persona_details: str, 
        thought_type: str, 
        action_orientation: str
    ) -> Dict[str, Any]:
        prompt = ESSAY_DRAFT_AND_TAG_PROMPT.format(
            starting_text=starting_text,
            persona_details=persona_details,
            thought_type=thought_type,
            action_orientation=action_orientation
        )
        result = self.llm.generate_content(prompt)
        
        try:
            # Clean up potential markdown blocks
            result_clean = result.strip()
            match = re.search(r"```(?:\w+)?\s*(.*?)```", result_clean, re.DOTALL)
            if match:
                result_clean = match.group(1).strip()
            
            parsed_result = json.loads(result_clean)
            if isinstance(parsed_result, dict) and "essay" in parsed_result:
                return parsed_result
        except json.JSONDecodeError:
            print(f"Error parsing essay draft JSON: {result}")
        
        # Fallback if parsing fails but returns text
        return {
            "essay": result,
            "tags": []
        }

    def modify_essay(self, essay_content: str, emotions: List[str]) -> str:
        if not emotions:
            return essay_content
            
        prompt = ESSAY_MODIFICATION_PROMPT.format(
            essay_content=essay_content,
            emotions=", ".join(emotions)
        )
        return self.llm.generate_content(prompt)

    def extract_emotions_from_profile(self, starting_text: str, profile: Dict[str, Any]) -> List[str]:
        prompt = PROFILE_EMOTION_EXTRACTION_PROMPT.format(
            starting_text=starting_text,
            profile_json=json.dumps(profile, indent=2)
        )
        result = self.llm.generate_content(prompt)
        return self._parse_list_output(result)

    def complete_essay_with_profile(
        self, 
        starting_text: str, 
        persona_details: str, 
        emotions: List[str]
    ) -> str:
        prompt = ESSAY_COMPLETION_FROM_PROFILE_PROMPT.format(
            starting_text=starting_text,
            persona_details=persona_details,
            emotions=", ".join(emotions) if emotions else "None"
        )
        return self.llm.generate_content(prompt)

    def generate_conversation_message(
        self,
        persona_name: str,
        persona_age: int,
        persona_gender: str,
        persona_profile: Dict[str, Any],
        conversation_context: str,
        recent_messages: List[Dict[str, str]]
    ) -> str:
        formatted_messages = ""
        for msg in recent_messages:
            formatted_messages += f"{msg['persona']}: {msg['content']}\n"
        
        prompt = CONVERSATION_MESSAGE_GENERATION_PROMPT.format(
            persona_name=persona_name,
            persona_age=persona_age,
            persona_gender=persona_gender,
            persona_profile=json.dumps(persona_profile, indent=2) if persona_profile else "None",
            conversation_context=conversation_context,
            recent_messages=formatted_messages
        )
        return self.llm.generate_content(prompt)
