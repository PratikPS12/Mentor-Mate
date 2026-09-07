# Mentor Mate — System Architecture Document

## 1. System Overview

Mentor Mate is an evidence-driven adaptive AI learning platform. The platform repudiates hardcoded mocks, fake percentages, and static question sequences. Every recommendation, study plan, tutor interaction, and test is dynamically derived from real student evidence.

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
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ▼
                   STUDENT ACTION
                         │
                         ▼
                    PERFORMANCE
                         │
                         ▼
                  MODEL UPDATE
                         │
                         └───────────────→ NEXT ACTION
```

---

## 2. Multi-Tier AI Provider Abstraction

The application is decoupled from any specific AI provider via the `AIProvider` interface:

```text
AIProvider (Abstract Interface)
    ▲
    ├── AgentRouterProvider (OpenAI-compatible /v1 proxy for AgentRouter)
    └── LocalFallbackProvider (High-precision offline deterministic & Socratic fallback)
```

### Model Task Router
- **Reasoning Tier (`AI_MODEL_REASONING`)**: Socratic tutoring, deep misconception diagnosis, multi-step derivation scaffolding.
- **Primary Tier (`AI_MODEL_PRIMARY`)**: Standard conceptual instruction, study plan reasoning.
- **Fast Tier (`AI_MODEL_FAST`)**: Intent classification, metadata extraction, lightweight tagging.
- **Vision Tier (`AI_MODEL_VISION`)**: Complex marksheet layout fallback and diagram analysis.
- **Deterministic Math & Rules**: SymPy symbolic solving, BKT parameter updates, IRT MAP estimation, and Ebbinghaus retention decay are executed in deterministic Python code—**never** left to LLM hallucination.

---

## 3. Mathematical & Machine Learning Formulations

### A. Bayesian Knowledge Tracing (BKT)
For each fine-grained concept component, student mastery $P(L_t)$ is updated after each question observation:
$$P(L_t \mid \text{obs}=1) = \frac{P(L_{t-1}) \cdot (1 - P(S))}{P(L_{t-1}) \cdot (1 - P(S)) + (1 - P(L_{t-1})) \cdot P(G)}$$
$$P(L_{t+1}) = P(L_t \mid \text{obs}) + (1 - P(L_t \mid \text{obs})) \cdot P(T)$$
- $P(S) = 0.10$ (Slip probability)
- $P(G) = 0.20$ (Guess probability)
- $P(T) = 0.20$ (Learning transition probability)

### B. Item Response Theory (IRT) & Computerized Adaptive Testing (CAT)
Student latent ability $\theta$ is estimated via Maximum A Posteriori (MAP) with a Gaussian $N(0, 1)$ prior:
$$P(Y_i = 1 \mid \theta) = \frac{1}{1 + e^{-a_i(\theta - b_i)}}$$
The next item $i^*$ is chosen from candidate curriculum questions to maximize Fisher Information at current estimated ability:
$$i^* = \arg\max_{i} \left[ a_i^2 P_i(\hat{\theta})(1 - P_i(\hat{\theta})) \cdot \left(1 + (1 - \text{Mastery}_{BKT})\right) \right]$$

### C. Ebbinghaus Forgetting & Spaced Repetition (FSRS)
Memory decay is predicted dynamically:
$$R(t) = e^{-\frac{t}{S}}$$
where $S$ is memory stability in days. When retention drops below $0.75$, the Adaptive Planner automatically schedules a spaced repetition task.

---

## 4. Prerequisite Knowledge Graph (DAG)
The platform models foundational-to-advanced prerequisites across Mathematics, Physics, Chemistry, and Biology. When a student demonstrates a persistent deficit in an advanced concept, the graph traverses backwards to identify foundational gaps (e.g. diagnosing that an error in Rotational Dynamics stems from a deficit in Vector Resolution).

---

## 5. Security & Privacy Non-Negotiables
1. **Zero Secret Leaks**: `AGENTROUTER_API_KEY` and all credentials reside strictly on the server-side (`.env` ignored in `.gitignore`).
2. **Context Isolation**: Students only access their own private records and authenticated learning events.
3. **Prompt Injection Defense**: Student uploads and user queries are treated as data parameters, never instruction overrides.
