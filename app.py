from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DATABASE = "data/attendance.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs("data", exist_ok=True)

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            attendance TEXT NOT NULL DEFAULT 'Absent'
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    student_id = request.form["student_id"].strip()
    name = request.form["name"].strip()

    if student_id and name:
        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO students (student_id, name) VALUES (?, ?)",
                (student_id, name)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            pass

        finally:
            conn.close()

    return redirect("/")


@app.route("/attendance/<int:student_id>/<status>")
def mark_attendance(student_id, status):
    if status not in ["Present", "Absent"]:
        return redirect("/")

    conn = get_db()

    conn.execute(
        "UPDATE students SET attendance = ? WHERE id = ?",
        (status, student_id)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)