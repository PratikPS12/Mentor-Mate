import pytest
from app.services.curriculum.curriculum_engine import CurriculumEngine
from app.services.document.study_material_service import StudyMaterialService

@pytest.mark.asyncio
async def test_resolve_goal_key():
    # Test Class 10
    assert CurriculumEngine.resolve_goal_key("10th Boards (CBSE)", "10") == "CBSE"
    assert CurriculumEngine.resolve_goal_key("ICSE Board Exam", "10") == "ICSE"
    
    # Test 11 / 12
    assert CurriculumEngine.resolve_goal_key("JEE Advanced 2026", "12") == "JEE"
    assert CurriculumEngine.resolve_goal_key("NEET Medical", "11") == "NEET"
    assert CurriculumEngine.resolve_goal_key("MHT-CET Entrance", "12") == "CET"
    
    # Test Undergraduate / Degree
    assert CurriculumEngine.resolve_goal_key("GATE CS 2027", "Degree") == "GATE"
    assert CurriculumEngine.resolve_goal_key("Software Placement DSA", "Degree") == "Software Engineering & Placements"
    assert CurriculumEngine.resolve_goal_key("Machine Learning & AI", "Degree") == "Data Science & AI"
    assert CurriculumEngine.resolve_goal_key("IIM CAT Prep", "Degree") == "CAT"
    assert CurriculumEngine.resolve_goal_key("College Engineering Semester", "Degree") == "Undergraduate"

@pytest.mark.asyncio
async def test_curriculum_undergraduate_courses():
    courses = CurriculumEngine.generate_courses_for_student("GATE", "Degree")
    assert len(courses) >= 3
    tags = [c["tag"] for c in courses]
    assert "Computer Science" in tags or "Operating Systems" in tags or "Database Systems" in tags or "Engineering Mathematics" in tags

@pytest.mark.asyncio
async def test_free_external_courses_undergrad():
    ext_courses = CurriculumEngine.get_free_external_courses("GATE", "Degree")
    assert len(ext_courses) >= 3
    providers = [c["provider"] for c in ext_courses]
    assert any("MIT" in p or "IIT" in p or "NPTEL" in p for p in providers)

@pytest.mark.asyncio
async def test_study_material_ocr_text_processing():
    # Test deterministic fallback and schema extraction
    sample_text = """
    Chapter 4: Quadratic Equations and Parabolic Trajectories
    Standard Form: ax^2 + bx + c = 0
    Quadratic Formula: x = (-b +- sqrt(b^2 - 4ac)) / (2a)
    Discriminant D = b^2 - 4ac determines nature of roots:
    If D > 0, two distinct real roots.
    If D = 0, two equal real roots.
    If D < 0, complex conjugate roots.
    Sum of roots: alpha + beta = -b/a
    Product of roots: alpha * beta = c/a
    """
    
    analysis = StudyMaterialService._deterministic_analysis_fallback(
        sample_text,
        title="Quadratic Equations",
        subject="Math",
        klass="10",
        goal="10th Boards"
    )
    
    assert "summary" in analysis
    assert "key_concepts" in analysis
    assert "key_formulas" in analysis
    assert len(analysis["generated_questions"]) >= 2
    assert "course_module" in analysis
    assert analysis["course_module"]["title"] == "Custom Module: Quadratic Equations"

@pytest.mark.asyncio
async def test_study_material_save_and_retrieve():
    student_id = "test_study_material_student_01"
    raw_notes = b"Lecture Notes on Newton's Laws: F = m*a, p = m*v, Impulse J = F*dt."
    
    res = await StudyMaterialService.process_and_save_study_material(
        student_id=student_id,
        filename="Physics_Lecture_Notes.txt",
        file_bytes=raw_notes,
        title="Newtonian Mechanics Notes",
        subject="Physics"
    )
    
    assert res["status"] == "success"
    assert res["title"] == "Newtonian Mechanics Notes"
    assert res["chunks_indexed"] >= 1
    
    # Retrieve
    stored = await StudyMaterialService.get_student_materials(student_id)
    assert len(stored) >= 1
    assert stored[0]["title"] == "Newtonian Mechanics Notes"

@pytest.mark.asyncio
async def test_profile_age_validation():
    from pydantic import ValidationError
    from app.models.schemas import StudentProfileUpdate, StudentProfile

    # Reject age 1000
    with pytest.raises(ValidationError):
        StudentProfileUpdate(age=1000)

    # Reject age < 10
    with pytest.raises(ValidationError):
        StudentProfileUpdate(age=5)

    # Accept valid student age
    valid = StudentProfileUpdate(name="Pratik", age=20, goal="AI/ML")
    assert valid.age == 20
    assert valid.name == "Pratik"

@pytest.mark.asyncio
async def test_course_unenroll_flow():
    from app.core.database import db_manager
    student_id = "test_unenroll_student_99"
    profile_col = db_manager.get_collection("student_profiles")
    await profile_col.update_one(
        {"student_id": student_id},
        {"$set": {"student_id": student_id, "enrolled_courses": ["Course Alpha", "Course Beta"]}},
        upsert=True
    )

    # Simulate unenroll
    prof = await profile_col.find_one({"student_id": student_id})
    enrolled = prof.get("enrolled_courses", [])
    updated = [c for c in enrolled if c.lower().strip() != "Course Alpha".lower().strip()]
    await profile_col.update_one({"student_id": student_id}, {"$set": {"enrolled_courses": updated}})

    prof_after = await profile_col.find_one({"student_id": student_id})
    assert "Course Alpha" not in prof_after["enrolled_courses"]
    assert "Course Beta" in prof_after["enrolled_courses"]

@pytest.mark.asyncio
async def test_guidance_generation():
    from app.routes.guidance_routes import generate_ai_guidance, GuidanceRequest
    fake_user = {"id": "test_guidance_user_42", "email": "test@mentor.ai"}
    req = GuidanceRequest(
        goal="AI/ML",
        klass="Degree",
        daily_hours=4.0,
        weak_areas=["Linear Algebra", "Backpropagation"],
        subjects=["Machine Learning", "Mathematics"]
    )
    res = await generate_ai_guidance(payload=req, user=fake_user)
    assert res["success"] is True
    g = res["guidance"]
    assert "executive_strategy" in g
    assert "weak_area_action_plan" in g
    assert len(g["weak_area_action_plan"]) >= 1
    assert "subject_time_allocation" in g
    assert len(g["subject_time_allocation"]) >= 1
