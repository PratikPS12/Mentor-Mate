# Mentor Mate — System Architecture

## 1. High-Level Architecture Overview

Mentor Mate is an evidence-driven adaptive AI learning platform. Rather than a static dashboard or generic chatbot, every student interaction flows through a closed-loop adaptive cognitive engine:

```
[ Student Evidence ]
         ↓
[ Learning Events Stream (Immutable) ]
         ↓
[ Student Model: BKT + Ebbinghaus Retention + Misconception Diagnostic ]
         ↓
[ Knowledge Graph: Curricula, Concepts & Prerequisites ]
         ↓
[ Adaptive Planner & Multi-Objective Recommendations ]
         ↓
[ Next Best Learning Action ]
         ↓
[ Grounded Pedagogical AI Tutor / Adaptive Diagnostic Assessment ]
         ↓
[ Dynamic State Recalibration ]
```

---

## 2. Core Subsystems

### 2.1 Student Model & Bayesian Knowledge Tracing (BKT)
- **Formulation:**
  - $P(L_0)$: Initial mastery probability.
  - $P(T)$: Learning transition probability after practice.
  - $P(S)$: Slip probability ($P(\text{Incorrect} \mid \text{Mastered})$).
  - $P(G)$: Guess probability ($P(\text{Correct} \mid \neg\text{Mastered})$).
- **Posterior Update:**
  $$P(L_t \mid X) = \frac{P(X \mid L_t) P(L_t)}{P(X \mid L_t) P(L_t) + P(X \mid \neg L_t)(1 - P(L_t))}$$
- **Transition Update:**
  $$P(L_{t+1}) = P(L_t \mid X) + (1 - P(L_t \mid X)) \cdot P(T)$$
- **Uncertainty Quantification:** Bernoulli variance $\sigma^2 = P(L)(1 - P(L))$.

### 2.2 Retention Engine (Ebbinghaus Spaced Repetition)
- Memory retention follows exponential decay:
  $$R(t) = \exp\left(-\frac{t}{S}\right)$$
  where $t$ is elapsed days and $S$ is memory stability in days.
- When $R(t) \le 0.75$, the Adaptive Planner automatically schedules a spaced consolidation block.
- Upon successful retrieval, memory stability expands: $S_{new} = S_{old} \times (1.8 + 0.25 \times n)$.

### 2.3 Document Intelligence & Marksheet OCR
- Accepts PDF / PNG / JPG / TXT marksheets.
- Layout parsing detects candidate metadata, session, and tabular scores.
- Field-level confidence scores are calculated; any field $< 90\%$ triggers an interactive verification review.
- Verified scores calibrate baseline concept masteries across PCM/Biology subject areas.

### 2.4 Pedagogical AI Tutor
- Governed by a deterministic state machine:
  $$\text{QUESTION} \rightarrow \text{DIAGNOSE} \rightarrow \text{EXPLAIN} \rightarrow \text{CHECK} \rightarrow \text{PRACTICE} \rightarrow \text{REMEDIATE}$$
- Integrates SymPy deterministic equation evaluation for mathematical precision.
- Grounded in official syllabus guidelines (NCERT / CBSE / JEE / NEET).

---

## 3. UI/UX Design System: Bright Educational Theme
Preserving the exact structural layout, component hierarchy, card proportions, and tab navigation from `index(6).html`, updated into a bright, clean, premium educational palette:
- Canvas: Warm off-white (`#f8fafc` / `#f1f5f9`)
- Panels: Crisp white (`#ffffff`) with subtle slate borders (`#e2e8f0`) and elevation shadows
- Accents: Primary cyan/blue (`#0284c7`), complementary indigo (`#4f46e5`), positive green (`#10b981`)
- Typography: Deep slate/navy (`#0f172a` / `#1e293b` / `#64748b`)
