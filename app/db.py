import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "Databases"
DB_PATH = DB_DIR / "moviesuggestion.db"


def get_connection():
    conn = sqlite3.connect(
        DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False
    )
    try:
        yield conn
    finally:
        conn.close()
