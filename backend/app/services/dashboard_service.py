from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import AttendanceRecord, Document, MarkRecord, StudyPlan, User


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_overview(self, user_id: int) -> dict:
        attendance = self.db.query(AttendanceRecord).filter(AttendanceRecord.user_id == user_id).all()
        marks = self.db.query(MarkRecord).filter(MarkRecord.user_id == user_id).all()
        documents = self.db.query(Document).filter(Document.user_id == user_id).count()
        study_plans = self.db.query(StudyPlan).filter(StudyPlan.user_id == user_id).count()

        attendance_percent = round(sum(record.attendance_percentage for record in attendance) / len(attendance), 2) if attendance else 0.0
        recent_marks = [
            {"subject": record.subject, "score": record.score, "exam_name": record.exam_name}
            for record in marks[-5:]
        ]

        return {
            "attendance_percentage": attendance_percent,
            "recent_marks": recent_marks,
            "uploaded_documents": documents,
            "study_plans": study_plans,
            "recommendations": [
                "Review your weakest subject with daily practice blocks.",
                "Prioritize consistency in attendance and revision timing.",
                "Create a 2-week revision cycle using uploaded notes and PDFs."
            ],
            "career_progress": "On track",
            "quick_actions": [
                "Upload notes",
                "Ask AI assistant",
                "Generate study plan",
                "Analyze attendance",
            ],
        }
