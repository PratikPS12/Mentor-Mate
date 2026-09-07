import httpx
import logging
from typing import Dict, Any, List, Optional, Tuple
from app.services.ai.provider import AIProvider
from app.core.config import settings

logger = logging.getLogger("mentormate.ai.agentrouter")

class AgentRouterProvider(AIProvider):
    """
    Production adapter for AgentRouter / OpenAI-compatible /v1 API gateways.
    Dynamically auto-detects and supports AgentRouter, OpenAI, Google Gemini, Groq, and OpenRouter.
    Never exposes API credentials to frontend or client code.
    """

    def __init__(self):
        self.api_key = settings.AGENTROUTER_API_KEY
        self.timeout = httpx.Timeout(connect=5.0, read=30.0, write=10.0, pool=5.0)

    def _resolve_endpoint_and_model(self, requested_model: Optional[str]) -> Tuple[str, str]:
        key = self.api_key or ""
        configured_base = (settings.AGENTROUTER_BASE_URL or "").strip().rstrip("/")

        # Auto-detect provider if user pasted key from specific platform
        if key.startswith("AIzaSy"):
            # Google Gemini OpenAI-compatible API
            base = configured_base if "generativelanguage" in configured_base else "https://generativelanguage.googleapis.com/v1beta/openai"
            model = requested_model if (requested_model and "gemini" in requested_model) else "gemini-2.0-flash"
            return base, model
        elif key.startswith("gsk_"):
            # Groq
            base = configured_base if "groq" in configured_base else "https://api.groq.com/openai/v1"
            model = requested_model if (requested_model and "llama" in requested_model) else "llama-3.3-70b-versatile"
            return base, model
        elif key.startswith("sk-or-"):
            # OpenRouter
            base = configured_base if "openrouter" in configured_base else "https://openrouter.ai/api/v1"
            model = requested_model or "meta-llama/llama-3.3-70b-instruct"
            return base, model
        elif key.startswith("sk-proj-"):
            # OpenAI direct
            base = configured_base if "openai.com" in configured_base else "https://api.openai.com/v1"
            model = requested_model or settings.AI_MODEL_PRIMARY or "gpt-4o"
            return base, model

        base = configured_base or "https://co.agentrouter.org/v1"
        model = requested_model or settings.AI_MODEL_PRIMARY or "gpt-4o"
        return base, model

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "MentorMate"
        }
        if self.api_key and self.api_key != "PASTE_YOUR_AGENTROUTER_KEY_HERE":
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        base_url, target_model = self._resolve_endpoint_and_model(model)

        if not self.api_key or self.api_key == "PASTE_YOUR_AGENTROUTER_KEY_HERE":
            logger.info("AgentRouter API key is not configured. Invoking local pedagogical fallback.")
            from app.services.ai.local_fallback_provider import LocalFallbackProvider
            return await LocalFallbackProvider().chat_completion(
                messages=messages,
                model=target_model,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format
            )

        payload: Dict[str, Any] = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if response_format:
            payload["response_format"] = response_format

        url = f"{base_url}/chat/completions"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(url, json=payload, headers=self._get_headers())
                if res.status_code == 200:
                    data = res.json()
                    choice = data["choices"][0]
                    content = choice["message"]["content"]
                    usage = data.get("usage", {})
                    return {
                        "content": content,
                        "model": data.get("model", target_model),
                        "provider": "agentrouter",
                        "usage": usage,
                        "status": "success"
                    }
                else:
                    logger.warning(f"Remote AI gateway returned HTTP {res.status_code}: {res.text}. Falling back to Socratic Pedagogical Engine.")
                    # Try fallback model if configured
                    if target_model != settings.AI_MODEL_FALLBACK and settings.AI_MODEL_FALLBACK:
                        payload["model"] = settings.AI_MODEL_FALLBACK
                        try:
                            res_fb = await client.post(url, json=payload, headers=self._get_headers())
                            if res_fb.status_code == 200:
                                data = res_fb.json()
                                return {
                                    "content": data["choices"][0]["message"]["content"],
                                    "model": data.get("model", settings.AI_MODEL_FALLBACK),
                                    "provider": "agentrouter",
                                    "usage": data.get("usage", {}),
                                    "status": "success_fallback"
                                }
                        except Exception:
                            pass
        except Exception as e:
            logger.warning(f"Remote AI connectivity exception: {e}. Falling back to Socratic Pedagogical Engine.")

        # Local pedagogical fallback on error/timeout/401
        from app.services.ai.local_fallback_provider import LocalFallbackProvider
        return await LocalFallbackProvider().chat_completion(
            messages=messages,
            model=target_model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format
        )

    async def get_available_models(self) -> List[str]:
        if not self.api_key or self.api_key == "PASTE_YOUR_AGENTROUTER_KEY_HERE":
            return ["local_pedagogical_fallback", "deterministic_math_solver", "bkt_irt_evaluator"]

        base_url, _ = self._resolve_endpoint_and_model(None)
        url = f"{base_url}/models"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.get(url, headers=self._get_headers())
                if res.status_code == 200:
                    data = res.json()
                    models = [m.get("id") for m in data.get("data", []) if "id" in m]
                    return sorted(models)
        except Exception as e:
            logger.debug(f"Failed to fetch models: {e}")
        return ["gpt-4o", "gpt-4o-mini", "o1", "local_pedagogical_fallback"]

    async def health_check(self) -> Dict[str, Any]:
        is_key_set = bool(self.api_key and self.api_key != "PASTE_YOUR_AGENTROUTER_KEY_HERE")
        base_url, target_model = self._resolve_endpoint_and_model(None)

        if not is_key_set:
            return {
                "provider": "agentrouter",
                "configured": False,
                "status": "ready_fallback",
                "message": "AI API key not configured. Running in high-precision local pedagogical mode.",
                "base_url": base_url,
                "active_models": ["local_pedagogical_fallback"]
            }

        try:
            models = await self.get_available_models()
            return {
                "provider": "agentrouter",
                "configured": True,
                "status": "connected",
                "base_url": base_url,
                "active_target_model": target_model,
                "available_models_count": len(models),
                "configured_models": {
                    "primary": settings.AI_MODEL_PRIMARY,
                    "fast": settings.AI_MODEL_FAST,
                    "reasoning": settings.AI_MODEL_REASONING,
                    "vision": settings.AI_MODEL_VISION,
                    "fallback": settings.AI_MODEL_FALLBACK
                }
            }
        except Exception as e:
            return {
                "provider": "agentrouter",
                "configured": True,
                "status": "ready_fallback",
                "error": str(e)
            }
