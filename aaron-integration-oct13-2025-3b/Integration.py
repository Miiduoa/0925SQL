import sqlite3
from pathlib import Path
import sys


DB_PATH = Path(__file__).with_name("Student.db")


def ensure_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS DB_student (
            db_student_id TEXT PRIMARY KEY,
            db_student_name TEXT
        )
        """
    )
    con.commit()
    return con


def list_students(con):
    cur = con.cursor()
    cur.execute("SELECT db_student_id, db_student_name FROM DB_student ORDER BY db_student_id")
    rows = cur.fetchall()
    if not rows:
        print("No students yet. Use 'seed' or 'add <id> <name>'.")
    else:
        for sid, name in rows:
            print(f"{sid}\t{name}")


def add_student(con, sid: str, name: str):
    cur = con.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO DB_student (db_student_id, db_student_name) VALUES (?, ?)",
        (sid, name),
    )
    con.commit()
    print(f"Saved: {sid} -> {name}")


def delete_student(con, sid: str):
    cur = con.cursor()
    cur.execute("DELETE FROM DB_student WHERE db_student_id = ?", (sid,))
    con.commit()
    print(f"Deleted: {sid}")


def seed(con):
    data = [
        ("S001", "Aaron"),
        ("S002", "Bella"),
        ("S003", "Chris"),
    ]
    cur = con.cursor()
    cur.executemany(
        "INSERT OR IGNORE INTO DB_student (db_student_id, db_student_name) VALUES (?, ?)",
        data,
    )
    con.commit()
    print("Seeded sample students.")


def main(argv):
    con = ensure_db()
    try:
        if not argv or argv[0] in {"list", "ls"}:
            list_students(con)
        elif argv[0] == "seed":
            seed(con)
        elif argv[0] == "add" and len(argv) >= 3:
            add_student(con, argv[1], " ".join(argv[2:]))
        elif argv[0] == "del" and len(argv) == 2:
            delete_student(con, argv[1])
        else:
            print(
                "Usage: python Integration.py [list|seed|add <id> <name>|del <id>]"
            )
    finally:
        con.close()


if __name__ == "__main__":
    main(sys.argv[1:])

