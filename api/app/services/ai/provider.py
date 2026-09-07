from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class AIProvider(ABC):
    """
    Abstract AI Provider contract.
    Ensures Mentor Mate is never tightly coupled to a single vendor or protocol.
    """

    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes a chat completion request and returns standardized response dict:
        {
            "content": str,
            "model": str,
            "provider": str,
            "usage": {"prompt_tokens": int, "completion_tokens": int, "total_tokens": int},
            "status": "success" | "fallback"
        }
        """
        pass

    @abstractmethod
    async def get_available_models(self) -> List[str]:
        """Retrieves list of models available to the active provider credentials."""
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Verifies provider connectivity and credential status."""
        pass
