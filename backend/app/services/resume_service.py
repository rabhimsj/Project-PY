from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.models import ResumeAnalysis


class ResumeService:
    def __init__(self, db: Session):
        self.db = db

    def extract_text_from_resume(self, file_path: str) -> str:
        lowered = file_path.lower()
        if lowered.endswith(".pdf"):
            reader = PdfReader(file_path)
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages)
        return Path(file_path).read_text(errors="replace")

    def analyze_resume(self, user_id: int, file_name: str, file_path: str, job_role: str | None = None) -> ResumeAnalysis:
        text = self.extract_text_from_resume(file_path)
        lower_text = text.lower()
        skills = ["python", "sql", "javascript", "communication", "problem solving"]
        found_skills = [skill for skill in skills if skill in lower_text]
        project_keywords = ["project", "experience", "portfolio", "internship", "dashboard"]
        project_mentions = [keyword for keyword in project_keywords if keyword in lower_text]
        missing_keywords = ["leadership", "scope", "impact"] if "leadership" not in lower_text else []

        analysis = ResumeAnalysis(
            user_id=user_id,
            file_name=file_name,
            skills=", ".join(found_skills) if found_skills else "No major skills detected.",
            projects=", ".join(project_mentions) if project_mentions else "Project details could be improved.",
            missing_keywords=", ".join(missing_keywords) if missing_keywords else "No obvious missing keywords.",
            structure_score=80 if "experience" in lower_text else 70,
            job_alignment=f"Strong alignment for {job_role or 'the target role'} with a few improvements in project impact storytelling." if job_role else "The resume is generally well structured.",
            suggestions="Add measurable outcomes, clear project impact, and role-specific keywords to improve ATS compatibility.",
            summary="The resume has potential, but strengthening achievement statements and role-specific keywords will improve alignment.",
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis
