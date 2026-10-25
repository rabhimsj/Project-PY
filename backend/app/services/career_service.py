from __future__ import annotations

from app.models import CareerProfile


class CareerService:
    def __init__(self, db):
        self.db = db

    def analyze_career(self, user_id: int, skills: str, education: str, projects: str, target_job_role: str) -> CareerProfile:
        skill_list = [item.strip() for item in skills.split(',') if item.strip()]
        project_list = [item.strip() for item in projects.split(',') if item.strip()]
        missing = ["SQL", "Problem solving", "Communication", "System design"] if "sql" not in " ".join(skill_list).lower() else []
        roadmap = [
            "Complete one hands-on project aligned with the target role.",
            "Practice mock interviews and behavioral questions.",
            "Study industry-relevant tools and case-based problem solving.",
        ]

        profile = CareerProfile(
            user_id=user_id,
            skills=skills,
            education=education,
            projects=projects,
            target_job_role=target_job_role,
            summary=f"Targeting {target_job_role} with a foundation in {education or 'relevant coursework'}.",
            skill_gap_analysis="Current profile is strong in fundamentals but may benefit from more practical exposure in the role-specific stack and communication skills." if missing else "Profile shows a solid foundation with balanced technical readiness.",
            recommended_skills=", ".join(skill_list + missing) if skill_list else ", ".join(missing),
            learning_roadmap="\n".join(roadmap),
            project_recommendations="Build a portfolio project demonstrating business impact, clean architecture, and measurable outcomes.",
            interview_plan="Practice technical deep-dives, STAR stories, and role-specific problem-solving questions.",
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile
