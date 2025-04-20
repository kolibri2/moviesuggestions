import sqlite3

DB_PATH = "../Databases/moviesuggestion.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    try:
        yield conn
    finally:
        conn.close()
