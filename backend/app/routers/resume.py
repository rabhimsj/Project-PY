from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas import ResumeAnalysisRequest
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/api/resume", tags=["resume"])


@router.post("/analyze")
def analyze_resume(
    file: UploadFile = File(...),
    payload: ResumeAnalysisRequest = ResumeAnalysisRequest(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Resume file is required")
    if not file.filename.lower().endswith((".pdf", ".docx", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT resumes are supported")

    file_bytes = file.file.read()
    saved_path = f"/tmp/{file.filename}"
    with open(saved_path, "wb") as handle:
        handle.write(file_bytes)
    service = ResumeService(db)
    analysis = service.analyze_resume(current_user.id, file.filename, saved_path, payload.job_role)
    return {"id": analysis.id, "file_name": analysis.file_name, "skills": analysis.skills, "summary": analysis.summary}
