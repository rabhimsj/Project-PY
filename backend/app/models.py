from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    profile: Mapped[Optional["Profile"]] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    documents: Mapped[list["Document"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    study_plans: Mapped[list["StudyPlan"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    attendance_records: Mapped[list["AttendanceRecord"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    marks: Mapped[list["MarkRecord"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    career_profiles: Mapped[list["CareerProfile"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    resume_analyses: Mapped[list["ResumeAnalysis"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    interview_sessions: Mapped[list["InterviewSession"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    branch: Mapped[Optional[str]] = mapped_column(String(255), default="")
    semester: Mapped[Optional[str]] = mapped_column(String(50), default="")
    graduation_year: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    target_role: Mapped[Optional[str]] = mapped_column(String(255), default="")
    bio: Mapped[Optional[str]] = mapped_column(Text, default="")
    skills: Mapped[Optional[str]] = mapped_column(Text, default="")
    interests: Mapped[Optional[str]] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="profile")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), default="application/octet-stream")
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, default="")
    metadata_json: Mapped[Optional[str]] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="documents")
    chunks: Mapped[list["DocumentChunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[Optional[str]] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    document: Mapped[Document] = relationship(back_populates="chunks")


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), default="New chat")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_document_id: Mapped[Optional[int]] = mapped_column(ForeignKey("documents.id", ondelete="SET NULL"), default=None)
    metadata_json: Mapped[Optional[str]] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    conversation: Mapped[Conversation] = relationship(back_populates="messages")


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    current_score: Mapped[Optional[float]] = mapped_column(default=None)
    target_score: Mapped[Optional[float]] = mapped_column(default=None)
    weak_topics: Mapped[Optional[str]] = mapped_column(Text, default="")


class AttendanceRecord(Base):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    attended_classes: Mapped[int] = mapped_column(Integer, default=0)
    total_classes: Mapped[int] = mapped_column(Integer, default=0)
    attendance_percentage: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="attendance_records")


class MarkRecord(Base):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    exam_name: Mapped[str] = mapped_column(String(255), nullable=False)
    score: Mapped[float] = mapped_column(default=0.0)
    max_score: Mapped[float] = mapped_column(default=100.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="marks")


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    exam_date: Mapped[Optional[str]] = mapped_column(String(50), default="")
    daily_hours: Mapped[int] = mapped_column(Integer, default=2)
    preparation_level: Mapped[str] = mapped_column(String(50), default="beginner")
    weak_topics: Mapped[Optional[str]] = mapped_column(Text, default="")
    plan_json: Mapped[str] = mapped_column(Text, default="[]")
    status: Mapped[str] = mapped_column(String(50), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="study_plans")


class StudyTask(Base):
    __tablename__ = "study_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    study_plan_id: Mapped[int] = mapped_column(ForeignKey("study_plans.id", ondelete="CASCADE"), nullable=False)
    day_index: Mapped[int] = mapped_column(Integer, default=1)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="pending")


class CareerProfile(Base):
    __tablename__ = "career_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skills: Mapped[str] = mapped_column(Text, default="")
    education: Mapped[str] = mapped_column(Text, default="")
    projects: Mapped[str] = mapped_column(Text, default="")
    target_job_role: Mapped[str] = mapped_column(String(255), default="")
    summary: Mapped[Optional[str]] = mapped_column(Text, default="")
    skill_gap_analysis: Mapped[Optional[str]] = mapped_column(Text, default="")
    recommended_skills: Mapped[Optional[str]] = mapped_column(Text, default="")
    learning_roadmap: Mapped[Optional[str]] = mapped_column(Text, default="")
    project_recommendations: Mapped[Optional[str]] = mapped_column(Text, default="")
    interview_plan: Mapped[Optional[str]] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="career_profiles")


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    skills: Mapped[Optional[str]] = mapped_column(Text, default="")
    projects: Mapped[Optional[str]] = mapped_column(Text, default="")
    missing_keywords: Mapped[Optional[str]] = mapped_column(Text, default="")
    structure_score: Mapped[int] = mapped_column(Integer, default=0)
    job_alignment: Mapped[Optional[str]] = mapped_column(Text, default="")
    suggestions: Mapped[Optional[str]] = mapped_column(Text, default="")
    summary: Mapped[Optional[str]] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="resume_analyses")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_role: Mapped[str] = mapped_column(String(255), nullable=False)
    session_summary: Mapped[Optional[str]] = mapped_column(Text, default="")
    questions_json: Mapped[Optional[str]] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped[User] = relationship(back_populates="interview_sessions")
