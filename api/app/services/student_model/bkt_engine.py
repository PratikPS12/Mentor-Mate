import math
from typing import Dict, Any, Tuple

class BKTEngine:
    """
    Bayesian Knowledge Tracing (BKT) Engine.
    Computes exact posterior mastery updates and future transition probabilities.
    """
    
    @staticmethod
    def update_mastery(
        prior_mastery: float,
        is_correct: bool,
        p_t: float = 0.20,
        p_s: float = 0.10,
        p_g: float = 0.20
    ) -> Tuple[float, float]:
        """
        Executes a single BKT step.
        Returns: (posterior_mastery, uncertainty)
        """
        # Ensure values stay strictly in valid bounds
        p_l = max(0.01, min(0.99, prior_mastery))
        p_t = max(0.01, min(0.50, p_t))
        p_s = max(0.01, min(0.40, p_s))
        p_g = max(0.01, min(0.40, p_g))

        if is_correct:
            # P(X=1 | L) = 1 - P(S)
            # P(X=1 | ~L) = P(G)
            num = (1.0 - p_s) * p_l
            den = num + p_g * (1.0 - p_l)
        else:
            # P(X=0 | L) = P(S)
            # P(X=0 | ~L) = 1 - P(G)
            num = p_s * p_l
            den = num + (1.0 - p_g) * (1.0 - p_l)

        if den <= 0:
            p_l_given_x = p_l
        else:
            p_l_given_x = num / den

        # Transition step: P(L_{t+1}) = P(L_t | X) + (1 - P(L_t | X)) * P(T)
        posterior = p_l_given_x + (1.0 - p_l_given_x) * p_t
        # Round posterior first, then calculate Bernoulli variance
        posterior = round(max(0.01, min(0.99, posterior)), 4)
        uncertainty = round(posterior * (1.0 - posterior), 4)

        return posterior, uncertainty

    @staticmethod
    def expected_correctness(mastery: float, p_s: float = 0.10, p_g: float = 0.20) -> float:
        """
        Expected probability that student answers next question correctly:
        P(Correct) = P(L)*(1 - P(S)) + (1 - P(L))*P(G)
        """
        p_l = max(0.0, min(1.0, mastery))
        return p_l * (1.0 - p_s) + (1.0 - p_l) * p_g
