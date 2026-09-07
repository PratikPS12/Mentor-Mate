from typing import Dict, Any, Optional, List

class MisconceptionEngine:
    """
    Diagnostic error and misconception classifier.
    Analyzes student response choices, response time, hint usage, and historical patterns.
    """

    @staticmethod
    def diagnose_error(
        question: Dict[str, Any],
        selected_index: int,
        response_time_ms: int,
        hints_used: int,
        prior_concept_mastery: float,
        retention_estimate: float
    ) -> Dict[str, Any]:
        """
        Classifies an incorrect answer into specific error categories.
        """
        distractors = question.get("misconception_distractors", {})
        str_idx = str(selected_index)
        
        # 1. Distractor-specific misconception tagged in question bank
        if str_idx in distractors:
            specific_error = distractors[str_idx]
            error_type = specific_error.get("type", "misconception")
            description = specific_error.get("description", "Conceptual misconception detected.")
            confidence = 0.85
        else:
            error_type = "unclassified_error"
            description = "Incorrect response option selected."
            confidence = 0.50

        # 2. Time-pressure / impulsive error (e.g. answering < 3 seconds)
        if response_time_ms < 3500 and hints_used == 0:
            if prior_concept_mastery > 0.70:
                error_type = "careless_impulse_error"
                description = "Answered too quickly despite having high prior mastery."
                confidence = 0.80

        # 3. Retention lapse (high mastery historically, but low predicted current retention)
        elif prior_concept_mastery > 0.75 and retention_estimate < 0.40:
            error_type = "retention_failure"
            description = "Concepts learned in the past experienced memory decay over time."
            confidence = 0.75

        # 4. Prerequisite / Fundamental gap
        elif prior_concept_mastery < 0.30:
            error_type = "prerequisite_gap"
            description = "Foundational prerequisites for this concept have not yet been mastered."
            confidence = 0.80

        return {
            "error_type": error_type,
            "description": description,
            "confidence": confidence,
            "remediation_hint": question.get("hints", ["Review fundamental concept notes."])[0] if question.get("hints") else ""
        }
