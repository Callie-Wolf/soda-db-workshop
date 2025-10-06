SoDA — Database Fundamentals Workshop
====================================

A complete, hands-on demo repository to teach Database Fundamentals for Software Engineering.
This README contains detailed instructions, project structure, examples, and teaching notes you can
use for your SoDA workshop (slides + live demo + hands-on challenge).

Repository purpose
------------------
This repo demonstrates:
- Basic SQL (SQLite) schema + queries
- A minimal backend (Flask) exposing GET/POST endpoints
- ORM usage with SQLAlchemy
- Raw SQL examples showing safe parameterization vs vulnerable string concatenation
- How to view and export the database
- A hands-on workshop challenge with a rubric
- Optional perf & indexing demo

Repository structure
--------------------
```
soda-db-workshop/
├── README.txt                      # (this file) workshop guide & instructions
├── requirements.txt                # Python dependencies
├── create_students.sql             # SQL schema + seed data
├── init_db.py                      # Initialize students.db from SQL file
├── students.db                     # (optional) the SQLite DB - typically .gitignored
├── orm_models.py                   # SQLAlchemy models and DB wrapper class
├── server_with_db.py               # Flask server demonstrating GET/POST and raw SQL
├── raw_sql_demo.py                 # Demo: parameterized vs vulnerable SQL
├── view_db.py                      # Pretty-print Students table (pandas fallback)
├── client_examples.sh              # curl examples (for Bash / Git Bash / WSL)
├── client_examples.ps1             # PowerShell examples (for Windows)
├── workshop_challenge.md           # Challenge prompt + rubric for attendees
├── .gitignore
└── README.txt      
```                

Quick setup (Linux / macOS / WSL)
---------------------------------
# clone + virtual environment
git clone <repo-url>
cd soda-db-workshop
python -m venv .venv
source .venv/bin/activate

# install deps
pip install -r requirements.txt

# create DB
python init_db.py

# run server (Flask)
python server_with_db.py

Server will run at: http://127.0.0.1:8000

Quick setup (Windows PowerShell)
--------------------------------
Open PowerShell in repo folder:

# create & activate venv
python -m venv .venv
# activate
.\.venv\Scripts\Activate.ps1   # or: . .venv\Scripts\Activate.ps1

# install
pip install -r requirements.txt

# initialize DB
python init_db.py

# run server
python server_with_db.py

PowerShell: Using client examples
--------------------------------
We included a PowerShell helper: client_examples.ps1. Run it after starting the server:

.\client_examples.ps1

This will:
- POST /students with a sample student
- GET /students?gpa_min=3.6
- Show /raw-query demonstrations (safe and unsafe)

Files and purpose
-----------------
- create_students.sql
  - Schema for Students table and seed data.
- init_db.py
  - Reads create_students.sql and creates students.db in the repo.
- orm_models.py
  - SQLAlchemy declarative models (Student) and DB wrapper class (DB).
  - Contains methods: add_students(list), get_students_with_min_gpa(gpa)
- server_with_db.py
  - Flask app exposing:
    - GET  /            -> index
    - POST /students   -> insert JSON student
    - GET  /students   -> list students (filter by gpa_min)
    - GET  /raw-query  -> demo parameterized vs unsafe SQL (unsafe only for demo)
- raw_sql_demo.py
  - Demonstrates sqlite3 parameterized queries vs vulnerable concatenation
  - Shows a simulated malicious input and why concatenation is unsafe
- view_db.py
  - Prints Students table in a readable tabular format (pandas if available, fallback to sqlite)
- client_examples.sh
  - curl examples for Bash / WSL
- client_examples.ps1
  - PowerShell examples for Windows
- populate_db.py & measure_perf.py
  - Tools to generate many records and measure indexing performance
- workshop_challenge.md
  - Challenge prompt & rubric for participants
- .gitignore
  - excludes .venv and students.db (recommended to create DB at runtime)

How to use the server (examples)
--------------------------------
# Insert a student (Bash / Git Bash)
curl -X POST http://127.0.0.1:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Lina Park","major":"AI","gpa":3.7}'

# Query students (Bash)
curl "http://127.0.0.1:8000/students?gpa_min=3.6"

# Parameterized raw query (safe)
curl "http://127.0.0.1:8000/raw-query?gpa_min=3.6"

