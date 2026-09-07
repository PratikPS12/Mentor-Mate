import uuid
from typing import Dict, Any
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, Header
from app.core.database import db_manager
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.models.schemas import UserRegister, UserLogin, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

async def get_current_user(authorization: str = Header(None)) -> Dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token required")
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    users_col = db_manager.get_collection("users")
    user = await users_col.find_one({"id": payload["sub"]})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/register", response_model=TokenResponse)
async def register(payload: UserRegister):
    users_col = db_manager.get_collection("users")
    existing = await users_col.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc).isoformat()

    user_doc = {
        "id": user_id,
        "email": payload.email.lower(),
        "name": payload.name,
        "password_hash": hash_password(payload.password),
        "role": payload.role,
        "created_at": now,
        "updated_at": now
    }
    await users_col.insert_one(user_doc)

    # Initialize default student profile
    profile_col = db_manager.get_collection("student_profiles")
    profile_doc = {
        "student_id": user_id,
        "name": payload.name,
        "email": payload.email.lower(),
        "klass": payload.klass or "10",
        "goal": payload.goal or "JEE",
        "board": "CBSE",
        "school": "",
        "weak_areas": [],
        "enrolled_courses": [],
        "daily_available_hours": 3.0,
        "days_to_exam": 180,
        "quick_actions": ["upload", "plan", "test", "mark", "courses", "mentor", "performance"],
        "dark_mode": False,
        "created_at": now,
        "updated_at": now
    }
    await profile_col.insert_one(profile_doc)

    token = create_access_token({"sub": user_id, "email": payload.email.lower(), "role": payload.role})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "name": payload.name,
            "email": payload.email.lower(),
            "role": payload.role,
            "klass": payload.klass,
            "goal": payload.goal
        }
    }

@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin):
    users_col = db_manager.get_collection("users")
    user = await users_col.find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user["id"], "email": user["email"], "role": user.get("role", "student")})

    profile_col = db_manager.get_collection("student_profiles")
    prof = await profile_col.find_one({"student_id": user["id"]})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user.get("role", "student"),
            "klass": prof.get("klass", "10") if prof else "10",
            "goal": prof.get("goal", "JEE") if prof else "JEE"
        }
    }

@router.get("/me")
async def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    profile_col = db_manager.get_collection("student_profiles")
    prof = await profile_col.find_one({"student_id": user["id"]})
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "role": user.get("role", "student"),
        "profile": prof
    }
