# Mentor Mate — Evidence-Driven Adaptive AI Learning Platform

<div align="center">

![Mentor Mate Banner](https://img.shields.io/badge/Mentor_Mate-Adaptive_AI_Tutor-4f46e5?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688?style=flat-square&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-16.3.4_(Turbopack)-black?style=flat-square&logo=next.js&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.14-3776ab?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-33%20Passed-10b981?style=flat-square)

**An evidence-driven, mathematical adaptive learning engine and Socratic AI mentor for competitive exams (JEE, NEET, Boards, and Computer Science).**

[Features](#-key-features) • [Architecture](#-system-architecture) • [Getting Started](#-getting-started) • [Adaptive Planner](#-adaptive-study-planner) • [Testing](#-verification--testing)

</div>

---

## 🌟 Key Features

- **🧠 Bayesian Knowledge Tracing (BKT)**: Dynamically updates fine-grained mastery probabilities $P(L_t)$ after every student observation using Bayesian slip/guess parameters.
- **🎯 Item Response Theory (IRT & CAT)**: Computerized Adaptive Testing estimating latent student ability $\theta$ via Maximum A Posteriori (MAP) and selecting items maximizing Fisher Information.
- **📉 Ebbinghaus Memory Decay & FSRS**: Tracks memory strength and schedules spaced repetition drills the moment predicted retention drops below 75%.
- **🕸️ Prerequisite Knowledge Graph (DAG)**: Diagnoses root-cause misconceptions by traversing foundational dependencies across Math, Physics, Chemistry, and Computer Science.
- **📅 Adaptive Constraint-Based Daily Planner**:
  - Dynamically synthesizes personalized daily study blocks based on student weaknesses, available daily hours, and days remaining to exam.
  - Multi-subject balancing (e.g., *Data Structures & Algorithms*, *Linear Algebra*, *Python*).
  - Built-in live **Pomodoro Focus Timer** for active study sessions.
  - One-click **Calendar Export (.ICS)** compatible with Google Calendar, Apple Calendar, and Outlook.
  - Markdown itinerary export for Notion and Obsidian.
- **💬 Socratic AI Tutor & Deterministic Math Evaluator**: SymPy symbolic derivation solver combined with a pedagogical reasoning engine providing scaffolded hints without hallucinating formulas.
- **📑 Multi-Source Learning Twin**: Ingests uploaded marksheets, OCR exam papers, diagnostic tests, and flashcard recall to maintain an unified student evidence profile.

---

## 🏗️ System Architecture

```text
                     MENTOR MATE LEARNING LOOP

                          │
                          ▼
                  STUDENT PROFILE
                          │
                          ▼
                   LEARNING EVIDENCE
                          │
           ┌──────────────┼──────────────┐
           ▼              ▼              ▼
      ASSESSMENTS       DOCUMENTS      ACTIVITY
           │              │              │
           └──────────────┼──────────────┘
                          ▼
                   STUDENT MODEL
                          │
           ┌──────────────┼──────────────┐
           ▼              ▼              ▼
      BKT MASTERY     IRT ABILITY   FSRS RETENTION
           │              │              │
           └──────────────┼──────────────┘
                          ▼
                 PERSONALIZED ENGINE
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
    AI MENTOR         STUDY PLAN        RESOURCES
   (Socratic)        (Constraint)      (Ranked Gap)
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+** (Tested on Python 3.14)
- **Node.js 18+** (Tested on Node.js v24)
- **npm** or **pnpm**

---

### 1. Clone the Repository
```bash
git clone https://github.com/PratikPS12/Mentor-Mate.git
cd Mentor-Mate
```

---

### 2. Backend Setup (FastAPI)

```bash
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # On Windows
# source .venv/bin/activate    # On Linux/macOS

# Install dependencies
pip install -r api/requirements.txt

# Configure environment variables
cp .env.example .env

# Run FastAPI backend
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- **API Base URL**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

---

### 3. Frontend Setup (Next.js 16)

In a new terminal:

```bash
cd apps/web

# Install dependencies
npm install

# Start Next.js with Turbopack
npm run dev
```

- **Web Dashboard**: `http://localhost:3000`

---

## 🐳 Docker Deployment (Optional)

You can launch the entire stack (Next.js frontend, FastAPI backend, MongoDB 7.0) via Docker Compose:

```bash
docker compose up --build
```

---

## 📅 Adaptive Study Planner

The upgraded **Schedule Tab** features:
1. **Curriculum Presets**: 1-click loading for `CS & AI/ML`, `JEE (PCM)`, `NEET (PCB)`, and `Class 12 Boards`.
2. **Timeline Cards**: Time-stamped slots (e.g. `09:00 AM - 09:15 AM`, `09:20 AM - 10:35 AM`) with category color-coding (`⚡ Warm-up`, `🧠 Deep Dive`, `✍️ Applied Drill`, `🔄 Spaced Recall`).
3. **Pomodoro Focus Timer**: Click **Focus** on any card to launch an interactive countdown timer with Play/Pause, Reset, +5m, and automatic task completion logging.
4. **Calendar Export (.ics)**: Download study blocks to sync with Google Calendar or Apple Calendar.
5. **Subject Allocation Graph**: Visual distribution of daily study hours across subjects.

---

## 🧪 Verification & Testing

Mentor Mate comes with a comprehensive test suite covering BKT parameter updates, IRT MAP estimation, FSRS memory decay, syllabus diagnostics, and full end-to-end user workflows.

Run all tests using pytest:

```bash
pytest
```

```text
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\...\Mentor Mate
configfile: pytest.ini
collected 33 items

api\tests\test_ai_assessment_flow.py .                                   [  3%]
api\tests\test_ai_provider_and_irt.py ........                           [ 27%]
api\tests\test_auth_and_api.py ..                                        [ 33%]
api\tests\test_bkt_and_retention.py .....                                [ 48%]
api\tests\test_full_platform_e2e.py ..                                   [ 54%]
api\tests\test_study_material_and_custom_goals.py ........               [ 78%]
api\tests\test_syllabus_and_weakness_evaluation.py .......               [100%]

============================= 33 passed in 13.71s =============================
```

---

## 👥 Author

- **Pratik Sakhare** ([@PratikPS12](https://github.com/PratikPS12))
- Email: [priteshsakhare5@gmail.com](mailto:priteshsakhare5@gmail.com)

---

## 📜 License

This project is licensed under the MIT License.