# Unsafe concatenation demo (do not use in prod)
curl "http://127.0.0.1:8000/raw-query?gpa_min=3.6&unsafe=1"

PowerShell equivalents are in client_examples.ps1

How to view the DB table
------------------------
Option A — view_db.py (recommended)
python view_db.py

Option B — using sqlite3 CLI (Git Bash / WSL)
sqlite3 students.db
sqlite> .headers on
sqlite> .mode column
sqlite> SELECT * FROM Students;

Option C — GUI
- DB Browser for SQLite: https://sqlitebrowser.org
- VS Code: "SQLite" extension (open students.db and browse tables)

<!-- Export to CSV (for slides or Excel)
----------------------------------
Run this Python snippet to export:
python - <<'PY'
import sqlite3, csv
conn = sqlite3.connect('students.db')
cur = conn.cursor()
cur.execute("SELECT * FROM Students")
with open('students_export.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([d[0] for d in cur.description])
    writer.writerows(cur.fetchall())
conn.close()
print("Exported students_export.csv")
PY

Teaching flow (recommended 60 minutes)
-------------------------------------
1) Intro (5 min)
   - Why DBs matter / examples (Instagram, banking, logs)
2) Types of Databases (5 min)
   - Relational (SQL), Document (NoSQL), Key-Value, Graph, Time-Series
3) Brief history of SQL (3 min)
4) SQL Basics + Schema (10 min)
   - Show create_students.sql and run SELECTs live
5) Live demo: server + DB integration (15 min)
   - Start server, POST a student, GET students -> show persistence
   - Walk through server_with_db.py: where DB calls are made
6) ORM demo (10 min)
   - Open orm_models.py, show session.add / session.query
   - Discuss benefits & tradeoffs of ORMs
7) Security tie-in (5 min)
   - Run raw_sql_demo.py and explain parameterized queries vs concatenation
8) Hands-on challenge (15-25 min)
   - See workshop_challenge.md: participants refactor schema, implement safe insert, and query endpoint
9) Wrap-up & resources (5 min)

Workshop challenge (copy into slides)
-------------------------------------
Title: Fix the Redundant Preference Schema & Implement Safe Endpoints

Given (bad schema):
CREATE TABLE Users (id INTEGER PRIMARY KEY, username TEXT, favorite_color TEXT);
CREATE TABLE Preferences (user_id INTEGER, favorite_color TEXT, FOREIGN KEY(user_id) REFERENCES Users(id));

Tasks:
1. Refactor schema to remove redundancy (support multiple preferences per user).
2. Implement POST /students to insert safely (parameterized SQL or ORM).
3. Implement GET /students?gpa_min=... returning JSON of students.
4. Bonus: Add index on gpa and show performance improvement with populate_db.py and measure_perf.py.

Rubric (10 points):
- Schema refactor correct: 3 pts
- Safe insert (no string concatenation): 3 pts
- GET filtering + JSON: 2 pts
- Bonus index + perf demo: 2 pts

Discussion points and presenter notes
------------------------------------
- Where to put DB logic: request handler vs service layer. Recommend separation for maintainability.
- Connection pooling: SQLite is not ideal for heavy concurrency. Mention PostgreSQL and SQLAlchemy pool for production.
- Indexes: useful for selective queries (e.g., gpa thresholds), but not free — discuss write overhead.
- Migration / schema evolution: mention Alembic (SQLAlchemy) or Django migrations when changing schema in real apps.
- Security: always use parameterized queries or ORM query builders to avoid SQL injection.

Optional next steps to improve the repo
--------------------------------------
- Add Dockerfile + docker-compose for reproducible demos
- Replace Flask with FastAPI for modern ASGI + docs (auto /docs)
- Add a Jupyter / Colab notebook for interactive attendees who cannot run locally
- Add tests and simple CI to run linting and basic DB integration checks -->

Troubleshooting (common issues)
-------------------------------
- "sqlite3.OperationalError: database is locked": close other processes, restart server, or use a smaller dataset.
- Windows PowerShell: if script execution is blocked, run:
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
- If pandas read_sql_query fails, ensure you pass a connection or use sqlite:///students.db as URL.
- If Flask not found: ensure venv activated and `pip install -r requirements.txt` ran successfully.

