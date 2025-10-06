# raw_sql_demo.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "students.db"

def param_demo(gpa_min):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, major, gpa FROM Students WHERE gpa >= ?", (gpa_min,))
    rows = cur.fetchall()
    conn.close()
    return rows

def vulnerable_demo(gpa_min_user_input):
    # Simulate a naive concatenation (vulnerable if input is malicious)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = f"SELECT id, name, major, gpa FROM Students WHERE gpa >= {gpa_min_user_input};"
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    print("Safe parameterized query (gpa_min=3.6):")
    print(param_demo(3.6))

    print("\nVulnerable concatenation with benign input '3.6':")
    print(vulnerable_demo("3.6"))

    print("\nVulnerable concatenation with malicious input to demonstrate injection (example):")
    malicious = "0; DROP TABLE Students; --"
    try:
        print(vulnerable_demo(malicious))
    except Exception as e:
        print("Error (as expected):", e)
        print("This shows why concatenating untrusted input into SQL is dangerous.")
