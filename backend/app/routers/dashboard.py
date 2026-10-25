from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models import User
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/overview")
def dashboard_overview(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = DashboardService(db)
    return service.get_overview(current_user.id)
