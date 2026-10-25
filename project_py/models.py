from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Task:
    id: int | None = None
    title: str = ""
    description: str = ""
    status: str = "pending"
    due_date: str = ""

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=row["status"],
            due_date=row["due_date"] or "",
        )
