from __future__ import annotations

import json
from datetime import datetime

from app.models import StudyPlan, StudyTask


class StudyPlanService:
    def __init__(self, db):
        self.db = db

    def generate_plan(self, user_id: int, subject: str, exam_date: str, daily_hours: int, preparation_level: str, weak_topics: str) -> StudyPlan:
        topics = weak_topics.split(',') if weak_topics else ["core concepts", "problem solving", "revision"]
        plan = []
        for day_index in range(1, 8):
            plan.append({
                "day": day_index,
                "focus": f"Day {day_index}: revise {subject} fundamentals and solve practice questions",
                "duration_hours": max(1, daily_hours),
                "tasks": [
                    f"Revise {topics[0].strip() if topics else 'core concepts'}",
                    f"Practice 10 questions for {subject}",
                    "Review mistakes and update notes",
                ],
            })

        plan_record = StudyPlan(
            user_id=user_id,
            subject=subject,
            exam_date=exam_date,
            daily_hours=daily_hours,
            preparation_level=preparation_level,
            weak_topics=weak_topics,
            plan_json=json.dumps(plan),
        )
        self.db.add(plan_record)
        self.db.commit()
        self.db.refresh(plan_record)

        for day_index, item in enumerate(plan, start=1):
            for task in item["tasks"]:
                self.db.add(StudyTask(study_plan_id=plan_record.id, day_index=day_index, title=task, status="pending"))
        self.db.commit()
        return plan_record

    def list_plans(self, user_id: int) -> list[StudyPlan]:
        return self.db.query(StudyPlan).filter(StudyPlan.user_id == user_id).order_by(StudyPlan.created_at.desc()).all()
