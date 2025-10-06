# view_db.py
from pathlib import Path
DB = Path(__file__).parent / "students.db"

def view_with_sqlite3():
    import sqlite3
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(Students);")
    cols = [c[1] for c in cur.fetchall()]
    cur.execute("SELECT * FROM Students;")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No rows found in Students table.")
        return

    # pretty simple column widths
    col_widths = [max(len(str(col)), *(len(str(r[i])) for r in rows)) for i, col in enumerate(cols)]
    header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(cols))
    sep = "-".join("-" * (w + 2) for w in col_widths)
    print(header)
    print(sep)
    for r in rows:
        print(" | ".join(str(r[i]).ljust(col_widths[i]) for i in range(len(cols))))

def view_with_pandas():
    import pandas as pd
    # Option A: pass SQLAlchemy-style URL:
    # df = pd.read_sql_query("SELECT * FROM Students", "sqlite:///students.db")
    # Option B (preferred): pass an sqlite3 connection object
    import sqlite3
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM Students", conn)
    conn.close()
    print(df.to_string(index=False))

if __name__ == "__main__":
    try:
        # Prefer pandas if available
        import pandas  # type: ignore
        view_with_pandas()
    except Exception:
        view_with_sqlite3()
