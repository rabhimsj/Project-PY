from __future__ import annotations

from app.models import MarkRecord


class MarksService:
    def __init__(self, db):
        self.db = db

    def add_mark(self, user_id: int, subject: str, exam_name: str, score: float, max_score: float = 100.0) -> MarkRecord:
        record = MarkRecord(user_id=user_id, subject=subject, exam_name=exam_name, score=score, max_score=max_score)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_summary(self, user_id: int) -> dict:
        records = self.db.query(MarkRecord).filter(MarkRecord.user_id == user_id).all()
        if not records:
            return {"average": 0.0, "highest_subject": None, "lowest_subject": None, "weak_subjects": [], "suggestions": []}

        per_subject = {}
        for record in records:
            per_subject.setdefault(record.subject, []).append(record.score)

        subject_averages = {subject: sum(values) / len(values) for subject, values in per_subject.items()}
        highest_subject = max(subject_averages.items(), key=lambda item: item[1])
        lowest_subject = min(subject_averages.items(), key=lambda item: item[1])
        weak_subjects = [subject for subject, score in subject_averages.items() if score < 60]

        average = round(sum(subject_averages.values()) / len(subject_averages), 2)
        suggestions = []
        if weak_subjects:
            suggestions.append(f"Focus on improving {', '.join(weak_subjects)} with targeted practice and revision blocks.")
        suggestions.append("Review mistakes from recent assessments and solve chapter-wise practice questions.")

        return {
            "average": average,
            "highest_subject": {"subject": highest_subject[0], "score": round(highest_subject[1], 2)},
            "lowest_subject": {"subject": lowest_subject[0], "score": round(lowest_subject[1], 2)},
            "weak_subjects": weak_subjects,
            "suggestions": suggestions,
        }
