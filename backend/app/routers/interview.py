from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas import InterviewRequest
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/api/interview", tags=["interview"])


@router.post("/generate")
def generate_interview_questions(payload: InterviewRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = InterviewService(db)
    session = service.generate_questions(current_user.id, payload.target_role, payload.student_skills, payload.resume_summary)
    return {"id": session.id, "target_role": session.target_role, "questions": session.questions_json}
