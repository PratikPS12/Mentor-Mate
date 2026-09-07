from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.routes.auth_routes import get_current_user
from app.services.assessment.assessment_service import assessment_service
from app.models.schemas import AssessmentAnswerSubmit

router = APIRouter(prefix="/assessment", tags=["Adaptive Assessment"])

@router.get("/studied-status")
async def get_studied_status(
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Verifies what the student has actually studied on the platform
    (enrolled courses, uploaded notes, study plan tasks) or returns syllabus suggestions.
    """
    return await assessment_service.get_student_studied_status(user["id"])

@router.post("/start")
async def start_assessment(
    assessment_type: str = Query("diagnostic"),
    subject_focus: Optional[str] = Query(None),
    topic: Optional[str] = Query(None),
    num_questions: int = Query(5),
    only_studied: bool = Query(False),
    user: Dict[str, Any] = Depends(get_current_user)
):
    session_data = await assessment_service.start_session(
        student_id=user["id"],
        assessment_type=assessment_type,
        subject_focus=subject_focus,
        topic=topic,
        num_questions=num_questions,
        only_studied=only_studied
    )
    return session_data

@router.post("/{session_id}/answer")
async def submit_answer(
    session_id: str,
    payload: AssessmentAnswerSubmit,
    user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        result = await assessment_service.submit_answer(
            session_id=session_id,
            question_id=payload.question_id,
            selected_index=payload.selected_index,
            response_time_ms=payload.response_time_ms,
            hints_used=payload.hints_used
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{session_id}/results")
async def get_results(
    session_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        results = await assessment_service.get_session_results(session_id)
        return results
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
