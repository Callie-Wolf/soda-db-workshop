Workshop Challenge — SoDA Database Fundamentals
=================================================

Duration: 30 minutes (core) + 15 minutes (bonus / demo)
Group size: individual or pairs
Goal: Refactor a redundant schema, implement safe endpoints, and demonstrate basic DB performance tuning.

Overview
--------
You are provided with a small demo server and a seeded SQLite database (`students.db`). Your job is to:
1. Identify and fix a redundant schema (design change).
2. Implement/verify two HTTP endpoints:
   - POST /students  --> safely insert a student record (JSON body)
   - GET  /students?gpa_min=<float>  --> return JSON list of students with gpa >= gpa_min
3. (Bonus) Add an index on `gpa`, populate many rows, and measure the speed-up.

Prerequisites (what should already be set up)
--------------------------------------------
- Python 3.8+ (recommended)
- Virtual environment with requirements installed:
  python -m venv .venv
  source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
- Database initialized:
  python init_db.py
- Server can be started:
  python server_with_db.py
  (server runs at http://127.0.0.1:8000)

Files you'll work with
----------------------
- create_students.sql : schema + seed data
- init_db.py           : creates students.db
- students.db          : SQLite DB (if present)
- server_with_db.py    : Flask server (starter)
- orm_models.py        : SQLAlchemy models and DB wrapper
- raw_sql_demo.py      : parameterized vs vulnerable SQL demo
- populate_db.py       : generates many rows for perf testing
- measure_perf.py      : measures query time before/after index

Starter "bad" schema (what to refactor)
--------------------------------------
The problematic schema example (not in students.db, but shown for exercise):
CREATE TABLE Users (id INTEGER PRIMARY KEY, username TEXT, favorite_color TEXT);
CREATE TABLE Preferences (user_id INTEGER, favorite_color TEXT, FOREIGN KEY(user_id) REFERENCES Users(id));

Problem: `favorite_color` stored in both tables (redundant). Also `Preferences` lacks a primary key and can't represent multiple preferences per user cleanly.

Task list (core)
----------------
1) Schema refactor (3 points)
   - Propose a corrected schema that:
     - Removes redundancy
     - Supports multiple preferences per user (if applicable)
     - Uses proper keys (primary key, foreign key)
   - Example refactor (acceptable):
     CREATE TABLE Users (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         username TEXT NOT NULL,
         email TEXT
     );
     CREATE TABLE Preferences (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         user_id INTEGER NOT NULL,
         preference_key TEXT NOT NULL,
         preference_value TEXT,
         FOREIGN KEY(user_id) REFERENCES Users(id)
     );

2) Implement safe POST (3 points)
   - Ensure `POST /students` accepts JSON body:
     { "name": "Lina Park", "major": "AI", "gpa": 3.7 }
   - Insert into DB **safely** using:
     - parameterized SQL (sqlite3 with `?` placeholders) OR
     - ORM method (SQLAlchemy session.add/commit)
   - Do NOT use string concatenation with untrusted input.

3) Implement GET filter & JSON output (2 points)
   - Ensure `GET /students?gpa_min=<value>` returns a JSON array of students with gpa >= gpa_min
   - Output format per student:
     { "id": 1, "name": "Alex Kim", "major": "Computer Science", "gpa": 3.9 }

4) Deliverables (what to submit)
   - A short Git branch or zip with:
     - Modified server_with_db.py (or new server file)
     - SQL schema changes (if you created a new SQL file)
     - Short README describing how to run your solution and how you tested it
   - Optional: a short terminal transcript or screenshots demonstrating curl/Invoke-RestMethod calls working.

Bonus tasks (2 points)
----------------------
A) Index & perf (2 points)
   - Use populate_db.py to add many rows (e.g., 10k–50k).
   - Run measure_perf.py to time a sample SELECT COUNT or SELECT * WHERE gpa >= X.
   - Create an index: CREATE INDEX idx_students_gpa ON Students(gpa);
   - Re-run measure_perf.py and report the timing improvement.

B) Extra: Add a simple client test script that validates POST+GET flow automatically.

Evaluation rubric (10 points total)
----------------------------------
- Schema refactor correct and justified: 3 pts
- POST implemented safely (no concatenation): 3 pts
- GET filter + JSON format correct: 2 pts
- Bonus index + perf demo: 2 pts

Hints & guidance
----------------
- Use ORM (SQLAlchemy) if you want to avoid writing raw SQL; it's easier and safer for the workshop.
- To inspect DB locally: python view_db.py OR use DB Browser for SQLite / VS Code SQLite extension.
- For parameterized sqlite3 example:
  conn = sqlite3.connect("students.db")
  cur = conn.cursor()
  cur.execute("INSERT INTO Students (name,major,gpa) VALUES (?,?,?)", (name, major, gpa))
  conn.commit()
  conn.close()
- For SQLAlchemy example:
  session.add(Student(name=name, major=major, gpa=gpa))
  session.commit()
- For the index demo, remember indexes speed up reads but make writes (INSERT/UPDATE/DELETE) slightly slower.

Common gotchas
-------------
- "database is locked": another thread/process is using the DB. Close other connections or restart server.
- JSON body parsing errors: ensure Content-Type: application/json when posting.
- On Windows PowerShell, use the provided client_examples.ps1 to avoid curl/platform quirks.

Timeboxing suggestions (for instructors)
---------------------------------------
- 5 min: Read prompt & plan
- 20 min: Implement core tasks (1–3)
- 5 min: Run tests and prepare a short demo
- 10–15 min: Bonus / improvements (if time remains)

Submission & demo
-----------------
- Each team should run their server, perform:
  1) POST /students -> show created response
  2) GET /students?gpa_min=3.6 -> show JSON result including inserted student
  3) (Bonus) Run measure_perf.py and show speedup after index
- Present results in 3–5 minutes per team.

Resources
---------
- SQLAlchemy quickstart: https://docs.sqlalchemy.org
- SQLite docs: https://sqlite.org/docs.html
- pwn.college (Computing 101 / Building a Web Server) — conceptual reference

Good luck — and remember: focus on safe inserts (parameterized/ORM), clear schema design, and being able to explain your changes briefly during the demo.
