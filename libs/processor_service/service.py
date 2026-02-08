import json
import ast
import random
import re
from typing import List
from libs.llm_service import LLMFactory
from .prompts import COGNITIVE_DISTORTION_PROMPT, SENTIMENT_ANALYSIS_PROMPT, THOUGHT_GENERATION_PROMPT, ESSAY_GENERATION_PROMPT, ACTION_ORIENTATION_PROMPT, THOUGHT_TYPE_PROMPT

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

    def generate_essay(self, starting_text: str, persona_details: str, emotions: List[str], tags: List[str]) -> str:
        prompt = ESSAY_GENERATION_PROMPT.format(
            starting_text=starting_text,
            persona_details=persona_details,
            emotions=", ".join(random.sample(emotions, min(len(emotions), 2))),
            tags=", ".join(random.sample(tags, min(len(tags), 2)))
        )
        return self.llm.generate_content(prompt)
