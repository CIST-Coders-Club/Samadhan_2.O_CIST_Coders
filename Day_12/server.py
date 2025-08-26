from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_NAME = "students.db"


# --------- DB SETUP ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')

    # Todos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()


init_db()


# --------- BASIC ROUTES ----------
@app.route("/")
def home():
    return "Welcome to the Home Page of samadhan 2.0 (Students + To-Do API)"


@app.route("/hello")
def hello():
    return "Hello, World!"


# --------- STUDENT CRUD ----------
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()
    name = data.get("name")
    course = data.get("course")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, course) VALUES (?, ?)", (name, course))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": new_id, "name": name, "course": course}), 201


@app.route("/students", methods=["GET"])
def get_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    students = [{"id": row[0], "name": row[1], "course": row[2]} for row in rows]
    return jsonify(students)


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({"id": row[0], "name": row[1], "course": row[2]})
    else:
        return jsonify({"error": "Student not found"}), 404


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json()
    name = data.get("name")
    course = data.get("course")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name = ?, course = ? WHERE id = ?", (name, course, student_id))
    conn.commit()
    conn.close()

    return jsonify({"id": student_id, "name": name, "course": course})


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Student {student_id} deleted"})


# --------- TODO CRUD ----------
@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    title = data.get("title")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (title, completed) VALUES (?, ?)", (title, False))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": new_id, "title": title, "completed": False}), 201


@app.route("/todos", methods=["GET"])
def get_todos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()
    conn.close()

    todos = [{"id": row[0], "title": row[1], "completed": bool(row[2])} for row in rows]
    return jsonify(todos)


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos WHERE id=?", (todo_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({"id": row[0], "title": row[1], "completed": bool(row[2])})
    return jsonify({"error": "Todo not found"}), 404


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    title = data.get("title")
    completed = data.get("completed")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET title=?, completed=? WHERE id=?", (title, completed, todo_id))
    conn.commit()
    conn.close()

    return jsonify({"id": todo_id, "title": title, "completed": completed})


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id=?", (todo_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Todo {todo_id} deleted"})


if __name__ == "__main__":
    app.run(debug=True)
