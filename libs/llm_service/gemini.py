import os
from google import genai
from .base import BaseLLM

class GeminiLLM(BaseLLM):
    def __init__(self, api_key: str = None, model_name: str = "gemini-2.0-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    def generate_content(self, prompt: str) -> str:
        """Generates content using Gemini API."""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            # Handle API errors gracefully or re-raise
            print(f"Error calling Gemini API: {e}")
            raise e
