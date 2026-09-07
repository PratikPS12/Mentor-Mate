from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# --- Authentication & User ---
class UserRole:
    STUDENT = "student"
    PARENT = "parent"
    ADMIN = "admin"

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = UserRole.STUDENT
    klass: Optional[str] = "10"
    goal: Optional[str] = "JEE"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    name: str
    created_at: str

# --- Student Profile ---
class StudentProfile(BaseModel):
    student_id: str
    name: str
    email: str
    age: Optional[int] = Field(None, ge=10, le=100)
    klass: str = "10"
    board: str = "CBSE"
    goal: str = "JEE"
    school: Optional[str] = ""
    weak_areas: List[str] = []
    enrolled_courses: List[str] = []
    daily_available_hours: float = 3.0
    days_to_exam: int = 180
    quick_actions: List[str] = ["upload", "plan", "test", "mark", "up1", "up2", "up3"]
    dark_mode: bool = False
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class StudentProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=60)
    age: Optional[int] = Field(None, ge=10, le=100)
    klass: Optional[str] = None
    board: Optional[str] = None
    goal: Optional[str] = None
    school: Optional[str] = None
    weak_areas: Optional[List[str]] = None
    enrolled_courses: Optional[List[str]] = None
    daily_available_hours: Optional[float] = Field(None, ge=0.5, le=18.0)
    days_to_exam: Optional[int] = Field(None, ge=1, le=1500)
    quick_actions: Optional[List[str]] = None
    dark_mode: Optional[bool] = None

# --- Curriculum & Concepts ---
class ConceptModel(BaseModel):
    id: str
    subject: str
    chapter: str
    topic: str
    name: str
    prerequisites: List[str] = []
    description: str
    default_bkt: Dict[str, float]

class CurriculumModel(BaseModel):
    id: str
    board: str
    grade: str
    title: str
    subjects: List[str]

# --- Questions ---
class QuestionModel(BaseModel):
    id: str
    concept_id: str
    subject: str
    topic: str
    difficulty: float
    type: str
    question: str
    options: List[str]
    correct_index: int
    explanation: str
    misconception_distractors: Dict[str, Dict[str, str]]
    hints: List[str]
    source: str

# --- Assessment ---
class AssessmentSessionCreate(BaseModel):
    student_id: str
    assessment_type: str = "diagnostic"  # diagnostic, targeted, weekly
    subject: Optional[str] = None
    topic: Optional[str] = None

class AssessmentAnswerSubmit(BaseModel):
    question_id: str
    selected_index: int
    response_time_ms: int = 15000
    hints_used: int = 0

class AssessmentQuestionView(BaseModel):
    id: str
    concept_id: str
    subject: str
    topic: str
    question: str
    options: List[str]
    hints: List[str]

# --- Learning Events ---
class LearningEvent(BaseModel):
    id: str
    student_id: str
    session_id: str
    event_type: str  # "question_answered", "concept_reviewed", "marksheet_verified"
    concept_id: str
    question_id: Optional[str] = None
    correct: bool
    response_time_ms: int
    hints_used: int = 0
    prior_mastery: float
    posterior_mastery: float
    misconception_detected: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

# --- Mastery & Retention ---
class MasteryState(BaseModel):
    student_id: str
    concept_id: str
    mastery: float  # 0.0 - 1.0
    uncertainty: float  # variance or std dev
    evidence_count: int
    p_l0: float
    p_t: float
    p_s: float
    p_g: float
    last_evidence_at: str

class RetentionState(BaseModel):
    student_id: str
    concept_id: str
    retention_estimate: float  # R(t)
    memory_strength: float  # S (days)
    last_review: str
    next_review: str
    repetition_number: int

# --- Study Plan ---
class StudyPlanTask(BaseModel):
    id: str
    type: str  # "warmup", "core_concept", "practice_pyq", "spaced_revision"
    subject: str
    concept_id: Optional[str] = None
    title: str
    description: str
    duration_minutes: int
    completed: bool = False
    reason: str

class StudyPlan(BaseModel):
    id: str
    student_id: str
    target_exam: str
    daily_hours: float
    generated_at: str
    tasks: List[StudyPlanTask]
    completion_rate: float = 0.0

# --- Marksheet & Document Intelligence ---
class ExtractedSubjectMark(BaseModel):
    subject: str
    marks_obtained: float
    maximum_marks: float
    percentage: float
    grade: Optional[str] = None
    confidence: float
    bounding_box: Optional[List[int]] = None

class MarksheetVerificationPayload(BaseModel):
    document_id: str
    student_name: str
    institution: str
    exam_session: str
    subjects: List[ExtractedSubjectMark]

# --- Tutor ---
class TutorMessagePayload(BaseModel):
    message: str
    concept_id: Optional[str] = None
    session_id: Optional[str] = None

class TutorMessageResponse(BaseModel):
    role: str
    content: str
    pedagogical_state: str  # "diagnose", "explain", "check", "practice", "remediate"
    concept_id: Optional[str] = None
    concept_name: Optional[str] = None
    detected_gap: Optional[str] = None
    practice_question: Optional[Dict[str, Any]] = None
    citations: List[str] = []
    timestamp: str

# --- Recommendations ---
class RecommendationItem(BaseModel):
    id: str
    title: str
    track: str
    tag: str
    hours: int
    reason: str
    concept_id: Optional[str] = None
    fit_score: float
