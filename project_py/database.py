from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "tasks.db"


def get_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    target = Path(db_path) if db_path is not None else DB_PATH
    connection = sqlite3.connect(target)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(db_path: str | Path | None = None) -> None:
    with get_connection(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'pending',
                due_date TEXT DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
