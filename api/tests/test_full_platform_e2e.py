import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_complete_17_step_platform_acceptance_journey():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Step 1: Create an account
        reg_payload = {
            "name": "Priya Sharma",
            "email": "priya.student@example.com",
            "password": "SecureStudentPass2026!",
            "klass": "10",
            "goal": "JEE"
        }
        reg_res = await client.post("/api/v1/auth/register", json=reg_payload)
        assert reg_res.status_code in [200, 400]

        # Step 2: Login and get token
        login_res = await client.post("/api/v1/auth/login", json={
            "email": "priya.student@example.com",
            "password": "SecureStudentPass2026!"
        })
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Step 3: Complete & verify profile with academic context
        prof_res = await client.put("/api/v1/student/profile", headers=headers, json={
            "school": "St. Xavier's High School",
            "board": "CBSE",
            "goal": "JEE",
            "daily_available_hours": 3.5,
            "days_to_exam": 160,
            "weak_areas": ["Algebra", "Physics"]
        })
        assert prof_res.status_code == 200
        assert prof_res.json()["profile"]["school"] == "St. Xavier's High School"

        # Step 4: Upload a marksheet
        sample_file_content = b"Mathematics: 82\nPhysics: 74\nChemistry: 68\nEnglish: 86\n"
        files = {"file": ("marksheet.txt", sample_file_content, "text/plain")}
        upload_res = await client.post("/api/v1/marksheet/upload", headers=headers, files=files)
        assert upload_res.status_code == 200
        upload_data = upload_res.json()
        assert "document_id" in upload_data
        doc_id = upload_data["document_id"]
        extraction = upload_data["extraction"]

        # Step 5: Verify extracted marksheet data & calibrate student model baseline
        verify_payload = {
            "document_id": doc_id,
            "student_name": extraction["candidate_name"],
            "institution": extraction["institution"],
            "exam_session": extraction["exam_session"],
            "subjects": extraction["subjects"]
        }
        verify_res = await client.post("/api/v1/marksheet/verify", headers=headers, json=verify_payload)
        assert verify_res.status_code == 200
        assert verify_res.json()["success"] is True

        # Step 6: Receive an evidence-based academic state & recommendations
        rec_res = await client.get("/api/v1/courses/recommended", headers=headers)
        assert rec_res.status_code == 200
        recommendations = rec_res.json()
        assert len(recommendations) > 0
        assert "reason" in recommendations[0]

        # Step 7: Complete diagnostic assessment session
        test_start = await client.post("/api/v1/assessment/start?assessment_type=diagnostic", headers=headers)
        assert test_start.status_code == 200
        session_id = test_start.json()["session_id"]
        current_q = test_start.json()["current_question"]

        # Step 8: Submit response and receive concept-level BKT mastery update
        ans_res = await client.post(f"/api/v1/assessment/{session_id}/answer", headers=headers, json={
            "question_id": current_q["id"],
            "selected_index": 1,
            "response_time_ms": 15000,
            "hints_used": 1
        })
        assert ans_res.status_code == 200
        ans_data = ans_res.json()
        assert "posterior_mastery" in ans_data

        # Step 9: Receive a personalized adaptive study plan
        plan_res = await client.post("/api/v1/schedule/generate?daily_hours=3.5&days_to_exam=160", headers=headers)
        assert plan_res.status_code == 200
        plan = plan_res.json()
        assert len(plan["tasks"]) >= 3

        # Step 10 & 11: Ask AI mentor a question & receive context-aware pedagogical response
        tutor_res = await client.post("/api/v1/tutor/message", headers=headers, json={
            "message": "How can I improve in Roots of Quadratic Equations?"
        })
        assert tutor_res.status_code == 200
        tutor_reply = tutor_res.json()
        assert tutor_reply["pedagogical_state"] in ["EXPLAIN", "DIAGNOSE", "CHECK"]
        assert len(tutor_reply["citations"]) > 0

        # Step 12 & 13: Mathematical query handled via deterministic SymPy solver
        math_res = await client.post("/api/v1/tutor/message", headers=headers, json={
            "message": "solve 2x + 6 = 18"
        })
        assert math_res.status_code == 200
        assert "SymPy" in math_res.json()["content"] and "x = 6" in math_res.json()["content"]

        # Step 14 & 15: Mark daily attendance & check streak
        att_res = await client.post("/api/v1/student/attendance/mark-today", headers=headers)
        assert att_res.status_code == 200
        assert att_res.json()["streak_days"] >= 1

        # Step 16: Verify genuine performance analytics & Learning Twin
        perf_res = await client.get("/api/v1/performance/summary", headers=headers)
        assert perf_res.status_code == 200
        perf_data = perf_res.json()
        assert "learning_twin" in perf_data
        assert perf_data["learning_twin"]["status"] is not None
        assert len(perf_data["charts"]["labels_day"]) == 7

        # Step 17: Return later and continue from persisted state
        me_res = await client.get("/api/v1/auth/me", headers=headers)
        assert me_res.status_code == 200
        assert me_res.json()["email"] == "priya.student@example.com"
        assert me_res.json()["profile"]["school"] == "St. Xavier's High School"

