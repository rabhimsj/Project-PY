from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models import CareerProfile, User
from app.schemas import CareerProfileInput
from app.services.career_service import CareerService

router = APIRouter(prefix="/api/career", tags=["career"])


@router.post("/analyze")
def analyze_career(payload: CareerProfileInput, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = CareerService(db)
    profile = service.analyze_career(current_user.id, payload.skills, payload.education, payload.projects, payload.target_job_role)
    return {"id": profile.id, "target_job_role": profile.target_job_role, "summary": profile.summary, "recommended_skills": profile.recommended_skills}


@router.get("")
def get_career_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(CareerProfile).filter(CareerProfile.user_id == current_user.id).order_by(CareerProfile.created_at.desc()).first()
    if not profile:
        return {"message": "No career profile found yet."}
    return {"target_job_role": profile.target_job_role, "summary": profile.summary, "learning_roadmap": profile.learning_roadmap}
