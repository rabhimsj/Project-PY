from __future__ import annotations

import json

from app.models import InterviewSession


class InterviewService:
    def __init__(self, db):
        self.db = db

    def generate_questions(self, user_id: int, target_role: str, student_skills: str, resume_summary: str) -> InterviewSession:
        skill_tokens = [item.strip() for item in student_skills.split(',') if item.strip()]
        question_set = [
            {
                "type": "technical",
                "difficulty": "medium",
                "question": f"Explain a project or concept related to {skill_tokens[0] if skill_tokens else 'your core domain'} and why it matters.",
                "sample_answer": "Describe the problem, your approach, decisions you made, and measurable outcomes.",
            },
            {
                "type": "hr",
                "difficulty": "easy",
                "question": "Why do you want to work in this role and what motivates you?",
                "sample_answer": "Share your interest in the role, your learning goals, and how the company or domain matches your strengths.",
            },
            {
                "type": "follow_up",
                "difficulty": "medium",
                "question": "What would you improve in your current work or project if you had more time?",
                "sample_answer": "Discuss improvements such as optimization, code quality, user experience, or testing strategy.",
            },
        ]

        session = InterviewSession(
            user_id=user_id,
            target_role=target_role,
            session_summary=f"Interview preparation plan for {target_role} based on the provided profile and resume summary.",
            questions_json=json.dumps(question_set),
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
