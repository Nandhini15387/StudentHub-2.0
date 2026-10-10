from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, send_file
)
import sqlite3
import csv
import io

app = Flask(__name__)
app.secret_key = "student-management-dev-key"

DATABASE = "students.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_number TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                year INTEGER NOT NULL,
                marks REAL NOT NULL
            )
        """)


@app.route("/")
def index():
    search = request.args.get("search", "").strip()
    department = request.args.get("department", "").strip()
    sort_by = request.args.get("sort", "newest")

    sort_options = {
        "newest": "id DESC",
        "name": "name COLLATE NOCASE ASC",
        "marks_high": "marks DESC",
        "marks_low": "marks ASC",
        "roll": "roll_number ASC",
        "year": "year ASC"
    }

    order_by = sort_options.get(sort_by, "id DESC")

    query = """
        SELECT * FROM students
        WHERE (name LIKE ? OR roll_number LIKE ?)
    """
    params = [f"%{search}%", f"%{search}%"]

    if department:
        query += " AND department = ?"
        params.append(department)

    query += f" ORDER BY {order_by}"

    with get_db_connection() as conn:
        students = conn.execute(query, params).fetchall()

        total = conn.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        average = conn.execute(
            "SELECT AVG(marks) FROM students"
        ).fetchone()[0]

        top_student = conn.execute("""
            SELECT name, roll_number, marks
            FROM students
            ORDER BY marks DESC, name ASC
            LIMIT 1
        """).fetchone()

        departments = conn.execute("""
            SELECT DISTINCT department FROM students
            ORDER BY department COLLATE NOCASE
        """).fetchall()

        department_stats = conn.execute("""
            SELECT department, COUNT(*) AS count,
                   ROUND(AVG(marks), 2) AS average_marks
            FROM students
            GROUP BY department
            ORDER BY department
        """).fetchall()

    return render_template(
        "index.html",
        students=students,
        total=total,
        search=search,
        average_marks=round(average, 2) if average is not None else None,
        top_student=top_student,
        departments=departments,
        department_stats=department_stats,
        selected_department=department,
        sort_by=sort_by
    )


@app.route("/add", methods=["POST"])
def add_student():
    roll_number = request.form.get("roll_number", "").strip()
    name = request.form.get("name", "").strip()
    department = request.form.get("department", "").strip()

    try:
        year = int(request.form.get("year", ""))
        marks = float(request.form.get("marks", ""))

        if not 1 <= year <= 4 or not 0 <= marks <= 100:
            raise ValueError
    except ValueError:
        flash("Enter a valid year (1–4) and marks (0–100).", "error")
        return redirect(url_for("index"))

    if not roll_number or not name or not department:
        flash("Please fill in all fields.", "error")
        return redirect(url_for("index"))

    try:
        with get_db_connection() as conn:
            conn.execute("""
                INSERT INTO students
                (roll_number, name, department, year, marks)
                VALUES (?, ?, ?, ?, ?)
            """, (roll_number, name, department, year, marks))
        flash("Student added successfully!", "success")
    except sqlite3.IntegrityError:
        flash("That roll number already exists.", "error")

    return redirect(url_for("index"))


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    with get_db_connection() as conn:
        student = conn.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        ).fetchone()

        if student is None:
            flash("Student not found.", "error")
            return redirect(url_for("index"))

        if request.method == "POST":
            roll_number = request.form.get("roll_number", "").strip()
            name = request.form.get("name", "").strip()
            department = request.form.get("department", "").strip()

            try:
                year = int(request.form.get("year", ""))
                marks = float(request.form.get("marks", ""))

                if (
                    not roll_number or not name or not department
                    or not 1 <= year <= 4
                    or not 0 <= marks <= 100
                ):
                    raise ValueError
            except ValueError:
                flash("Check all fields and enter valid values.", "error")
                return redirect(
                    url_for("edit_student", student_id=student_id)
                )

            try:
                conn.execute("""
                    UPDATE students
                    SET roll_number = ?, name = ?, department = ?,
                        year = ?, marks = ?
                    WHERE id = ?
                """, (
                    roll_number, name, department,
                    year, marks, student_id
                ))
                flash("Student updated successfully!", "success")
            except sqlite3.IntegrityError:
                flash("That roll number is already in use.", "error")
                return redirect(
                    url_for("edit_student", student_id=student_id)
                )

            return redirect(url_for("index"))

    return render_template("edit.html", student=student)


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db_connection() as conn:
        conn.execute(
            "DELETE FROM students WHERE id = ?", (student_id,)
        )

    flash("Student deleted.", "success")
    return redirect(url_for("index"))


@app.route("/export")
def export_students():
    with get_db_connection() as conn:
        students = conn.execute("""
            SELECT roll_number, name, department, year, marks
            FROM students
            ORDER BY roll_number
        """).fetchall()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Roll Number", "Student Name",
        "Department", "Year", "Marks"
    ])

    for student in students:
        writer.writerow([
            student["roll_number"],
            student["name"],
            student["department"],
            student["year"],
            student["marks"]
        ])

    file_data = io.BytesIO(
        output.getvalue().encode("utf-8-sig")
    )
    file_data.seek(0)

    return send_file(
        file_data,
        mimetype="text/csv",
        as_attachment=True,
        download_name="student_records.csv"
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)