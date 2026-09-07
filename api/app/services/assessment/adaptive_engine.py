import math
from typing import Dict, Any, List, Optional, Tuple
from app.services.student_model.irt_engine import IRTEngine

class AdaptiveAssessmentEngine:
    """
    Computerized Adaptive Testing (CAT) Engine.
    Selects the next assessment item by maximizing Fisher Information at student's current
    latent ability theta, prioritized by BKT knowledge component gaps.
    """

    STOPPING_SE_THRESHOLD = 0.35
    MIN_ITEMS = 4
    MAX_ITEMS = 15

    @classmethod
    def select_next_question(
        cls,
        candidate_questions: List[Dict[str, Any]],
        administered_ids: List[str],
        current_theta: float,
        concept_masteries: Optional[Dict[str, float]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Picks optimal next item:
        Score = Fisher_Info(theta, b_i, a_i) * (1.0 + 0.5 * (1.0 - BKT_mastery))
        """
        available = [q for q in candidate_questions if q["id"] not in administered_ids]
        if not available:
            return None

        best_item = None
        highest_utility = -1.0

        for q in available:
            # Map question difficulty to IRT parameter b in [-2.5, +2.5]
            diff_raw = q.get("difficulty", "medium")
            if isinstance(diff_raw, (int, float)):
                b = float(diff_raw) * 2.0 - 1.0  # normalize [0.0, 1.0] to [-1.0, 1.0]
            elif isinstance(diff_raw, str):
                diff_label = diff_raw.lower()
                b = -1.0 if diff_label == "easy" else (1.0 if diff_label == "hard" else 0.0)
            else:
                b = 0.0

            a = float(q.get("discrimination", 1.2))
            info = IRTEngine.fisher_information(current_theta, difficulty=b, discrimination=a)

            # Weight by BKT mastery gap if available
            concept_id = q.get("concept_id")
            mastery_weight = 1.0
            if concept_masteries and concept_id in concept_masteries:
                mastery = concept_masteries[concept_id]
                # If student is weak in this concept, increase information utility
                mastery_weight = 1.0 + (1.0 - mastery)

            utility = info * mastery_weight
            if utility > highest_utility:
                highest_utility = utility
                best_item = q

        return best_item

    @classmethod
    def evaluate_stopping_criteria(
        cls,
        items_administered_count: int,
        current_se: float
    ) -> Tuple[bool, str]:
        """
        Evaluates whether the adaptive testing session has attained statistical stability.
        """
        if items_administered_count < cls.MIN_ITEMS:
            return False, "Minimum item threshold not yet reached"

        if current_se <= cls.STOPPING_SE_THRESHOLD:
            return True, f"Measurement error reduced to target threshold ({current_se:.2f} <= {cls.STOPPING_SE_THRESHOLD})"

        if items_administered_count >= cls.MAX_ITEMS:
            return True, f"Maximum item limit ({cls.MAX_ITEMS}) reached"

        return False, "Active adaptive test in progress"
