import pytest
from app.services.ai.registry import AIProviderRegistry
from app.services.ai.task_router import AITaskRouter, AITaskType
from app.services.student_model.irt_engine import IRTEngine
from app.services.assessment.adaptive_engine import AdaptiveAssessmentEngine
from app.services.curriculum.curriculum_graph import CurriculumKnowledgeGraph
from app.services.rag.rag_service import RAGService
from app.services.tutor.tutor_service import PedagogicalTutorService

@pytest.mark.asyncio
async def test_ai_provider_registry_and_health():
    provider = AIProviderRegistry.get_provider()
    assert provider is not None

    health = await AIProviderRegistry.get_health()
    assert "provider" in health
    assert health["status"] in ["connected", "ready_fallback", "ready"]

@pytest.mark.asyncio
async def test_ai_task_router():
    model_reasoning = AITaskRouter.get_model_for_task(AITaskType.REASONING)
    assert isinstance(model_reasoning, str) and len(model_reasoning) > 0

    model_fast = AITaskRouter.get_model_for_task(AITaskType.FAST)
    assert isinstance(model_fast, str) and len(model_fast) > 0

def test_irt_engine_probability_and_fisher_information():
    # When ability equals difficulty, probability should be 0.5
    p_equal = IRTEngine.probability_correct(theta=0.0, difficulty=0.0, discrimination=1.0)
    assert abs(p_equal - 0.5) < 1e-5

    # High ability should have higher probability
    p_high = IRTEngine.probability_correct(theta=1.5, difficulty=0.0, discrimination=1.0)
    assert p_high > 0.8

    # Fisher information is maximized when theta == difficulty
    info_max = IRTEngine.fisher_information(theta=0.0, difficulty=0.0, discrimination=1.0)
    info_sub = IRTEngine.fisher_information(theta=2.0, difficulty=0.0, discrimination=1.0)
    assert info_max > info_sub

def test_irt_ability_estimation():
    # Student who gets easy and medium questions right should have positive theta
    responses = [
        (-1.0, 1.2, 1), # Easy correct
        (0.0, 1.2, 1),  # Medium correct
        (1.0, 1.2, 0)   # Hard incorrect
    ]
    est = IRTEngine.estimate_ability_map(responses)
    assert "theta" in est
    assert est["theta"] >= -0.5
    assert "standard_error" in est
    assert "proficiency_band" in est

def test_adaptive_cat_question_selection():
    candidates = [
        {"id": "q1", "difficulty": "easy", "discrimination": 1.0, "concept_id": "c1"},
        {"id": "q2", "difficulty": "hard", "discrimination": 1.2, "concept_id": "c2"}
    ]
    # For a high ability student (theta = 1.2), the hard question provides more utility
    selected = AdaptiveAssessmentEngine.select_next_question(
        candidate_questions=candidates,
        administered_ids=[],
        current_theta=1.2
    )
    assert selected is not None
    assert selected["id"] == "q2"

def test_curriculum_knowledge_graph_prerequisites():
    prereqs = CurriculumKnowledgeGraph.get_all_prerequisites("math_differential_calc")
    assert "concept_math_quad_roots" in prereqs or "math_functions_limits" in prereqs

    # Root cause diagnosis when foundational prerequisite is unmastered
    diagnosis = CurriculumKnowledgeGraph.diagnose_root_cause(
        failed_concept_id="concept_math_quad_roots",
        student_masteries={"math_poly_factor": 0.35, "math_linear_eq": 0.90}
    )
    assert diagnosis["error_type"] == "prerequisite_gap"
    assert diagnosis["root_concept_id"] == "math_poly_factor"

@pytest.mark.asyncio
async def test_rag_chunking_and_retrieval():
    test_text = (
        "In Newtonian Mechanics, the second law states that the net force acting on a body "
        "equals the rate of change of momentum: F = m * a.\n\n"
        "Conservation of linear momentum holds whenever external forces sum to zero."
    )
    chunks = await RAGService.index_document_chunks(
        student_id="test_student_rag",
        document_id="doc_test_1",
        title="Physics Notes",
        text_content=test_text,
        subject="Physics"
    )
    assert len(chunks) >= 1

    retrieved = await RAGService.retrieve_relevant_context(
        student_id="test_student_rag",
        query="Explain Newton's second law F = m * a",
        subject_filter="Physics"
    )
    assert len(retrieved) >= 1
    assert "Newtonian Mechanics" in retrieved[0]["content"]

@pytest.mark.asyncio
async def test_pedagogical_tutor_socratic_message():
    res = await PedagogicalTutorService.process_student_message(
        student_id="test_student_tutor",
        message="Can you solve 3x + 6 = 15?"
    )
    assert res["role"] == "Mentor"
    assert "content" in res
    assert "x = 3" in res["content"] or "SymPy" in res["content"]
    assert "citations" in res
