from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.init_db import init_db
from app.routers.attendance import router as attendance_router
from app.routers.auth import router as auth_router
from app.routers.career import router as career_router
from app.routers.chat import router as chat_router
from app.routers.dashboard import router as dashboard_router
from app.routers.documents import router as documents_router
from app.routers.interview import router as interview_router
from app.routers.marks import router as marks_router
from app.routers.resume import router as resume_router
from app.routers.study_plans import router as study_plans_router
from app.routers.users import router as users_router

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(dashboard_router)
app.include_router(documents_router)
app.include_router(chat_router)
app.include_router(study_plans_router)
app.include_router(attendance_router)
app.include_router(marks_router)
app.include_router(career_router)
app.include_router(resume_router)
app.include_router(interview_router)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
