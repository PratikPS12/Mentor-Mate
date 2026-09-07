from typing import Dict, Any, List
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import db_manager
from app.routes.auth_routes import get_current_user
from app.models.schemas import StudentProfileUpdate

router = APIRouter(prefix="/student", tags=["Student Profile & Attendance"])

@router.get("/profile")
async def get_profile(user: Dict[str, Any] = Depends(get_current_user)):
    profile_col = db_manager.get_collection("student_profiles")
    prof = await profile_col.find_one({"student_id": user["id"]})
    if not prof:
        raise HTTPException(status_code=404, detail="Profile not found")
    return prof

@router.put("/profile")
async def update_profile(payload: StudentProfileUpdate, user: Dict[str, Any] = Depends(get_current_user)):
    profile_col = db_manager.get_collection("student_profiles")
    users_col = db_manager.get_collection("users")
    
    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    if "name" in update_data:
        await users_col.update_one({"id": user["id"]}, {"$set": {"name": update_data["name"]}})

    await profile_col.update_one(
        {"student_id": user["id"]},
        {"$set": update_data},
        upsert=True
    )

    updated_prof = await profile_col.find_one({"student_id": user["id"]})
    return {"message": "Profile updated successfully", "profile": updated_prof}

@router.post("/attendance/mark-today")
async def mark_studied_today(user: Dict[str, Any] = Depends(get_current_user)):
    today_key = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    att_col = db_manager.get_collection("attendance_logs")
    
    await att_col.update_one(
        {"student_id": user["id"], "date": today_key},
        {"$set": {
            "student_id": user["id"],
            "date": today_key,
            "studied": True,
            "recorded_at": datetime.now(timezone.utc).isoformat()
        }},
        upsert=True
    )

    streak_info = await calculate_weekly_streak(user["id"])
    return {
        "message": "Today marked as studied successfully",
        "date": today_key,
        "streak_days": streak_info["streak_days"],
        "streak_percentage": streak_info["percentage"]
    }

@router.get("/attendance")
async def get_attendance(user: Dict[str, Any] = Depends(get_current_user)):
    att_col = db_manager.get_collection("attendance_logs")
    logs = await att_col.find({"student_id": user["id"]}, sort_by="date", ascending=False)
    streak_info = await calculate_weekly_streak(user["id"])
    return {
        "streak": streak_info,
        "history": logs
    }

async def calculate_weekly_streak(student_id: str) -> Dict[str, Any]:
    att_col = db_manager.get_collection("attendance_logs")
    now = datetime.now(timezone.utc)
    # Match JS getDay(): Sunday = 0, Monday = 1, etc.
    days_since_sunday = (now.weekday() + 1) % 7
    start_of_week = now - timedelta(days=days_since_sunday)
    studied_days = 0

    for i in range(7):
        day_date = (start_of_week + timedelta(days=i)).strftime("%Y-%m-%d")
        rec = await att_col.find_one({"student_id": student_id, "date": day_date})
        if rec and rec.get("studied"):
            studied_days += 1

    return {
        "streak_days": studied_days,
        "max_days": 7,
        "percentage": round((studied_days / 7) * 100, 1)
    }

