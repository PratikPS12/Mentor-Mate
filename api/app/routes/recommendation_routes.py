from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query, Body
from app.routes.auth_routes import get_current_user
from app.services.recommendation.recommendation_service import RecommendationService
from app.core.database import db_manager

router = APIRouter(prefix="/courses", tags=["Courses & Recommendations"])

@router.get("/catalog")
async def get_catalog(
    track: Optional[str] = Query(None),
    user: Dict[str, Any] = Depends(get_current_user)
):
    catalog = await RecommendationService.get_catalog_for_user(user["id"], track)
    return catalog

@router.get("/recommended")
async def get_recommended(user: Dict[str, Any] = Depends(get_current_user)):
    recommended = await RecommendationService.get_personalized_recommendations(user["id"])
    return recommended

@router.post("/enroll")
async def enroll_course(
    course_title: str = Body(..., embed=True),
    user: Dict[str, Any] = Depends(get_current_user)
):
    profile_col = db_manager.get_collection("student_profiles")
    prof = await profile_col.find_one({"student_id": user["id"]})
    enrolled = prof.get("enrolled_courses", []) if prof else []
    
    if course_title not in enrolled:
        enrolled.append(course_title)
        await profile_col.update_one(
            {"student_id": user["id"]},
            {"$set": {"enrolled_courses": enrolled}}
        )

    return {"message": f"Successfully enrolled in {course_title}", "enrolled_courses": enrolled}

@router.post("/unenroll")
async def unenroll_course(
    course_title: str = Body(..., embed=True),
    user: Dict[str, Any] = Depends(get_current_user)
):
    profile_col = db_manager.get_collection("student_profiles")
    prof = await profile_col.find_one({"student_id": user["id"]})
    enrolled = prof.get("enrolled_courses", []) if prof else []
    
    updated_enrolled = [c for c in enrolled if c.lower().strip() != course_title.lower().strip()]
    await profile_col.update_one(
        {"student_id": user["id"]},
        {"$set": {"enrolled_courses": updated_enrolled}}
    )

    return {"message": f"Successfully removed {course_title} from your enrolled courses", "enrolled_courses": updated_enrolled}

@router.get("/external/free")
async def get_free_external_courses(user: Dict[str, Any] = Depends(get_current_user)):
    return await RecommendationService.get_free_courses_for_user(user["id"])

@router.get("/{course_id}")
async def get_course_detail(
    course_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    course = await RecommendationService.get_course_for_user(course_id, user.get("id"))
    if not course:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Course not found")
    return course
