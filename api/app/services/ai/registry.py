from typing import Dict, Any, Optional
from app.core.config import settings
from app.services.ai.provider import AIProvider
from app.services.ai.agentrouter_provider import AgentRouterProvider
from app.services.ai.local_fallback_provider import LocalFallbackProvider

class AIProviderRegistry:
    """
    Central registry for dynamic AI provider instantiation and resolution.
    """

    _providers: Dict[str, AIProvider] = {}

    @classmethod
    def get_provider(cls, name: Optional[str] = None) -> AIProvider:
        provider_name = (name or settings.AI_PROVIDER or "agentrouter").lower()

        if provider_name not in cls._providers:
            if provider_name in ["agentrouter", "openai"]:
                cls._providers[provider_name] = AgentRouterProvider()
            else:
                cls._providers[provider_name] = LocalFallbackProvider()

        return cls._providers[provider_name]

    @classmethod
    async def get_health(cls) -> Dict[str, Any]:
        provider = cls.get_provider()
        return await provider.health_check()
