from enum import Enum
from app.core.config import settings

class AITaskType(str, Enum):
    REASONING = "reasoning"
    PRIMARY = "primary"
    FAST = "fast"
    VISION = "vision"
    FALLBACK = "fallback"

class AITaskRouter:
    """
    Routes educational tasks to appropriate model tiers to balance
    accuracy, latency, and cost efficiency.
    """

    @staticmethod
    def get_model_for_task(task_type: AITaskType) -> str:
        if task_type == AITaskType.REASONING:
            return settings.AI_MODEL_REASONING or settings.AI_MODEL_PRIMARY or "o1"
        elif task_type == AITaskType.FAST:
            return settings.AI_MODEL_FAST or "gpt-4o-mini"
        elif task_type == AITaskType.VISION:
            return settings.AI_MODEL_VISION or settings.AI_MODEL_PRIMARY or "gpt-4o"
        elif task_type == AITaskType.FALLBACK:
            return settings.AI_MODEL_FALLBACK or "gpt-4o-mini"
        else:
            return settings.AI_MODEL_PRIMARY or "gpt-4o"
