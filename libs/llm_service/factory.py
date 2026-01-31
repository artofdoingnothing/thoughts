from enum import Enum
from .gemini import GeminiLLM
from .base import BaseLLM

class LLMProvider(Enum):
    GEMINI = "gemini"

class LLMFactory:
    @staticmethod
    def get_llm(provider: LLMProvider = LLMProvider.GEMINI, **kwargs) -> BaseLLM:
        if provider == LLMProvider.GEMINI:
            return GeminiLLM(**kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
