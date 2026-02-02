import json
import ast
from typing import List
from libs.llm_service import LLMFactory
from .prompts import COGNITIVE_DISTORTION_PROMPT, SENTIMENT_ANALYSIS_PROMPT, THOUGHT_GENERATION_PROMPT

class ProcessorService:
    def __init__(self):
        self.llm = LLMFactory.get_llm()

    def _parse_list_output(self, output: str) -> List[str]:
        """Parses the LLM output which is expected to be a string representation of a list."""
        try:
            # First clean up any potential markdown code blocks
            output = output.strip()
            if output.startswith("```"):
                output = output.splitlines()[1] if len(output.splitlines()) > 1 else output
                if output.startswith("python") or output.startswith("json"):
                     output = output[6:] if output.startswith("python") else output[4:]
                if output.endswith("```"):
                     output = output[:-3]
            
            # Use ast.literal_eval for safe evaluation of python-like list strings
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
