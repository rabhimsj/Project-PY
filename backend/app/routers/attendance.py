from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models import AttendanceRecord, User
from app.schemas import AttendanceInput, AttendanceResult
from app.services.attendance_service import AttendanceService

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


@router.post("/analyze", response_model=AttendanceResult)
def analyze_attendance(payload: AttendanceInput, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = AttendanceService(db)
    result = service.analyze_attendance(current_user.id, payload.subject, payload.attended_classes, payload.total_classes)
    return AttendanceResult(**result)


@router.get("")
def list_attendance(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(AttendanceRecord).filter(AttendanceRecord.user_id == current_user.id).all()
    return [{"id": item.id, "subject": item.subject, "attendance_percentage": item.attendance_percentage, "attended_classes": item.attended_classes, "total_classes": item.total_classes} for item in records]
