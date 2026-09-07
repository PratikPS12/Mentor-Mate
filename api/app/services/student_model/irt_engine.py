import math
from typing import Dict, Any, List, Tuple, Optional

class IRTEngine:
    """
    Item Response Theory (IRT) Engine supporting 1PL (Rasch) and 2PL models.
    Estimates student latent ability (theta) and computes item Fisher Information.
    """

    DEFAULT_THETA = 0.0          # Standard normal prior mean
    PRIOR_VARIANCE = 1.0         # Standard normal prior variance
    MAX_ITERATIONS = 25
    CONVERGENCE_THRESHOLD = 0.001
    MAX_STEP = 0.75              # Damping step to prevent divergence

    @staticmethod
    def probability_correct(theta: float, difficulty: float, discrimination: float = 1.0) -> float:
        """
        2-Parameter Logistic (2PL) response function:
        P(Y=1 | theta, a, b) = 1 / (1 + exp(-a * (theta - b)))
        """
        z = discrimination * (theta - difficulty)
        # Numerical stability clamping
        if z > 35.0:
            return 1.0
        if z < -35.0:
            return 0.0
        return 1.0 / (1.0 + math.exp(-z))

    @classmethod
    def fisher_information(cls, theta: float, difficulty: float, discrimination: float = 1.0) -> float:
        """
        Computes Fisher Information for an item at ability level theta:
        I(theta) = a^2 * P(theta) * (1 - P(theta))
        """
        p = cls.probability_correct(theta, difficulty, discrimination)
        return (discrimination ** 2) * p * (1.0 - p)

    @classmethod
    def test_information(cls, theta: float, items: List[Dict[str, float]]) -> float:
        """
        Total test information across an item set:
        I_total(theta) = sum(I_i(theta))
        """
        return sum(cls.fisher_information(theta, item["difficulty"], item.get("discrimination", 1.0)) for item in items)

    @classmethod
    def standard_error(cls, theta: float, items: List[Dict[str, float]]) -> float:
        """
        Standard Error of Measurement:
        SE(theta) = 1 / sqrt(I_total(theta) + 1 / prior_var)
        """
        info = cls.test_information(theta, items) + (1.0 / cls.PRIOR_VARIANCE)
        return 1.0 / math.sqrt(info) if info > 0 else 1.0

    @classmethod
    def estimate_ability_map(
        cls,
        responses: List[Tuple[float, float, int]], # (difficulty, discrimination, correct 1/0)
        initial_theta: float = 0.0
    ) -> Dict[str, Any]:
        """
        Maximum A Posteriori (MAP) estimation of latent ability theta
        using Newton-Raphson optimization with N(0, 1) prior.
        """
        if not responses:
            return {
                "theta": initial_theta,
                "standard_error": 1.0,
                "confidence": "Low",
                "proficiency_band": cls.classify_proficiency(initial_theta),
                "items_administered": 0
            }

        theta = initial_theta
        for _ in range(cls.MAX_ITERATIONS):
            first_deriv = 0.0
            second_deriv = 0.0

            # Prior contribution (Gaussian log-prior: -theta / var)
            first_deriv -= theta / cls.PRIOR_VARIANCE
            second_deriv -= 1.0 / cls.PRIOR_VARIANCE

            for diff, disc, correct in responses:
                p = cls.probability_correct(theta, diff, disc)
                w = p * (1.0 - p)
                first_deriv += disc * (correct - p)
                second_deriv -= (disc ** 2) * w

            if abs(second_deriv) < 1e-9:
                break

            step = -first_deriv / second_deriv
            # Apply damping
            step = max(-cls.MAX_STEP, min(cls.MAX_STEP, step))
            theta += step

            if abs(step) < cls.CONVERGENCE_THRESHOLD:
                break

        # Constrain theta to reasonable pedagogical bounds [-3.5, +3.5]
        theta = max(-3.5, min(3.5, theta))
        se = 1.0 / math.sqrt(abs(second_deriv)) if abs(second_deriv) > 0 else 1.0

        confidence = "High" if len(responses) >= 8 and se < 0.45 else ("Medium" if len(responses) >= 4 else "Low")

        return {
            "theta": round(theta, 3),
            "standard_error": round(se, 3),
            "confidence": confidence,
            "proficiency_band": cls.classify_proficiency(theta),
            "items_administered": len(responses)
        }

    @staticmethod
    def classify_proficiency(theta: float) -> str:
        if theta < -1.0:
            return "Foundational (Needs Prerequisites)"
        elif theta < 0.0:
            return "Developing (Building Core Concepts)"
        elif theta < 1.0:
            return "Proficient (Solid Concept Mastery)"
        else:
            return "Advanced (Exemplar / High Competitive Rank)"
