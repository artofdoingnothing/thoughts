from abc import ABC, abstractmethod
from typing import Any

class BaseLLM(ABC):
    @abstractmethod
    def generate_content(self, prompt: str) -> str:
        """Generates content based on the prompt."""
        pass
