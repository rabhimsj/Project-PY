from __future__ import annotations

from app.models import AttendanceRecord


class AttendanceService:
    def __init__(self, db):
        self.db = db

    def analyze_attendance(self, user_id: int, subject: str, attended: int, total: int, target: float = 75.0) -> dict:
        if total <= 0:
            raise ValueError("Total classes must be greater than zero.")
        percentage = round((attended / total) * 100, 2)
        required = None
        safe_limit = None

        if percentage < target:
            required_classes = 0
            remaining_classes = total
            while True:
                projected = ((attended + required_classes) / (total + required_classes)) * 100
                if projected >= target:
                    break
                required_classes += 1
            required = required_classes
        else:
            required = 0

        if percentage >= 0:
            safe_limit = max(0, total - int((target * total) / 100))

        record = AttendanceRecord(
            user_id=user_id,
            subject=subject,
            attended_classes=attended,
            total_classes=total,
            attendance_percentage=percentage,
        )
        self.db.add(record)
        self.db.commit()

        return {
            "subject": subject,
            "attendance_percentage": percentage,
            "required_classes": required,
            "safe_absence_limit": safe_limit,
            "target": target,
        }