import uuid

@pytest.mark.asyncio
async def test_multi_student_isolation_and_rag_grounding():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        alpha_email = f"alpha_{uuid.uuid4().hex[:6]}@mentor.internal"
        beta_email = f"beta_{uuid.uuid4().hex[:6]}@mentor.internal"

        # Register Student Alpha
        await client.post("/api/v1/auth/register", json={
            "name": "Alpha Student",
            "email": alpha_email,
            "password": "AlphaPassword123!",
            "klass": "11",
            "goal": "JEE"
        })
        alpha_login = await client.post("/api/v1/auth/login", json={
            "email": alpha_email,
            "password": "AlphaPassword123!"
        })
        alpha_token = alpha_login.json()["access_token"]
        alpha_hdr = {"Authorization": f"Bearer {alpha_token}"}

        # Register Student Beta
        await client.post("/api/v1/auth/register", json={
            "name": "Beta Student",
            "email": beta_email,
            "password": "BetaPassword123!",
            "klass": "12",
            "goal": "NEET"
        })
        beta_login = await client.post("/api/v1/auth/login", json={
            "email": beta_email,
            "password": "BetaPassword123!"
        })
        beta_token = beta_login.json()["access_token"]
        beta_hdr = {"Authorization": f"Bearer {beta_token}"}

        # 1. Student Alpha uploads private study notes into RAG
        alpha_notes_content = b"Markovnikov Rule in Organic Addition: When HX adds to an unsymmetrical alkene, hydrogen attaches to carbon with more hydrogens.\n"
        notes_file = {"file": ("markovnikov_notes.txt", alpha_notes_content, "text/plain")}
        upload_notes_res = await client.post(
            "/api/v1/marksheet/notes/upload?title=Alpha Markovnikov Synthesis&subject=Chemistry",
            headers=alpha_hdr,
            files=notes_file
        )
        assert upload_notes_res.status_code == 200
        assert upload_notes_res.json()["chunks_indexed"] >= 1

        # 2. Student Alpha sends a tutor message
        alpha_msg = await client.post("/api/v1/tutor/message", headers=alpha_hdr, json={
            "message": "Can you explain Markovnikov Rule using my notes?"
        })
        assert alpha_msg.status_code == 200

        # 3. VERIFY ISOLATION: Student Beta CANNOT see Alpha's uploaded notes
        beta_notes_res = await client.get("/api/v1/marksheet/notes", headers=beta_hdr)
        assert beta_notes_res.status_code == 200
        beta_materials = beta_notes_res.json()["materials"]
        assert len(beta_materials) == 0, "Student Beta should have 0 notes uploaded"

        # 4. VERIFY ISOLATION: Student Beta CANNOT see Alpha's conversation history
        beta_history_res = await client.get("/api/v1/tutor/history", headers=beta_hdr)
        assert beta_history_res.status_code == 200
        beta_convs = beta_history_res.json()
        assert len(beta_convs) == 0, "Student Beta must have empty conversation history"

        # 5. Student Alpha verifies their notes are present for them
        alpha_notes_res = await client.get("/api/v1/marksheet/notes", headers=alpha_hdr)
        assert alpha_notes_res.status_code == 200
        assert len(alpha_notes_res.json()["materials"]) == 1
        assert alpha_notes_res.json()["materials"][0]["title"] == "Alpha Markovnikov Synthesis"

