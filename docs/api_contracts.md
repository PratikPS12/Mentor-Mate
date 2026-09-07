# Mentor Mate — API Specifications & Contracts

Base URL: `http://localhost:8000/api/v1`

---

## 1. Authentication
* `POST /auth/register`: Register new student account.
  * Request: `{ name, email, password, klass, goal }`
  * Response: `{ access_token, token_type, user: { id, name, email, role, klass, goal } }`
* `POST /auth/login`: Authenticate existing user.
  * Request: `{ email, password }`
  * Response: `{ access_token, token_type, user: { id, name, email, role, klass, goal } }`
* `GET /auth/me`: Retrieve current authenticated profile.

---

## 2. Student Profile & Attendance
* `GET /student/profile`: Current student profile, goals, weak areas, and enrolled courses.
* `PUT /student/profile`: Update profile fields, study hours, or quick action preferences.
* `POST /student/attendance/mark-today`: Record today's study session; recalculates weekly streak.
* `GET /student/attendance`: Retrieve attendance history and weekly streak metrics.

---

## 3. Marksheet Document Intelligence
* `POST /marksheet/upload`: Upload PDF/JPG/PNG marksheet for OCR analysis.
  * Response: `{ document_id, status, extraction: { candidate_name, institution, subjects, overall_confidence, requires_verification } }`
* `POST /marksheet/verify`: Confirm extracted subject scores.
  * Updates baseline weak areas and initializes BKT concept mastery estimates.

---

## 4. Adaptive Assessment
* `POST /assessment/start?assessment_type=diagnostic`: Initialize adaptive test session.
  * Response: `{ session_id, status, progress, current_question }`
* `POST /assessment/{session_id}/answer`: Submit question answer.
  * Request: `{ question_id, selected_index, response_time_ms, hints_used }`
  * Response: `{ is_correct, explanation, diagnosis, prior_mastery, posterior_mastery, is_complete, current_score, next_question }`
* `GET /assessment/{session_id}/results`: Complete diagnostic results and concept mastery breakdown.

---

## 5. Adaptive Planner
* `POST /schedule/generate?daily_hours=3.0&days_to_exam=180`: Generate daily study plan with constraints.
* `POST /schedule/{plan_id}/task/{task_id}/toggle`: Toggle task completion state.

---

## 6. AI Mentor
* `POST /tutor/message`: Submit student query.
  * Request: `{ message, concept_id, session_id }`
  * Response: `{ role, content, pedagogical_state, concept_id, concept_name, practice_question, citations, timestamp }`
* `GET /tutor/conversations`: Retrieve conversation history.

---

## 7. Courses & Recommendations
* `GET /courses/catalog?track=CBSE`: Filterable course catalog.
* `GET /courses/recommended`: Evidence-driven course recommendations ranked by mastery gap and goals.
* `POST /courses/enroll`: Enroll in course.

---

## 8. Performance Analytics
* `GET /performance/summary`: Aggregated measured test scores (weekly, monthly, yearly), model estimates (BKT & retention), and Learning Twin synthesis.
