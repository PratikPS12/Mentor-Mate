import pytest
from app.services.student_model.bkt_engine import BKTEngine
from app.services.student_model.retention_engine import RetentionEngine
from app.services.student_model.misconception_engine import MisconceptionEngine

def test_bkt_correct_response_increases_mastery():
    prior = 0.30
    posterior, uncertainty = BKTEngine.update_mastery(
        prior_mastery=prior,
        is_correct=True,
        p_t=0.20,
        p_s=0.10,
        p_g=0.20
    )
    # With correct response, posterior must strictly increase above prior
    assert posterior > prior
    assert 0.0 < posterior < 1.0
    assert uncertainty == round(posterior * (1.0 - posterior), 4)

def test_bkt_incorrect_response_updates():
    prior = 0.60
    posterior, uncertainty = BKTEngine.update_mastery(
        prior_mastery=prior,
        is_correct=False,
        p_t=0.15,
        p_s=0.10,
        p_g=0.20
    )
    # Incorrect response should suppress mastery or constrain transition
    assert 0.0 < posterior < 1.0
    assert uncertainty > 0.0

def test_ebbinghaus_retention_decay():
    # Immediate retention
    now_iso = "2026-09-06T12:00:00+00:00"
    retention_now = RetentionEngine.calculate_current_retention(now_iso, memory_strength=5.0)
    assert 0.0 < retention_now <= 1.0

def test_retention_strength_update():
    new_s, last_rev, next_rev = RetentionEngine.update_memory_strength(
        prior_strength=2.0,
        is_successful=True,
        repetition_count=1
    )
    assert new_s > 2.0
    assert last_rev is not None
    assert next_rev is not None

def test_misconception_diagnosis():
    sample_q = {
        "misconception_distractors": {
            "0": {"type": "freshman_dream_misconception", "description": "Power distribution error"}
        },
        "hints": ["Remember that (a+b)^2 = (a+b)(a+b)"]
    }
    diag = MisconceptionEngine.diagnose_error(
        question=sample_q,
        selected_index=0,
        response_time_ms=12000,
        hints_used=0,
        prior_concept_mastery=0.40,
        retention_estimate=0.80
    )
    assert diag["error_type"] == "freshman_dream_misconception"
    assert diag["confidence"] > 0.8
