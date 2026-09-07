from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from app.routes.auth_routes import get_current_user
from app.services.planner.planner_service import AdaptivePlannerService

router = APIRouter(prefix="/schedule", tags=["Adaptive Study Planner"])

@router.post("/generate")
async def generate_plan(
    days_to_exam: int = Query(180),
    daily_hours: float = Query(3.0),
    subjects: Optional[str] = Query("Math, Physics, Chemistry"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    sub_list = [s.strip() for s in subjects.split(",") if s.strip()] if subjects else ["Math", "Physics", "Chemistry"]
    plan = await AdaptivePlannerService.generate_daily_plan(
        student_id=user["id"],
        days_to_exam=days_to_exam,
        daily_hours=daily_hours,
        subjects=sub_list
    )
    return plan

@router.post("/{plan_id}/task/{task_id}/toggle")
async def toggle_task(
    plan_id: str,
    task_id: str,
    completed: bool = Body(..., embed=True),
    user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        res = await AdaptivePlannerService.toggle_task_completion(plan_id, task_id, completed)
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
