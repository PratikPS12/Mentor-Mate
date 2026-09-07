import pytest
from app.core.database import db_manager
from app.services.curriculum.curriculum_engine import CurriculumEngine
from app.services.assessment.assessment_service import assessment_service
from app.services.recommendation.recommendation_service import RecommendationService

@pytest.mark.asyncio
async def test_curriculum_engine_syllabus_and_questions():
    # 1. NEET track should have Biology, Physics, Chemistry
    neet_syllabus = CurriculumEngine.get_syllabus_for_student("NEET", "12")
    assert "Biology" in neet_syllabus["subjects"]
    assert "Physics" in neet_syllabus["subjects"]
    assert "Chemistry" in neet_syllabus["subjects"]

    neet_qs = CurriculumEngine.get_questions_for_student("NEET", "12")
    assert len(neet_qs) >= 4
    subjects = {q["subject"] for q in neet_qs}
    assert "Biology" in subjects
    assert "Physics" in subjects

    # 2. JEE track should have Math, Physics, Chemistry
    jee_syllabus = CurriculumEngine.get_syllabus_for_student("JEE", "11")
    assert "Math" in jee_syllabus["subjects"]
    jee_qs = CurriculumEngine.get_questions_for_student("JEE", "11")
    jee_subjects = {q["subject"] for q in jee_qs}
    assert "Math" in jee_subjects
    assert "Physics" in jee_subjects

@pytest.mark.asyncio
async def test_curriculum_course_generation_aligned_with_student():
    # NEET Class 12 student with weak area in 'genetics'
    courses = CurriculumEngine.generate_courses_for_student("NEET", "12", ["genetics"])
    assert len(courses) >= 3
    tags = {c["tag"] for c in courses}
    assert "Biology" in tags
    assert "Physics" in tags
    assert "Chemistry" in tags

    # Verify weakness remedy flag
    bio_course = next((c for c in courses if c["tag"] == "Biology"), None)
    assert bio_course is not None
    assert bio_course["is_weakness_remedy"] is True

@pytest.mark.asyncio
async def test_assessment_session_weakness_evaluation_and_remediation():
    student_id = "test_student_eval_01"
    
    # Setup student profile as NEET Class 11
    profile_col = db_manager.get_collection("student_profiles")
    await profile_col.update_one(
        {"student_id": student_id},
        {"$set": {
            "student_id": student_id,
            "name": "NEET Aspirant",
            "goal": "NEET",
            "klass": "11",
            "weak_areas": []
        }},
        upsert=True
    )

    # Start assessment session
    session_data = await assessment_service.start_session(student_id, "diagnostic")
    session_id = session_data["session_id"]
    assert "NEET" in session_data.get("syllabus_name", "")

    # Answer all questions in session
    sessions_col = db_manager.get_collection("assessment_sessions")
    session = await sessions_col.find_one({"id": session_id})
    candidate_ids = session["candidate_questions"][:session["total_items"]]

    last_res = None
    for idx, qid in enumerate(candidate_ids):
        q = assessment_service.get_question_by_id(qid)
        # Intentionally answer the first question wrong to trigger weakness analysis
        selected_opt = (q["correct_index"] + 1) % len(q["options"]) if idx == 0 else q["correct_index"]
        
        last_res = await assessment_service.submit_answer(
            session_id=session_id,
            question_id=qid,
            selected_index=selected_opt,
            response_time_ms=8000,
            hints_used=0
        )

    assert last_res["is_complete"] is True
    report = last_res["evaluation_report"]
    assert report is not None

    # Check evaluation report components
    assert "overall_score" in report
    assert "percentage" in report
    assert "performance_tier" in report
    assert "subject_breakdown" in report
    assert len(report["subject_breakdown"]) > 0
    assert len(report["weaknesses"]) >= 1

    # Check weakness diagnostic details
    first_weak = report["weaknesses"][0]
    assert "error_type" in first_weak
    assert "remedial_action" in first_weak

    # Verify student profile weak_areas was automatically updated
    updated_prof = await profile_col.find_one({"student_id": student_id})
    assert len(updated_prof.get("weak_areas", [])) >= 1

    # Check remedial courses are generated
    assert len(report["remedial_courses"]) >= 1

