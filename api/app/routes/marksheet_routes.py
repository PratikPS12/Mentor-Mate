import os
from typing import Dict, Any
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from app.routes.auth_routes import get_current_user
from app.services.document.ocr_service import MarksheetOCRService
from app.models.schemas import MarksheetVerificationPayload

from app.core.database import db_manager

router = APIRouter(prefix="/marksheet", tags=["Marksheet Document Intelligence"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_marksheet(
    file: UploadFile = File(...),
    user: Dict[str, Any] = Depends(get_current_user)
):
    if not file.filename.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png', '.txt')):
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF, JPG, PNG or TXT.")

    file_ext = os.path.splitext(file.filename)[1]
    safe_filename = f"{user['id']}_{file.filename}"
    saved_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(saved_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Trigger OCR and Document extraction
    result = await MarksheetOCRService.process_marksheet_file(saved_path, file.filename, user["id"])
    return result

@router.post("/verify")
async def verify_marksheet(
    payload: MarksheetVerificationPayload,
    user: Dict[str, Any] = Depends(get_current_user)
):
    result = await MarksheetOCRService.verify_and_commit(user["id"], payload.model_dump())
    return result

from app.services.document.study_material_service import StudyMaterialService

@router.post("/notes/upload")
@router.post("/study-material/upload")
async def upload_study_material(
    file: UploadFile = File(...),
    title: str = Query(None),
    subject: str = Query("General"),
    user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Ingests study materials (PDF, JPG, PNG, TXT, MD) using OCR and AI Document Intelligence.
    Extracts key formulas, concepts, summary, generates diagnostic quiz items and course modules,
    and indexes semantic RAG chunks for Socratic tutoring.
    """
    valid_exts = ('.pdf', '.jpg', '.jpeg', '.png', '.webp', '.txt', '.csv', '.md')
    if not file.filename.lower().endswith(valid_exts):
        raise HTTPException(status_code=400, detail="Supported formats: PDF, JPG, PNG, TXT, MD.")

    raw_bytes = await file.read()
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    try:
        result = await StudyMaterialService.process_and_save_study_material(
            student_id=user["id"],
            filename=file.filename,
            file_bytes=raw_bytes,
            title=title,
            subject=subject
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Study material analysis error: {str(e)}")

@router.get("/notes")
@router.get("/study-material")
async def get_uploaded_study_materials(user: Dict[str, Any] = Depends(get_current_user)):
    materials = await StudyMaterialService.get_student_materials(user["id"])
    return {"materials": materials}

@router.get("/study-material/{material_id}")
async def get_study_material_detail(material_id: str, user: Dict[str, Any] = Depends(get_current_user)):
    mat = await StudyMaterialService.get_material_by_id(material_id, user["id"])
    if not mat:
        raise HTTPException(status_code=404, detail="Study material document not found")
    return mat
