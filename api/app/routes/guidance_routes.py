import json
import logging
import re
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from app.routes.auth_routes import get_current_user
from app.services.ai.registry import AIProviderRegistry
from app.services.ai.task_router import AITaskRouter, AITaskType
from app.core.database import db_manager

logger = logging.getLogger("mentormate.guidance")

router = APIRouter(prefix="/guidance", tags=["AI Academic Guidance"])

class GuidanceRequest(BaseModel):
    goal: Optional[str] = "Academic Prep"
    klass: Optional[str] = "10"
    daily_hours: Optional[float] = 3.0
    weak_areas: Optional[List[str]] = []
    subjects: Optional[List[str]] = []

@router.post("/generate")
async def generate_ai_guidance(
    payload: GuidanceRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Dynamically generates personalized academic strategic guidance via the AI LLM
    based purely on the student's exact goal, class level, input weak areas, and daily study hours.
    """
    student_id = user["id"]
    profile_col = db_manager.get_collection("student_profiles")
    profile = await profile_col.find_one({"student_id": student_id}) or {}

    goal = payload.goal or profile.get("goal") or "Academic Prep"
    klass = payload.klass or profile.get("klass") or "10"
    daily_hours = payload.daily_hours or profile.get("daily_available_hours") or 3.0
    weak_areas = payload.weak_areas or profile.get("weak_areas") or []
    subjects = payload.subjects or []

    # If subjects empty, default from weak areas or curriculum
    if not subjects:
        if weak_areas:
            subjects = list(weak_areas)
        else:
            subjects = ["Core Syllabus", "Quantitative / Analytical Problem Solving"]

    provider = AIProviderRegistry.get_provider()
    model = AITaskRouter.get_model_for_task(AITaskType.PRIMARY)

    prompt = (
        f"You are a world-class academic strategist designing an elite, personalized study roadmap for a student.\n"
        f"Student Profile:\n"
        f"- Academic Tier: Class/Degree {klass}\n"
        f"- Target Goal / Exam: {goal}\n"
        f"- Daily Available Study Time: {daily_hours} hours/day\n"
        f"- Explicit Input Weak Areas: {', '.join(weak_areas) if weak_areas else 'None explicitly tagged yet'}\n"
        f"- Core Subjects in Focus: {', '.join(subjects)}\n\n"
        "Generate a highly specific, non-generic, high-impact guidance roadmap. "
        "Strictly address the student's exact weak areas and target goal with realistic tactics.\n\n"
        "Return STRICTLY a valid JSON object matching this schema (no markdown fences, no conversational preamble):\n"
        "{\n"
        '  "executive_strategy": "2-3 sentences outlining the master strategy tailored to this exact goal and hours",\n'
        '  "weak_area_action_plan": [\n'
        '    {\n'
        '      "weak_area": "Exact weak area name",\n'
        '      "tactical_remedy": "Step-by-step diagnostic and conceptual remediation strategy",\n'
        '      "recommended_practice": "Targeted problem sets, drills, or projects to execute"\n'
        '    }\n'
        '  ],\n'
        '  "subject_time_allocation": [\n'
        '    {\n'
        '      "subject": "Subject Name",\n'
        '      "percentage": 40,\n'
        '      "weekly_hours": 8.5\n'
        '    }\n'
        '  ],\n'
        '  "milestone_timeline": [\n'
        '    {\n'
        '      "phase": "Weeks 1-4",\n'
        '      "milestone": "Milestone objective",\n'
        '      "action": "Concrete test or evaluation to complete"\n'
        '    }\n'
        '  ],\n'
        '  "pitfalls_to_avoid": [\n'
        '    "Specific common trap for students preparing for this goal"\n'
        '  ]\n'
        "}"
    )

    try:
        res = await provider.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0.3,
            max_tokens=2500
        )
        raw = res.get("content", "").strip()
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        raw_json = match.group(0) if match else raw.strip('`').replace('```json', '').replace('```', '').strip()
        data = json.loads(raw_json)
        return {"success": True, "guidance": data}
    except Exception as e:
        logger.warning(f"AI Guidance LLM generation failed ({e}). Using deterministic synthesizer.")

    # Fallback synthesizer if offline
    weekly_total = round(daily_hours * 7, 1)
    allocations = []
    if weak_areas:
        allocations.append({"subject": weak_areas[0], "percentage": 45, "weekly_hours": round(weekly_total * 0.45, 1)})
        remaining = [s for s in subjects if s != weak_areas[0]]
        if remaining:
            allocations.append({"subject": remaining[0], "percentage": 35, "weekly_hours": round(weekly_total * 0.35, 1)})
            allocations.append({"subject": "Review & Practice Mock Drills", "percentage": 20, "weekly_hours": round(weekly_total * 0.20, 1)})
        else:
            allocations.append({"subject": "Active Recall & Retesting", "percentage": 55, "weekly_hours": round(weekly_total * 0.55, 1)})
    else:
        allocations = [
            {"subject": subjects[0] if subjects else "Core Theory", "percentage": 50, "weekly_hours": round(weekly_total * 0.5, 1)},
            {"subject": "Applied Problem Solving", "percentage": 30, "weekly_hours": round(weekly_total * 0.3, 1)},
            {"subject": "Spaced Revision & Diagnostics", "percentage": 20, "weekly_hours": round(weekly_total * 0.2, 1)}
        ]

    synth_actions = []
    for wa in (weak_areas or [subjects[0] if subjects else "Foundations"]):
        synth_actions.append({
            "weak_area": wa,
            "tactical_remedy": f"Deconstruct {wa} into core axioms. Isolate conceptual prerequisites using the Socratic Mentor before attempting multi-step problems.",
            "recommended_practice": f"Execute 8 targeted diagnostic drills in {wa} followed by error post-mortems."
        })

    fallback_data = {
        "executive_strategy": f"Strategic {daily_hours}h/day roadmap calibrated for {goal} (Class/Degree {klass}). 50% time focused on prioritized weak areas with structured active recall intervals.",
        "weak_area_action_plan": synth_actions,
        "subject_time_allocation": allocations,
        "milestone_timeline": [
            {"phase": "Phase 1: Foundation", "milestone": "Prerequisite Repair", "action": f"Complete diagnostic tests for {', '.join(weak_areas) if weak_areas else 'core syllabus'}."},
            {"phase": "Phase 2: Mastery", "milestone": "Full Syllabus Integration", "action": "Timed adaptive mock drills with Bayesian mastery > 80%."}
        ],
        "pitfalls_to_avoid": [
            "Passive rereading instead of active problem solving.",
            "Ignoring error post-mortems when answering questions incorrectly."
        ]
    }
    return {"success": True, "guidance": fallback_data}