@pytest.mark.asyncio
async def test_recommendation_catalog_for_user():
    student_id = "test_student_eval_01"
    catalog = await RecommendationService.get_catalog_for_user(student_id)
    assert len(catalog) >= 3
    # Check that course titles reference the student's goal (NEET)
    titles = [c["title"] for c in catalog]
    assert any("NEET" in t for t in titles)

@pytest.mark.asyncio
async def test_subject_accurate_video_lectures_no_cross_mismatch():
    # Test across multiple goals and grade levels
    for goal in ["NEET", "JEE", "CBSE", "State Board"]:
        for klass in ["10", "12"]:
            courses = CurriculumEngine.generate_courses_for_student(goal, klass)
            for c in courses:
                tag = c["tag"]
                modules = c.get("modules", [])
                assert len(modules) >= 1, f"Course {c['id']} must have modules"

                for m in modules:
                    v_url = m.get("video_url", "")
                    assert v_url.startswith("https://www.youtube.com/embed/"), f"Invalid embed in {c['id']}"

                    # Strictly verify no cross-subject contamination
                    if tag == "Biology":
                        assert "ZM8ECpBuQYE" not in v_url, f"Physics video in Biology course {c['title']}!"
                        assert any(vid in v_url for vid in ["URUJD5NEXC8", "Mehz7tCxjSE", "TNKWgcFPHqw", "itsb2SqR-R0"]), f"Non-bio video in Biology: {v_url}"
                    elif tag == "Chemistry":
                        assert "ZM8ECpBuQYE" not in v_url, f"Physics video in Chemistry course {c['title']}!"
                        assert any(vid in v_url for vid in ["cExhtwVT1v0", "oDigu9YxXUg", "wCspf85eQQo", "mAjrnZ-znkY", "g2g-G77qWpE"]), f"Non-chem video in Chemistry: {v_url}"
                    elif tag == "Math":
                        assert "ZM8ECpBuQYE" not in v_url, f"Physics video in Math course {c['title']}!"
                        assert any(vid in v_url for vid in ["ZBalWWHYQVE", "WUvTyaaNkzM", "rAof9Ld5sOg", "GkJ4jKxO9zQ"]), f"Non-math video in Math: {v_url}"

@pytest.mark.asyncio
async def test_free_accredited_external_courses():
    # 1. NEET student
    neet_free = CurriculumEngine.get_free_external_courses("NEET", "12")
    assert len(neet_free) >= 4
    platforms = {fc["platform"] for fc in neet_free}
    assert "Khan Academy" in platforms
    assert "MIT OpenCourseWare" in platforms
    assert "DIKSHA (NCERT)" in platforms
    assert all(fc["url"].startswith("http") for fc in neet_free)

    # 2. JEE student
    jee_free = CurriculumEngine.get_free_external_courses("JEE", "11")
    assert len(jee_free) >= 4
    jee_platforms = {fc["platform"] for fc in jee_free}
    assert "MIT OpenCourseWare" in jee_platforms
    assert "NPTEL / SWAYAM" in jee_platforms

    # 3. Secondary student (Class 10 State Board)
    sb_free = CurriculumEngine.get_free_external_courses("State Board", "10")
    assert len(sb_free) >= 4
    assert any("Class 10" in fc["title"] or "Class 10" in fc["class_level"] for fc in sb_free)

@pytest.mark.asyncio
async def test_enrolled_course_lookup_resolution():
    student_id = "test_student_enrolled_res"
    profile_col = db_manager.get_collection("student_profiles")
    await profile_col.update_one(
        {"student_id": student_id},
        {"$set": {
            "student_id": student_id,
            "name": "State Board Student",
            "goal": "State Board",
            "klass": "10",
            "enrolled_courses": [
                "Class 10 State Board Biology: Cell Architecture & Genetics",
                "Organic Chemistry Rapid Review"
            ]
        }},
        upsert=True
    )

    # Resolving enrolled_0
    course_0 = await RecommendationService.get_course_for_user("enrolled_0", student_id)
    assert course_0 is not None
    assert len(course_0.get("modules", [])) >= 1
    # Check that Biology module contains a Biology video, NOT physics
    assert "ZM8ECpBuQYE" not in course_0["modules"][0]["video_url"]

    # Resolving enrolled_1
    course_1 = await RecommendationService.get_course_for_user("enrolled_1", student_id)
    assert course_1 is not None
    assert len(course_1.get("modules", [])) >= 1
    assert "ZM8ECpBuQYE" not in course_1["modules"][0]["video_url"]

