from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas import StudyPlanRequest, StudyPlanResponse
from app.services.study_plan_service import StudyPlanService

router = APIRouter(prefix="/api/study-plans", tags=["study-plans"])


@router.post("/generate", response_model=StudyPlanResponse)
def generate_study_plan(payload: StudyPlanRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = StudyPlanService(db)
    plan_record = service.generate_plan(
        user_id=current_user.id,
        subject=payload.subject,
        exam_date=payload.exam_date,
        daily_hours=payload.daily_hours,
        preparation_level=payload.preparation_level,
        weak_topics=payload.weak_topics,
    )
    return StudyPlanResponse(
        subject=plan_record.subject,
        exam_date=plan_record.exam_date or "",
        daily_hours=plan_record.daily_hours,
        preparation_level=plan_record.preparation_level,
        weak_topics=plan_record.weak_topics or "",
        plan=[{"day": item["day"], "focus": item["focus"], "tasks": item["tasks"]} for item in __import__("json").loads(plan_record.plan_json)],
    )


@router.get("")
def list_study_plans(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = StudyPlanService(db)
    plans = service.list_plans(current_user.id)
    return [{"id": item.id, "subject": item.subject, "status": item.status, "exam_date": item.exam_date} for item in plans]
