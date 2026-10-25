from __future__ import annotations

from pathlib import Path

from .database import DB_PATH, get_connection, initialize_database
from .models import Task


class TaskService:
    def __init__(self, db_path: str | Path | None = None):
        self.db_path = Path(db_path) if db_path is not None else DB_PATH
        initialize_database(self.db_path)

    def add_task(
        self,
        title: str,
        description: str = "",
        status: str = "pending",
        due_date: str = "",
    ) -> Task:
        cleaned_title = (title or "").strip()
        if not cleaned_title:
            raise ValueError("Task title is required.")

        cleaned_status = status.strip().lower() if status else "pending"
        if cleaned_status not in {"pending", "in_progress", "completed"}:
            cleaned_status = "pending"

        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks (title, description, status, due_date)
                VALUES (?, ?, ?, ?)
                """,
                (cleaned_title, (description or "").strip(), cleaned_status, due_date.strip() if due_date else ""),
            )
            task_id = cursor.lastrowid

        return self.get_task(task_id)

    def get_task(self, task_id: int) -> Task | None:
        with get_connection(self.db_path) as connection:
            row = connection.execute(
                "SELECT * FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()
            if row is None:
                return None
            return Task.from_row(row)

    def list_tasks(self, status_filter: str | None = None) -> list[Task]:
        query = "SELECT * FROM tasks"
        parameters = []

        if status_filter and status_filter != "all":
            query += " WHERE status = ?"
            parameters.append(status_filter.strip().lower())

        query += " ORDER BY CASE status WHEN 'pending' THEN 1 WHEN 'in_progress' THEN 2 WHEN 'completed' THEN 3 ELSE 4 END, due_date ASC, id DESC"

        with get_connection(self.db_path) as connection:
            rows = connection.execute(query, parameters).fetchall()

        return [Task.from_row(row) for row in rows]

    def update_task(
        self,
        task_id: int,
        *,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
        due_date: str | None = None,
    ) -> Task | None:
        current = self.get_task(task_id)
        if current is None:
            return None

        updated_title = (title if title is not None else current.title).strip()
        if not updated_title:
            raise ValueError("Task title is required.")

        updated_status = (status if status is not None else current.status).strip().lower()
        if updated_status not in {"pending", "in_progress", "completed"}:
            updated_status = current.status

        updated_description = (description if description is not None else current.description).strip()
        updated_due_date = (due_date if due_date is not None else current.due_date).strip()

        with get_connection(self.db_path) as connection:
            connection.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, status = ?, due_date = ?
                WHERE id = ?
                """,
                (updated_title, updated_description, updated_status, updated_due_date, task_id),
            )

        return self.get_task(task_id)

    def mark_done(self, task_id: int) -> Task | None:
        return self.update_task(task_id, status="completed")

    def delete_task(self, task_id: int) -> bool:
        with get_connection(self.db_path) as connection:
            cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cursor.rowcount > 0

    def seed_demo_tasks(self) -> None:
        if self.list_tasks():
            return

        self.add_task("Plan project kickoff", "Define goals and outline milestones.", "pending", "2026-08-30")
        self.add_task("Build UI layout", "Create the dashboard and task form flows.", "in_progress", "2026-08-31")
        self.add_task("Ship first release", "Review and publish the app.", "completed", "2026-09-01")