@router.get("/dashboard")
async def get_dashboard_summary(user: Dict[str, Any] = Depends(get_current_user)):
    student_id = user["id"]
    profile_col = db_manager.get_collection("student_profiles")
    mastery_col = db_manager.get_collection("mastery_states")
    retention_col = db_manager.get_collection("retention_states")
    sessions_col = db_manager.get_collection("assessment_sessions")
    plans_col = db_manager.get_collection("study_plans")

    profile = await profile_col.find_one({"student_id": student_id}) or {}
    streak_info = await calculate_weekly_streak(student_id)
    mastery_records = await mastery_col.find({"student_id": student_id})
    retention_records = await retention_col.find({"student_id": student_id})
    last_session = await sessions_col.find({"student_id": student_id, "status": "completed"}, sort_by="created_at", ascending=False)
    latest_plan = await plans_col.find({"student_id": student_id}, sort_by="generated_at", ascending=False)

    # 1. Today's Focus & Current Priority
    from app.services.student_model.retention_engine import RetentionEngine
    from app.services.curriculum.curriculum_graph import CurriculumKnowledgeGraph
    import re

    def clean_concept_name(slug: str) -> str:
        c_clean = slug.replace("concept_", "").replace("q_ai_", "")
        c_clean = re.sub(r'_[a-f0-9]{4,12}$', '', c_clean)
        parts = c_clean.split("_")
        if parts and parts[0] in ["math", "physics", "chem", "chemistry", "bio", "biology", "cs"]:
            topic = " ".join(parts[1:]).title()
            return f"{topic} ({parts[0].capitalize()})" if topic else parts[0].capitalize()
        return c_clean.replace("_", " ").title()

    weak_areas = profile.get("weak_areas", [])
    today_focus = None

    # Find lowest mastery concept
    lowest_concept = None
    min_mastery = 1.0
    for m in mastery_records:
        if m.get("mastery", 1.0) < min_mastery:
            min_mastery = m.get("mastery", 1.0)
            lowest_concept = m

    if lowest_concept:
        cid = lowest_concept.get("concept_id", "")
        cinfo = CurriculumKnowledgeGraph.get_concept(cid)
        concept_name = cinfo["name"] if cinfo else clean_concept_name(cid)
        subject_name = cinfo["subject"] if cinfo else ("Academic Core" if not profile.get("goal") else profile.get("goal"))

        # Determine evidence source
        events_col = db_manager.get_collection("learning_events")
        last_evt = await events_col.find_one({"student_id": student_id, "concept_id": cid})
        if last_evt:
            etype = last_evt.get("event_type", "")
            if "assessment" in etype or "test" in etype:
                basis_source = "Diagnostic Test Results"
            elif "notes" in etype or "material" in etype:
                basis_source = "Uploaded Study Notes AI Drill"
            else:
                basis_source = "Bayesian Student Model Evidence"
        elif last_session:
            basis_source = "Diagnostic Test Results"
        else:
            basis_source = "Verified Assessment Evidence"

        # Check for root cause prerequisite
        mastery_dict = {m.get("concept_id"): m.get("mastery", 0.5) for m in mastery_records}
        root_diag = CurriculumKnowledgeGraph.diagnose_root_cause(cid, mastery_dict)
        if root_diag["error_type"] == "prerequisite_gap":
            why_text = f"Based on {basis_source}: Struggle in '{concept_name}' stems from foundational gap in prerequisite '{root_diag['root_concept_name']}' (Mastery: {int(min_mastery * 100)}%)."
            action_text = f"Review {root_diag['root_concept_name']} with Socratic Mentor → 6 practice drills → retest."
            focus_title = f"{root_diag['root_concept_name']} (Prerequisite Repair)"
        else:
            why_text = f"Based on {basis_source}: Recent performance demonstrates {int(min_mastery * 100)}% mastery confidence requiring concept reinforcement."
            action_text = f"Review core principles of {concept_name} → 8 targeted practice drills."
            focus_title = concept_name

        today_focus = {
            "title": focus_title,
            "concept_id": cid,
            "subject": subject_name,
            "mastery_percent": int(min_mastery * 100),
            "basis_source": basis_source,
            "why": why_text,
            "next_action": action_text,
            "has_evidence": True
        }
    elif weak_areas:
        primary_weak = weak_areas[0]
        today_focus = {
            "title": f"{primary_weak} Core Concepts",
            "concept_id": f"concept_{primary_weak.lower().replace(' ', '_')}",
            "subject": primary_weak,
            "mastery_percent": 45,
            "basis_source": "Self-Reported Profile Weak Area",
            "why": f"Based on Self-Reported Profile Weak Area: Prioritized from your input weak areas in profile settings.",
            "next_action": f"Take a 5-question diagnostic in {primary_weak} to isolate specific misconceptions.",
            "has_evidence": True
        }
    else:
        today_focus = {
            "title": "Initial Baseline Calibration",
            "concept_id": "concept_baseline",
            "subject": profile.get("goal", "Academic Prep"),
            "mastery_percent": 0,
            "basis_source": "Initial Account Setup",
            "why": "Based on Initial Account Setup: No assessment trials or marksheet data recorded yet.",
            "next_action": "Complete a 5-question diagnostic in the 'Test' tab to initialize ability tracking.",
            "has_evidence": False
        }

    # 2. Upcoming Spaced Revision (Retention <= 0.75)
    upcoming_revision = []
    now_iso = datetime.now(timezone.utc).isoformat()
    for r in retention_records:
        ret_val = RetentionEngine.calculate_current_retention(
            r.get("last_review", now_iso),
            r.get("memory_strength", 2.0)
        )
        if ret_val <= 0.75:
            cid = r.get("concept_id", "")
            cinfo = CurriculumKnowledgeGraph.get_concept(cid)
            upcoming_revision.append({
                "concept_id": cid,
                "title": cinfo["name"] if cinfo else cid,
                "subject": cinfo["subject"] if cinfo else "Core",
                "retention_percent": int(ret_val * 100),
                "next_review": r.get("next_review", "")[:10]
            })

    # 3. Recent Assessment Preview
    recent_eval = None
    if last_session:
        s0 = last_session[0]
        rep = s0.get("evaluation_report") or {}
        recent_eval = {
            "session_id": s0.get("id"),
            "score": rep.get("overall_score", f"{s0.get('score', 0)}/6"),
            "percentage": rep.get("percentage", 0),
            "performance_tier": rep.get("performance_tier", "Completed"),
            "date": s0.get("created_at", "")[:10],
            "irt_ability": rep.get("irt_ability")
        }

    return {
        "streak": streak_info,
        "today_focus": today_focus,
        "upcoming_revision": upcoming_revision[:3],
        "recent_assessment": recent_eval,
        "current_plan": latest_plan[0] if latest_plan else None,
        "enrolled_courses": profile.get("enrolled_courses", []),
        "student_name": profile.get("name", "Student"),
        "goal": profile.get("goal", "CBSE"),
        "klass": str(profile.get("klass") or "10")
    }
