import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "students.db"
SQL_FILE = Path(__file__).parent / "create_students.sql"

def init_db():
    if DB_PATH.exists():
        print(f"{DB_PATH} already exists. Remove it if you want a fresh DB.")
        return
    sql = SQL_FILE.read_text()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(sql)
    conn.commit()
    conn.close()
    print(f"Initialized database at {DB_PATH}")

if __name__ == "__main__":
    init_db()
