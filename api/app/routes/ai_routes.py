from fastapi import APIRouter
from app.services.ai.registry import AIProviderRegistry

router = APIRouter(prefix="/ai", tags=["AI Provider Engine"])

@router.get("/health")
async def ai_health():
    """
    Validates AI Provider configuration, verifies network reachability to AgentRouter,
    and returns model availability metrics.
    """
    return await AIProviderRegistry.get_health()

@router.get("/models")
async def list_available_models():
    """
    Returns list of verified available models accessible to current credentials.
    """
    provider = AIProviderRegistry.get_provider()
    models = await provider.get_available_models()
    return {"status": "success", "models": models}
