import uuid
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
import sympy
from app.core.database import db_manager
from app.services.ai.registry import AIProviderRegistry
from app.services.ai.task_router import AITaskRouter, AITaskType
from app.services.rag.rag_service import RAGService
from app.services.curriculum.curriculum_graph import CurriculumKnowledgeGraph
from app.services.ai.math_formatter import clean_latex_to_plain_text
from app.services.ai.math_evaluator import DynamicProblemSolver

class PedagogicalTutorService:
    """
    Socratic AI Tutor Orchestrator.
    Controls the educational state machine:
    QUESTION -> DIAGNOSE -> EXPLAIN -> CHECK -> PRACTICE -> EVALUATE -> REMEDIATE -> RETEST
    Enriched with real student mastery state, RAG document chunks, SymPy verification,
    and AgentRouter AI provider abstraction.
    Guarantees clean plain-text formula rendering with standard Unicode symbols (zero LaTeX).
    """

    @classmethod
    async def process_student_message(
        cls,
        student_id: str,
        message: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        conv_col = db_manager.get_collection("conversations")
        mastery_col = db_manager.get_collection("mastery_states")
        profile_col = db_manager.get_collection("student_profiles")

        profile = await profile_col.find_one({"student_id": student_id}) if student_id else None
        student_name = profile.get("name", "Student") if profile else "Student"
        goal = profile.get("goal", "CBSE") if profile else "CBSE"
        student_class = str(profile.get("klass") or "10") if profile else "10"

        # 1. Identify relevant concept and subject from knowledge graph
        concept_match, detected_subject = cls._identify_concept(message)

        # 2. Fetch student's real BKT mastery for this concept
        concept_mastery = 0.45
        if concept_match:
            m_rec = await mastery_col.find_one({"student_id": student_id, "concept_id": concept_match["id"]})
            if m_rec:
                concept_mastery = m_rec.get("mastery", 0.45)

        # 3. Retrieve grounded RAG document context (uploaded notes / syllabus)
        rag_chunks = await RAGService.retrieve_relevant_context(
            student_id=student_id,
            query=message,
            subject_filter=detected_subject,
            max_chunks=2
        )
        grounding_notes = "\n".join([f"- {c['title']}: {c['content'][:250]}..." for c in rag_chunks]) if rag_chunks else ""

        # 4. Check for mathematical/physics problems and solve deterministically with SymPy
        math_eval_result = DynamicProblemSolver.solve(message)
        math_eval_text = math_eval_result["text"] if math_eval_result else None

        # 5. Build Warm Socratic Teacher Prompt
        system_prompt = (
            f"You are Mentor Mate, a warm, encouraging, conversational, and brilliant personal teacher. "
            f"You are tutoring {student_name}, preparing for {goal} at Class {student_class} level. "
            f"Active Concept: {concept_match['name'] if concept_match else detected_subject} "
            f"(Student's estimated mastery: {int(concept_mastery * 100)}%).\n\n"
            f"TEACHING GUIDELINES:\n"
            f"1. Tone: Warm, cheerful, articulate, and patient—like a favorite school or college teacher who loves explaining science and math.\n"
            f"2. Clarity: Thoroughly explain principles with clear definitions, intuitive real-world analogies, and step-by-step mechanisms.\n"
            f"3. Formulas & Units: Provide exact governing equations, defining every variable, constant, and standard unit clearly.\n"
            f"4. Engagement: Always end with an encouraging Socratic check-in question to invite the student into the dialogue.\n"
            f"5. Math/Derivations: For numerical or algebraic problems, show full step-by-step calculations: {math_eval_text or 'None'}.\n"
            f"6. CRITICAL - NO LATEX FORMATTING: Under NO circumstances use LaTeX, TeX, dollar signs ($ or $$), or backslash commands (like \\frac, \\vec, \\sqrt, \\text). "
            f"Always write all mathematical and scientific formulas, symbols, and values using standard plain text and clean Unicode (for example: x², ³, √x, ±, ·, ×, ÷, →, θ, λ, Δ, π, α, β, subscripts like H₂O, v₁, and clean fractions like (a/b) or (Δp / Δt)). "
            f"Explicitly define every variable and constant, and give exact numerical values with proper standard units (e.g. m/s, m/s², N, J, W, kg, Ω).\n"
        )
        if grounding_notes:
            system_prompt += f"\nGrounded Curriculum Notes:\n{grounding_notes}\n"

        # 6. Fetch previous conversation turns for this student for conversational continuity
        history_turns = await conv_col.find(
            {"student_id": student_id, "session_id": session_id or "default_session"}
        ) if student_id else []
        history_messages = []
        for prev in history_turns[-4:]:
            if prev.get("user_message"):
                history_messages.append({"role": "user", "content": prev["user_message"]})
            if prev.get("tutor_reply"):
                history_messages.append({"role": "assistant", "content": prev["tutor_reply"]})

        messages = [{"role": "system", "content": system_prompt}] + history_messages + [{"role": "user", "content": message}]

        # 7. Execute through centralized AIProviderRegistry (AgentRouter with LocalFallback)
        provider = AIProviderRegistry.get_provider()
        model = AITaskRouter.get_model_for_task(AITaskType.REASONING)

        ai_response = await provider.chat_completion(
            messages=messages,
            model=model,
            temperature=0.6,
            max_tokens=800
        )

        raw_reply = ai_response.get("content", "")
        # Guarantee clean plain-text formatting (no LaTeX)
        reply = clean_latex_to_plain_text(raw_reply)

        # 8. Determine pedagogical state (canonical EXPLAIN/DIAGNOSE/CHECK + friendly label)
        pedagogical_state = "EXPLAIN"
        pedagogical_label = "Conceptual Lesson 💡"
        q_lower = message.lower()
        if math_eval_result or any(w in q_lower for w in ["solve", "calculate", "find", "evaluate", "differentiate", "integrate", "="]):
            pedagogical_state = "EXPLAIN"
            pedagogical_label = "Worked Solution ✍️"
        elif any(w in q_lower for w in ["test", "quiz", "practice", "question"]):
            pedagogical_state = "CHECK"
            pedagogical_label = "Practice Drill 🎯"
        elif any(w in q_lower for w in ["diagnose", "weak", "confused", "stuck", "don't understand", "dont understand", "help me identify"]):
            pedagogical_state = "DIAGNOSE"
            pedagogical_label = "Diagnostic Check 🔍"

        citations = [f"NCERT / {goal} Curriculum Standard", "Mentor Mate Knowledge Graph"]
        if rag_chunks:
            citations.extend([f"Uploaded Material: {c['title']}" for c in rag_chunks])

        msg_record = {
            "id": f"msg_{uuid.uuid4().hex[:10]}",
            "student_id": student_id,
            "session_id": session_id or "default_session",
            "user_message": message,
            "tutor_reply": reply,
            "pedagogical_state": pedagogical_state,
            "pedagogical_label": pedagogical_label,
            "concept_id": concept_match["id"] if concept_match else None,
            "ai_model": ai_response.get("model", "default"),
            "provider": ai_response.get("provider", "agentrouter"),
            "citations": citations,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        await conv_col.insert_one(msg_record)

        return {
            "role": "Mentor",
            "content": reply,
            "pedagogical_state": pedagogical_state,
            "pedagogical_label": pedagogical_label,
            "concept_id": concept_match["id"] if concept_match else None,
            "concept_name": concept_match["name"] if concept_match else None,
            "citations": citations,
            "provider": ai_response.get("provider", "agentrouter"),
            "timestamp": msg_record["created_at"]
        }


    @classmethod
    def _identify_concept(cls, query: str) -> Tuple[Optional[Dict[str, Any]], str]:
        q = query.lower()
        for cid, cdata in CurriculumKnowledgeGraph.CONCEPTS_REGISTRY.items():
            cname = cdata["name"].lower()
            subject = cdata["subject"]
            words = [w for w in cname.split() if len(w) > 4]
            if any(w in q for w in words):
                return cdata, subject

        if any(w in q for w in ["matrix", "matrices", "determinant", "cramer", "eigen"]):
            return CurriculumKnowledgeGraph.get_concept("math_matrices_determinants"), "Mathematics"
        if any(w in q for w in ["math", "calculus", "derivative", "equation", "root", "algebra"]):
            return CurriculumKnowledgeGraph.get_concept("concept_math_quad_roots"), "Mathematics"
        if any(w in q for w in ["physics", "force", "gravity", "motion", "newton"]):
            return CurriculumKnowledgeGraph.get_concept("concept_phys_force_units"), "Physics"
        if any(w in q for w in ["chem", "organic", "iupac", "reaction", "bond"]):
            return CurriculumKnowledgeGraph.get_concept("concept_chem_iupac"), "Chemistry"
        if any(w in q for w in ["bio", "cell", "dna", "genetics"]):
            return CurriculumKnowledgeGraph.get_concept("concept_bio_cell"), "Biology"

        return None, "General"

    @staticmethod
    def _evaluate_math_expression(query: str) -> Optional[str]:
        try:
            eq_match = re.search(r"(\d*x\s*[\+\-]\s*\d+\s*=\s*\d+)", query)
            if eq_match:
                eq_str = eq_match.group(1)
                lhs, rhs = eq_str.split("=")
                x = sympy.Symbol("x")
                p_lhs = sympy.sympify(lhs.replace("x", "*x") if "x" in lhs and not lhs.strip().startswith("x") and not "*" in lhs else lhs)
                p_rhs = sympy.sympify(rhs)
                solution = sympy.solve(sympy.Eq(p_lhs, p_rhs), x)
                return f"SymPy Verified: For '{eq_str.strip()}', x = {solution[0]}"
        except Exception:
            return None
        return None
