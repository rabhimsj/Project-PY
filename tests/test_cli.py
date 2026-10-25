from pathlib import Path

from project_py.task_service import TaskService


def test_task_lifecycle(tmp_path):
    database_path = tmp_path / "tasks.db"
    service = TaskService(db_path=database_path)

    created = service.add_task("Write documentation", "Add project usage notes.", "in_progress", "2026-09-01")
    assert created.title == "Write documentation"

    tasks = service.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].status == "in_progress"

    updated = service.update_task(created.id, title="Write documentation", status="completed")
    assert updated is not None
    assert updated.status == "completed"

    result = service.get_task(created.id)
    assert result is not None
    assert result.status == "completed"

    service.delete_task(created.id)
    assert service.get_task(created.id) is None


def test_filter_tasks_by_status(tmp_path):
    database_path = tmp_path / "tasks.db"
    service = TaskService(db_path=database_path)

    service.add_task("Task 1", "Alpha", "pending", "2026-09-02")
    service.add_task("Task 2", "Beta", "completed", "2026-09-03")

    pending_tasks = service.list_tasks("pending")
    completed_tasks = service.list_tasks("completed")

    assert len(pending_tasks) == 1
    assert len(completed_tasks) == 1
    assert pending_tasks[0].title == "Task 1"
    assert completed_tasks[0].title == "Task 2"
