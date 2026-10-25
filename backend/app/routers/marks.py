from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models import MarkRecord, User
from app.schemas import MarkInput
from app.services.marks_service import MarksService

router = APIRouter(prefix="/api/marks", tags=["marks"])


@router.post("")
def add_mark(payload: MarkInput, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = MarksService(db)
    record = service.add_mark(current_user.id, payload.subject, payload.exam_name, payload.score, payload.max_score)
    return {"id": record.id, "subject": record.subject, "score": record.score}


@router.get("/summary")
def marks_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = MarksService(db)
    return service.get_summary(current_user.id)
