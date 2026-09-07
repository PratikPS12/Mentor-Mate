import pytest
from app.services.assessment.assessment_service import assessment_service
from app.core.database import db_manager

@pytest.mark.asyncio
async def test_full_ai_diagnostic_test_flow():
    # 1. Create a fresh student with no study history
    student_id = "test_ai_student_99"
    profile_col = db_manager.get_collection("student_profiles")
    await profile_col.update_one(
        {"student_id": student_id},
        {"$set": {
            "student_id": student_id,
            "name": "Arjun Sharma",
            "goal": "JEE",
            "klass": "11",
            "enrolled_courses": [],
            "weak_areas": []
        }},
        upsert=True
    )

    # 2. Check Studied Status for fresh student
    status = await assessment_service.get_student_studied_status(student_id)
    assert "has_studied" in status
    assert "suggested_topics" in status
    assert len(status["suggested_topics"]) > 0

    # 3. Student suggests a topic from their school/college class: "Thermodynamics"
    topic = "Thermodynamics"
    session_data = await assessment_service.start_session(
        student_id=student_id,
        assessment_type="diagnostic",
        topic=topic,
        num_questions=5
    )

    assert session_data["status"] == "active"
    assert session_data["total_items"] == 5
    first_q = session_data["current_question"]
    assert first_q is not None
    assert first_q["question_number"] == 1
    assert first_q["total_questions"] == 5
    assert len(first_q["options"]) == 4
    assert len(first_q["hints"]) >= 1

    session_id = session_data["session_id"]
    asked_ids = [first_q["id"]]

    # 4. Sequentially answer all 5 questions
    curr_q = first_q
    step = 1
    final_res = None

    while curr_q and step <= 5:
        # Submit answer (choose option 0)
        res = await assessment_service.submit_answer(
            session_id=session_id,
            question_id=curr_q["id"],
            selected_index=0,
            response_time_ms=10000,
            hints_used=0
        )
        if step < 5:
            assert not res["is_complete"], f"Step {step} should not be complete yet"
            assert res["next_question"] is not None
            next_q = res["next_question"]
            assert next_q["id"] not in asked_ids, "Question repeated! Found duplicate question in sequence."
            asked_ids.append(next_q["id"])
            assert next_q["question_number"] == step + 1
            curr_q = next_q
        else:
            assert res["is_complete"], "Session should be complete on question 5"
            final_res = res
            curr_q = None
        step += 1

    # 5. Verify Definitive Evaluation Report
    assert final_res is not None
    report = final_res["evaluation_report"]
    assert report is not None
    assert "overall_score" in report
    assert "percentage" in report
    assert "performance_tier" in report
    assert "question_reviews" in report
    assert len(report["question_reviews"]) == 5
    assert "remedial_courses" in report

    # 6. Verify each review item has explanation and answer context
    for qr in report["question_reviews"]:
        assert qr["question_text"]
        assert len(qr["options"]) == 4
        assert qr["explanation"]
