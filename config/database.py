"""SQLite database configuration."""
import os
import sqlite3
from pathlib import Path
from typing import Generator

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Database:
    """Open the local SQLite database and ensure its schema exists."""
    def __init__(self) -> None:
        self.db_path = Path(os.getenv(
            "DB_PATH", str(PROJECT_ROOT / "database" / "food_recipe.sqlite3")
        ))

    def get_connection(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.isolation_level = None
        conn.execute("PRAGMA foreign_keys = ON")

        schema_path = PROJECT_ROOT / "database" / "schema_sqlite.sql"
        conn.executescript(schema_path.read_text(encoding="utf-8"))
        return conn


# FastAPI Dependency — ใช้กับ Depends(get_db) ใน router
def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = Database().get_connection()
    try:
        yield conn
    finally:
        conn.close()
