import re
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.core.database import db_manager

class RAGService:
    """
    Retrieval Augmented Generation (RAG) Service for Mentor Mate.
    Indexes educational textbook chunks, syllabus guides, and student-uploaded study materials.
    Enriches Socratic AI Tutor context with grounded citations.
    """

    @classmethod
    async def index_document_chunks(
        cls,
        student_id: str,
        document_id: str,
        title: str,
        text_content: str,
        subject: str = "General",
        chapter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Chunks text into manageable semantic segments (approx 200-300 words) with metadata.
        """
        chunks_col = db_manager.get_collection("rag_chunks")
        paragraphs = [p.strip() for p in text_content.split("\n\n") if len(p.strip()) > 30]

        created_chunks = []
        for i, para in enumerate(paragraphs):
            chunk_id = f"chunk_{uuid.uuid4().hex[:12]}"
            # Extract basic formulas or key terms
            formulas = re.findall(r"([A-Za-z0-9_\^]+(?:\s*[=+\-*/]\s*[A-Za-z0-9_\^]+)+)", para)
            
            chunk_doc = {
                "id": chunk_id,
                "student_id": student_id,
                "document_id": document_id,
                "title": title,
                "chunk_index": i,
                "subject": subject,
                "chapter": chapter or "Uploaded Notes",
                "content": para,
                "formulas": formulas[:5],
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            await chunks_col.insert_one(chunk_doc)
            created_chunks.append(chunk_doc)

        return created_chunks

    @classmethod
    async def retrieve_relevant_context(
        cls,
        student_id: str,
        query: str,
        subject_filter: Optional[str] = None,
        max_chunks: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Hybrid retrieval combining keyword matching, subject filtering, and term frequency.
        """
        chunks_col = db_manager.get_collection("rag_chunks")
        query_terms = set(re.findall(r"\b\w{3,}\b", query.lower()))

        # Retrieve all student and curriculum chunks
        all_chunks = await chunks_col.find()
        candidates = [
            c for c in all_chunks
            if (c.get("student_id") in [student_id, "system_curriculum"])
            and (not subject_filter or subject_filter == "General" or c.get("subject") == subject_filter)
        ]

        scored_chunks = []
        for chunk in candidates:
            content_lower = chunk.get("content", "").lower()
            overlap_count = sum(1 for term in query_terms if term in content_lower)
            if overlap_count > 0:
                score = overlap_count / max(len(query_terms), 1)
                scored_chunks.append((score, chunk))

        # Sort by relevance score descending
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_chunks[:max_chunks]]
