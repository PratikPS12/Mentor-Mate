import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

@pytest.mark.asyncio
async def test_auth_and_profile_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register new student
        reg_payload = {
            "name": "Arjun Patel",
            "email": "arjun@example.com",
            "password": "SecurePassword123!",
            "klass": "11",
            "goal": "JEE"
        }
        res = await client.post("/api/v1/auth/register", json=reg_payload)
        assert res.status_code in [200, 400]  # If already registered, returns 400

        # Login
        login_payload = {
            "email": "arjun@example.com",
            "password": "SecurePassword123!"
        }
        login_res = await client.post("/api/v1/auth/login", json=login_payload)
        assert login_res.status_code == 200
        token_data = login_res.json()
        token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get Profile
        prof_res = await client.get("/api/v1/student/profile", headers=headers)
        assert prof_res.status_code == 200
        assert prof_res.json()["name"] == "Arjun Patel"

        # Update Profile
        update_res = await client.put(
            "/api/v1/student/profile",
            headers=headers,
            json={"weak_areas": ["Algebra", "Physics"], "daily_available_hours": 4.0}
        )
        assert update_res.status_code == 200
        assert update_res.json()["profile"]["daily_available_hours"] == 4.0

        # Generate Adaptive Study Plan
        plan_res = await client.post("/api/v1/schedule/generate?daily_hours=4.0", headers=headers)
        assert plan_res.status_code == 200
        plan = plan_res.json()
        assert len(plan["tasks"]) >= 3

        # Start Adaptive Diagnostic Assessment
        test_res = await client.post("/api/v1/assessment/start?assessment_type=diagnostic", headers=headers)
        assert test_res.status_code == 200
        test_session = test_res.json()
        assert "session_id" in test_session
        assert "current_question" in test_session
        first_q = test_session["current_question"]

        # Submit answer
        ans_res = await client.post(
            f"/api/v1/assessment/{test_session['session_id']}/answer",
            headers=headers,
            json={"question_id": first_q["id"], "selected_index": 1, "response_time_ms": 14000, "hints_used": 0}
        )
        assert ans_res.status_code == 200
        ans_data = ans_res.json()
        assert "is_correct" in ans_data
        assert "posterior_mastery" in ans_data
