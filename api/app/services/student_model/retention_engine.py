import math
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Tuple

class RetentionEngine:
    """
    Ebbinghaus Memory Retention & Spaced Repetition Engine.
    Formula: R(t) = exp(-t / S)
    """
    RETENTION_THRESHOLD = 0.75  # Target retention to trigger review

    @staticmethod
    def calculate_current_retention(last_review_iso: str, memory_strength: float) -> float:
        """Computes current retention probability R(t) given elapsed days."""
        try:
            last_review = datetime.fromisoformat(last_review_iso)
            if last_review.tzinfo is None:
                last_review = last_review.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            elapsed_days = max(0.0, (now - last_review).total_seconds() / 86400.0)
            strength = max(0.5, memory_strength)
            retention = math.exp(-elapsed_days / strength)
            return round(max(0.05, min(1.0, retention)), 4)
        except Exception:
            return 0.5

    @classmethod
    def update_memory_strength(
        cls,
        prior_strength: float,
        is_successful: bool,
        repetition_count: int
    ) -> Tuple[float, str, str]:
        """
        Updates memory strength S after a practice/review trial and calculates next review timestamp.
        Returns: (new_strength, last_review_iso, next_review_iso)
        """
        now = datetime.now(timezone.utc)
        current_s = max(1.0, prior_strength)

        if is_successful:
            # Memory stability expands with successful recall
            factor = 1.8 + min(1.2, repetition_count * 0.25)
            new_s = current_s * factor
        else:
            # Memory lapse resets stability partially
            new_s = max(1.0, current_s * 0.6)

        new_s = round(min(180.0, new_s), 2)  # Cap at 180 days

        # Next review is when R(t) drops to threshold:
        # 0.75 = exp(-t_due / S) => t_due = -S * ln(0.75) ≈ 0.2877 * S days
        days_until_due = max(0.5, round(new_s * -math.log(cls.RETENTION_THRESHOLD), 2))
        next_review = now + timedelta(days=days_until_due)

        return new_s, now.isoformat(), next_review.isoformat()
