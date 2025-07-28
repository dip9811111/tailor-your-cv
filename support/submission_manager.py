import sqlite3
from datetime import datetime


DB_PATH = "cv_submissions.db"


def initialize_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                submission_date TEXT NOT NULL,
                pdf BLOB NOT NULL
            )
        """)
        conn.commit()


def save_submission(company, position, pdf_path):
    with sqlite3.connect(DB_PATH) as conn:
        with open(pdf_path, "rb") as f:
            pdf_blob = f.read()

        conn.execute("""
            INSERT INTO submissions (company, position, submission_date, pdf)
            VALUES (?, ?, ?, ?)
        """, (company, position, datetime.now().isoformat(), pdf_blob))
        conn.commit()


def get_all_submissions():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT id, company, position, submission_date FROM submissions").fetchall()


def get_pdf_by_id(submission_id):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("SELECT pdf FROM submissions WHERE id = ?", (submission_id,)).fetchone()
        return result[0] if result else None
