import uuid
from typing import Dict, Any, List
from datetime import datetime, timezone
from app.core.database import db_manager
from app.services.student_model.retention_engine import RetentionEngine

class AdaptivePlannerService:
    """
    Adaptive constraint-based study planner.
    Generates personalized daily study blocks optimizing mastery progression and spaced retention.
    """

    @staticmethod
    async def generate_daily_plan(
        student_id: str,
        days_to_exam: int = 180,
        daily_hours: float = 3.0,
        subjects: List[str] = None
    ) -> Dict[str, Any]:
        subjects = subjects or ["Math", "Physics", "Chemistry"]
        plan_id = f"plan_{uuid.uuid4().hex[:12]}"

        # 1. Fetch student's current mastery and retention states
        mastery_col = db_manager.get_collection("mastery_states")
        retention_col = db_manager.get_collection("retention_states")
        profile_col = db_manager.get_collection("student_profiles")

        profile = await profile_col.find_one({"student_id": student_id})
        weak_areas = profile.get("weak_areas", []) if profile else []

        mastery_records = await mastery_col.find({"student_id": student_id})
        retention_records = await retention_col.find({"student_id": student_id})

        # Identify concepts due for spaced review (retention < 0.75)
        review_due_concepts = []
        for r in retention_records:
            cur_ret = RetentionEngine.calculate_current_retention(
                r.get("last_review", datetime.now(timezone.utc).isoformat()),
                r.get("memory_strength", 2.0)
            )
            if cur_ret <= 0.75:
                review_due_concepts.append(r.get("concept_id"))

        # Identify weakest concept
        weakest_concept = None
        min_mastery = 1.0
        for m in mastery_records:
            if m.get("mastery", 1.0) < min_mastery:
                min_mastery = m.get("mastery", 1.0)
                weakest_concept = m.get("concept_id")

        # Attempt AI LLM dynamic schedule generation
        goal = profile.get("goal", "Academic Prep") if profile else "Academic Prep"
        klass = str(profile.get("klass", "10")) if profile else "10"
        ai_tasks = await AdaptivePlannerService._generate_ai_study_tasks(
            goal=goal,
            klass=klass,
            days_to_exam=days_to_exam,
            daily_hours=daily_hours,
            subjects=subjects,
            weak_areas=weak_areas,
            weakest_concept=weakest_concept,
            min_mastery=min_mastery,
            review_due_concepts=review_due_concepts
        )

        if ai_tasks and len(ai_tasks) >= 3:
            tasks = ai_tasks
        else:
            total_minutes = int(daily_hours * 60)
            tasks = []

            # Determine subject assignments across tasks
            sub1 = subjects[0] if len(subjects) > 0 else "General"
            sub2 = subjects[1] if len(subjects) > 1 else sub1
            sub3 = subjects[2] if len(subjects) > 2 else (sub1 if len(subjects) == 1 else sub2)
            primary_subject = weak_areas[0] if weak_areas else sub1

            # Task 1: Warmup & Recall (10 - 15 mins)
            warmup_duration = 15 if total_minutes >= 120 else 10
            tasks.append({
                "id": f"task_{uuid.uuid4().hex[:8]}",
                "type": "warmup",
                "subject": sub1,
                "title": f"Warm-up: {sub1} Flashcard & Active Recall",
                "description": f"Rapid recall of high-frequency definitions, formulas, and theorems in {sub1}.",
                "duration_minutes": warmup_duration,
                "completed": False,
                "reason": "Activates neural pathways before intensive cognitive problem solving."
            })

            # Task 2: Core Concept Mastery (Primary Focus - 40-45% of time)
            core_duration = int(total_minutes * 0.40)
            core_title = f"Deep Dive: {primary_subject} Core Foundations & Derivations"
            core_reason = "High priority: weak area identified from assessment/marksheet evidence."

            from app.services.curriculum.curriculum_graph import CurriculumKnowledgeGraph
            if weakest_concept:
                # Check for foundational prerequisite gaps
                mastery_dict = {m.get("concept_id"): m.get("mastery", 0.5) for m in mastery_records}
                root_diagnosis = CurriculumKnowledgeGraph.diagnose_root_cause(weakest_concept, mastery_dict)
                if root_diagnosis["error_type"] == "prerequisite_gap":
                    core_title = f"Prerequisite Repair: {root_diagnosis['root_concept_name']}"
                    core_desc = f"{root_diagnosis['explanation']} Remediating prerequisite before advancing to {primary_subject}."
                    core_reason = f"Prerequisite Deficit: Master foundational '{root_diagnosis['root_concept_name']}' first."
                else:
                    core_desc = f"Targeted work on weak area '{primary_subject}' (Current mastery: {int(min_mastery*100)}%)."
            else:
                core_desc = f"Concept breakdown, structured derivations, and worked examples in {primary_subject}."

            tasks.append({
                "id": f"task_{uuid.uuid4().hex[:8]}",
                "type": "core_concept",
                "subject": primary_subject,
                "concept_id": weakest_concept,
                "title": core_title,
                "description": core_desc,
                "duration_minutes": core_duration,
                "completed": False,
                "reason": core_reason
            })

            # Task 3: Secondary Subject Practice (25% of time)
            sec_duration = int(total_minutes * 0.25)
            tasks.append({
                "id": f"task_{uuid.uuid4().hex[:8]}",
                "type": "secondary_subject",
                "subject": sub2,
                "title": f"Applied Practice: {sub2} Problem Sets",
                "description": f"8-10 focused problem solving and numerical drills in {sub2}.",
                "duration_minutes": sec_duration,
                "completed": False,
                "reason": "Maintains inter-subject momentum and prevents topic fatigue."
            })

            # Task 4: Spaced Repetition or Tertiary Subject Practice
            rem_duration = max(20, total_minutes - (warmup_duration + core_duration + sec_duration))
            if len(subjects) >= 3 and not review_due_concepts:
                tasks.append({
                    "id": f"task_{uuid.uuid4().hex[:8]}",
                    "type": "tertiary_subject",
                    "subject": sub3,
                    "title": f"Targeted Application: {sub3} Drills",
                    "description": f"Hands-on exercises and exam-style problem sets in {sub3}.",
                    "duration_minutes": rem_duration,
                    "completed": False,
                    "reason": f"Completes balanced syllabus distribution across {', '.join(subjects)}."
                })
            elif review_due_concepts:
                tasks.append({
                    "id": f"task_{uuid.uuid4().hex[:8]}",
                    "type": "spaced_revision",
                    "subject": "Integrated",
                    "title": "Spaced Repetition Review (Memory Decay Due)",
                    "description": f"Memory retention for {len(review_due_concepts)} concepts has dropped below 75% threshold.",
                    "duration_minutes": rem_duration,
                    "completed": False,
                    "reason": "Ebbinghaus spaced repetition schedule mandates timely consolidation."
                })
            else:
                tasks.append({
                    "id": f"task_{uuid.uuid4().hex[:8]}",
                    "type": "spaced_revision",
                    "subject": "Integrated",
                    "title": f"{goal} Applied Problem Solving & Error Analysis",
                    "description": f"Solve focused application drills and diagnostic problems. Target date in {days_to_exam} days.",
                    "duration_minutes": rem_duration,
                    "completed": False,
                    "reason": "Calibrates exam speed, accuracy, and eliminates recurring error traps."
                })

        # Calculate realistic chronological time slots and category labels
        from datetime import datetime as dt, timedelta
        current_clock = dt(2026, 1, 1, 9, 0)
        for t in tasks:
            dur = t.get("duration_minutes", 30)
            end_clock = current_clock + timedelta(minutes=dur)
            t["time_slot"] = f"{current_clock.strftime('%I:%M %p')} - {end_clock.strftime('%I:%M %p')}"
            current_clock = end_clock + timedelta(minutes=5 if dur <= 30 else 10)

            t_type = t.get("type", "")
            if t_type == "warmup":
                t["category"] = "Warm-up"
                t["priority"] = "High"
                t["suggested_method"] = "Active Recall & Flashcards"
            elif t_type in ["core_concept", "deep_dive"]:
                t["category"] = "Deep Dive"
                t["priority"] = "Essential"
                t["suggested_method"] = "Feynman Technique & Derivations"
            elif t_type in ["secondary_subject", "tertiary_subject", "practice"]:
                t["category"] = "Applied Drill"
                t["priority"] = "High"
                t["suggested_method"] = "Timed Problem Solving"
            else:
                t["category"] = "Spaced Review"
                t["priority"] = "Medium"
                t["suggested_method"] = "Error Log & Retrieval Practice"

        plan_doc = {
            "id": plan_id,
            "student_id": student_id,
            "days_to_exam": days_to_exam,
            "daily_hours": daily_hours,
            "subjects": subjects,
            "tasks": tasks,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

        plans_col = db_manager.get_collection("study_plans")
        await plans_col.insert_one(plan_doc)

        return plan_doc

    @staticmethod
    async def toggle_task_completion(plan_id: str, task_id: str, completed: bool) -> Dict[str, Any]:
        plans_col = db_manager.get_collection("study_plans")
        plan = await plans_col.find_one({"id": plan_id})
        if not plan:
            raise ValueError("Plan not found")

        tasks = plan.get("tasks", [])
        for t in tasks:
            if t["id"] == task_id:
                t["completed"] = completed
                break

        completed_count = sum(1 for t in tasks if t.get("completed", False))
        rate = round((completed_count / len(tasks)) * 100, 1) if tasks else 0.0

        await plans_col.update_one(
            {"id": plan_id},
            {"$set": {"tasks": tasks, "completion_rate": rate}}
        )

        return {"plan_id": plan_id, "task_id": task_id, "completed": completed, "completion_rate": rate}

    @staticmethod
    async def _generate_ai_study_tasks(
        goal: str,
        klass: str,
        days_to_exam: int,
        daily_hours: float,
        subjects: List[str],
        weak_areas: List[str],
        weakest_concept: Optional[str] = None,
        min_mastery: float = 1.0,
        review_due_concepts: List[str] = None
    ) -> List[Dict[str, Any]]:
        from app.services.ai.registry import AIProviderRegistry
        from app.services.ai.task_router import AITaskRouter, AITaskType
        import re, json, logging
        logger = logging.getLogger("mentormate.planner")

        provider = AIProviderRegistry.get_provider()
        model = AITaskRouter.get_model_for_task(AITaskType.PRIMARY)
        total_minutes = int(daily_hours * 60)

        prompt = (
            f"You are an elite academic daily scheduler designing an optimal daily study schedule for a student.\n"
            f"Student Parameters:\n"
            f"- Academic Level: Class/Degree {klass}\n"
            f"- Target Exam Goal: {goal}\n"
            f"- Days to Exam: {days_to_exam} days remaining\n"
            f"- Daily Available Time: {daily_hours} hours ({total_minutes} minutes total)\n"
            f"- Input Target Subjects: {', '.join(subjects)}\n"
            f"- Input Weak Areas to Prioritize: {', '.join(weak_areas) if weak_areas else 'Core syllabus'}\n\n"
            f"Generate exactly 4 structured, realistic daily study tasks that sum to approximately {total_minutes} minutes:\n"
            "1. Task 1: Warmup & Recall (10-15 mins)\n"
            "2. Task 2: Core Concept Deep-Dive (40-45% of time, directly attacking their weak areas)\n"
            "3. Task 3: Secondary Subject Application & Problem Set (25-30% of time)\n"
            "4. Task 4: Spaced Retrieval Diagnostic / Rapid Review (15-20% of time)\n\n"
            "Return STRICTLY a JSON array of objects (no markdown fences, no conversational text) matching this schema:\n"
            "[\n"
            "  {\n"
            '    "type": "warmup | core_concept | secondary_subject | spaced_revision",\n'
            '    "subject": "Subject Name",\n'
            '    "title": "Specific actionable task title",\n'
            '    "description": "Concrete instructions on what problem sets or concept derivations to execute",\n'
            '    "duration_minutes": 45,\n'
            '    "reason": "Why this specific task is prioritized based on their goal and weak areas"\n'
            "  }\n"
            "]"
        )

        try:
            res = await provider.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=0.3,
                max_tokens=2000
            )
            raw = res.get("content", "").strip()
            match = re.search(r'\[\s*\{.*\}\s*\]', raw, re.DOTALL)
            raw_json = match.group(0) if match else raw.strip('`').replace('```json', '').replace('```', '').strip()
            items = json.loads(raw_json)
            if isinstance(items, list) and len(items) >= 3:
                valid_items = [
                    it for it in items
                    if isinstance(it, dict)
                    and it.get("title")
                    and it.get("title").strip().lower() not in ["", "study block", "task", "block"]
                ]
                # Ensure titles aren't all identical
                unique_titles = {it["title"].strip().lower() for it in valid_items}
                if len(valid_items) >= 3 and len(unique_titles) >= 2:
                    ai_tasks = []
                    for item in valid_items:
                        ai_tasks.append({
                            "id": f"task_{uuid.uuid4().hex[:8]}",
                            "type": item.get("type", "core_concept"),
                            "subject": item.get("subject", subjects[0] if subjects else "Core"),
                            "title": item.get("title").strip(),
                            "description": item.get("description", "Targeted concept mastery and practice.").strip(),
                            "duration_minutes": int(item.get("duration_minutes", 30)),
                            "completed": False,
                            "reason": item.get("reason", "Directly targets syllabus requirements.").strip()
                        })
                    return ai_tasks
        except Exception as e:
            logger.warning(f"AI Planner task generation failed ({e}). Using deterministic task synthesizer.")

        return []
