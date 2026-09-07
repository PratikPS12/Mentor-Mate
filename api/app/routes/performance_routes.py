from typing import Dict, Any, List
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends
from app.routes.auth_routes import get_current_user
from app.core.database import db_manager
from app.services.student_model.retention_engine import RetentionEngine

router = APIRouter(prefix="/performance", tags=["Performance & Learning Twin Analytics"])

@router.get("/summary")
async def get_performance_summary(user: Dict[str, Any] = Depends(get_current_user)):
    student_id = user["id"]
    sessions_col = db_manager.get_collection("assessment_sessions")
    mastery_col = db_manager.get_collection("mastery_states")
    retention_col = db_manager.get_collection("retention_states")
    events_col = db_manager.get_collection("learning_events")
    profile_col = db_manager.get_collection("student_profiles")

    profile = await profile_col.find_one({"student_id": student_id})
    sessions = await sessions_col.find({"student_id": student_id, "status": "completed"})
    mastery_records = await mastery_col.find({"student_id": student_id})
    retention_records = await retention_col.find({"student_id": student_id})
    events = await events_col.find({"student_id": student_id})

    # 1. Measured Performance (Real test scores)
    test_scores = []
    for s in sessions:
        total = len(s.get("answers", []))
        score = s.get("score", 0)
        pct = round((score / total) * 100) if total > 0 else 0
        test_scores.append({
            "session_id": s["id"],
            "date": s.get("created_at", "")[:10],
            "score": score,
            "total": total,
            "percentage": pct
        })

    # Weekly chart data (past 7 days)
    labels_day = []
    by_day = []
    now = datetime.now(timezone.utc)
    for i in range(6, -1, -1):
        day_date = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        labels_day.append(day_date[5:])  # MM-DD
        day_tests = [t for t in test_scores if t["date"] == day_date]
        if day_tests:
            avg_score = round(sum(t["percentage"] for t in day_tests) / len(day_tests))
        else:
            avg_score = 0
        by_day.append(avg_score)

    # Monthly chart data (4 weeks)
    week_avgs = [0, 0, 0, 0]
    week_counts = [0, 0, 0, 0]
    for t in test_scores:
        try:
            t_dt = datetime.fromisoformat(t["date"])
            days_ago = (now.date() - t_dt.date()).days
            if 0 <= days_ago < 28:
                w_idx = min(3, days_ago // 7)
                week_avgs[3 - w_idx] += t["percentage"]
                week_counts[3 - w_idx] += 1
        except Exception:
            pass
    monthly_data = [round(week_avgs[i] / week_counts[i]) if week_counts[i] > 0 else 0 for i in range(4)]

    # Yearly chart data (12 months)
    month_avgs = [0] * 12
    month_counts = [0] * 12
    for t in test_scores:
        try:
            m_idx = int(t["date"][5:7]) - 1
            month_avgs[m_idx] += t["percentage"]
            month_counts[m_idx] += 1
        except Exception:
            pass
    yearly_data = [round(month_avgs[i] / month_counts[i]) if month_counts[i] > 0 else 0 for i in range(12)]

    # 2. Model Estimates (BKT Mastery & Retention)
    concept_mastery_list = []
    avg_mastery = 0.0
    for m in mastery_records:
        cur_m = m.get("mastery", 0.35)
        concept_mastery_list.append({
            "concept_id": m.get("concept_id"),
            "mastery": cur_m,
            "uncertainty": m.get("uncertainty", 0.2),
            "evidence_count": m.get("evidence_count", 0)
        })
    if concept_mastery_list:
        avg_mastery = round(sum(c["mastery"] for c in concept_mastery_list) / len(concept_mastery_list), 3)

    # 3. Learning Twin State Synthesis
    from app.services.curriculum.curriculum_graph import CurriculumKnowledgeGraph
    import re

    def clean_concept_name(slug: str) -> str:
        if not slug:
            return "Core Academic Foundation"
        c_clean = slug.replace("concept_", "").replace("q_ai_", "")
        c_clean = re.sub(r'_[a-f0-9]{4,12}$', '', c_clean)
        parts = c_clean.split("_")
        if parts and parts[0] in ["math", "physics", "chem", "chemistry", "bio", "biology", "cs"]:
            topic = " ".join(parts[1:]).title()
            return f"{topic} ({parts[0].capitalize()})" if topic else parts[0].capitalize()
        return c_clean.replace("_", " ").title()

    if len(events) == 0 and len(concept_mastery_list) == 0:
        twin_priority = "Initial Baseline Calibration"
        twin_basis = "Initial Account Setup"
        twin_reason = "Based on Initial Account Setup: No assessment trials or marksheet data recorded yet for this student account."
        twin_action = "Complete a diagnostic test in the 'Test' tab or upload your marksheet to initialize ability tracking."
        twin_status = "Awaiting Student Evidence"
        confidence_level = "No Evidence Recorded"
    else:
        weak_concepts = [c for c in concept_mastery_list if c["mastery"] < 0.60]
        weak_concepts.sort(key=lambda x: x["mastery"])
        
        if weak_concepts:
            cid = weak_concepts[0]["concept_id"]
            cinfo = CurriculumKnowledgeGraph.get_concept(cid)
            clean_title = cinfo["name"] if cinfo else clean_concept_name(cid)

            # Detect exact source of cognitive evidence
            last_evt = await events_col.find_one({"student_id": student_id, "concept_id": cid})
            if last_evt:
                etype = str(last_evt.get("event_type", "")).lower()
                if "quiz" in etype or "course" in etype:
                    twin_basis = "Course Quiz"
                elif "notes" in etype or "material" in etype:
                    twin_basis = "Uploaded Study Notes AI Drill"
                elif "assessment" in etype or "test" in etype:
                    twin_basis = "Diagnostic Test Results"
                else:
                    twin_basis = "Verified Assessment Trials"
            elif len(sessions) > 0:
                twin_basis = "Diagnostic Test Results"
            elif profile and profile.get("weak_areas"):
                twin_basis = "Self-Reported Profile Weak Area"
            else:
                twin_basis = "Adaptive Cognitive Model"

            twin_priority = clean_title
            twin_reason = (
                f"Based on {twin_basis}: Mastery estimate is at {int(weak_concepts[0]['mastery']*100)}% based on verified student evidence."
            )
            twin_action = f"Execute 10 focused numerical practice drills in {clean_title}."
        else:
            twin_priority = "All Concepts Meeting Target Threshold"
            twin_basis = "Diagnostic Test Results"
            twin_reason = "Based on Diagnostic Test Results: All assessed concepts currently meet the 60% baseline confidence threshold."
            twin_action = "Attempt a full-syllabus mock diagnostic to elevate ability parameters."

        twin_status = "Active & Calibrating"
        confidence_level = "High" if len(events) >= 5 else "Calibrating Baseline"

    return {
        "charts": {
            "labels_day": labels_day,
            "by_day": by_day,
            "weekly_avg": monthly_data,
            "monthly_avg": yearly_data
        },
        "measured_metrics": {
            "total_assessments_taken": len(sessions),
            "total_questions_attempted": len(events),
            "recent_test_scores": test_scores[-5:]
        },
        "model_estimates": {
            "average_mastery": avg_mastery,
            "concepts_tracked": len(concept_mastery_list),
            "concept_masteries": concept_mastery_list
        },
        "learning_twin": {
            "status": twin_status,
            "current_focus_concept": twin_priority,
            "basis_source": twin_basis,
            "why": twin_reason,
            "next_best_action": twin_action,
            "confidence_level": confidence_level,
            "total_evidence_events": len(events)
        }
    }
