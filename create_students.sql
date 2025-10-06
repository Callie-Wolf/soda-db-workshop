PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    major TEXT,
    gpa REAL
);

INSERT INTO Students (name, major, gpa) VALUES
 ('Alex Kim', 'Computer Science', 3.9),
 ('Priya Patel', 'Software Engineering', 3.6),
 ('John Doe', 'Data Science', 3.8),
 ('Maria Lopez', 'Computer Systems', 3.5);