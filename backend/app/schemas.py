from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=2, max_length=120)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    password: str


class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str = "bearer"


class ProfileUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    branch: str | None = None
    semester: str | None = None
    graduation_year: int | None = None
    target_role: str | None = None
    bio: str | None = None
    skills: str | None = None
    interests: str | None = None


class ProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    branch: str | None = None
    semester: str | None = None
    graduation_year: int | None = None
    target_role: str | None = None
    bio: str | None = None
    skills: str | None = None
    interests: str | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    username: str
    full_name: str
    profile: ProfileRead | None = None


class AttendanceInput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    attended_classes: int
    total_classes: int


class AttendanceResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    attendance_percentage: float
    required_classes: int | None = None
    safe_absence_limit: int | None = None
    target: float | None = None


class MarkInput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    exam_name: str
    score: float
    max_score: float = 100.0


class CareerProfileInput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    skills: str
    education: str
    projects: str
    target_job_role: str


class DocumentSummaryRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    summary_type: str = "short"


class ChatMessageRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message: str
    conversation_id: int | None = None


class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    answer: str
    conversation_id: int
    source_documents: list[str] = Field(default_factory=list)


class StudyPlanRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    exam_date: str
    daily_hours: int = 2
    preparation_level: str = "intermediate"
    weak_topics: str = ""


class StudyPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject: str
    exam_date: str
    daily_hours: int
    preparation_level: str
    weak_topics: str
    plan: list[dict[str, Any]]


class ResumeAnalysisRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    job_role: str | None = None


class InterviewRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    target_role: str
    student_skills: str = ""
    resume_summary: str = ""
