from typing import Dict, Any, List
from fastapi import APIRouter, Depends, Query
from app.routes.auth_routes import get_current_user
from app.services.tutor.tutor_service import PedagogicalTutorService
from app.core.database import db_manager
from app.models.schemas import TutorMessagePayload

router = APIRouter(prefix="/tutor", tags=["AI Mentor"])

@router.post("/message")
async def send_tutor_message(
    payload: TutorMessagePayload,
    user: Dict[str, Any] = Depends(get_current_user)
):
    response = await PedagogicalTutorService.process_student_message(
        student_id=user["id"],
        message=payload.message,
        session_id=payload.session_id
    )
    return response

@router.get("/conversations")
@router.get("/history")
async def get_conversations(
    limit: int = Query(20),
    user: Dict[str, Any] = Depends(get_current_user)
):
    conv_col = db_manager.get_collection("conversations")
    all_convs = await conv_col.find()
    user_convs = [c for c in all_convs if c.get("student_id") == user["id"]]
    user_convs.sort(key=lambda x: x.get("created_at", ""))
    return user_convs[-limit:]
