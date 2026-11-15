from flask import Flask, jsonify, render_template, request, redirect, url_for
from contextlib import contextmanager
import json
import os
import sqlite3

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "backend", "data.json")

# SQLite is a file inside this process, not a server. Where the file lives decides
# whether data survives: EC2 -> /var/lib/todo (EBS), ECS -> /data (EFS mount).
DB_PATH = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "data", "app.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS submissions (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS todo_items (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name        TEXT NOT NULL,
    item_description TEXT NOT NULL,
    created_at       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


@contextmanager
def get_db():
    # One short-lived connection per call: sqlite3 connections must not be shared
    # across the dev server's threads. Commits on success, rolls back on error,
    # always closes. Rollback journal (not WAL) because WAL does not work on
    # network filesystems such as EFS.
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as conn:
        conn.executescript(SCHEMA)


init_db()


@app.route("/health", methods=["GET"])
def health():
    # Load balancer / bootstrap health check.
    return jsonify({"status": "ok"})


@app.route("/api", methods=["GET"])
def api_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        try:
            if not name or not email:
                raise ValueError("Name and email are required")

            with get_db() as conn:
                conn.execute(
                    "INSERT INTO submissions (name, email) VALUES (?, ?)", (name, email)
                )
            return redirect(url_for("success"))
        except (ValueError, sqlite3.Error) as e:
            error = str(e)

    return render_template("form.html", error=error)


@app.route("/success", methods=["GET"])
def success():
    return render_template("success.html")


@app.route("/submissions", methods=["GET"])
def submissions():
    error = None
    records = []

    try:
        with get_db() as conn:
            records = conn.execute(
                "SELECT name, email FROM submissions ORDER BY id"
            ).fetchall()
    except sqlite3.Error as e:
        error = str(e)

    return render_template("submissions.html", records=records, error=error)


@app.route("/todoitems", methods=["GET"])
def todo_items():
    # Read-back page: proves frontend -> backend -> SQLite writes landed.
    error = None
    records = []

    try:
        with get_db() as conn:
            records = conn.execute(
                "SELECT id, item_name, item_description, created_at"
                " FROM todo_items ORDER BY id DESC"
            ).fetchall()
    except sqlite3.Error as e:
        error = str(e)

    return render_template("todoitems.html", records=records, error=error)


@app.route("/todo", methods=["GET", "POST"])
def todo():
    # Submission is intentionally a no-op for now.
    return render_template("todo.html")


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = (request.form.get("itemName") or "").strip()
    item_description = (request.form.get("itemDescription") or "").strip()

    if request.is_json:
        payload = request.get_json(silent=True) or {}
        item_name = (payload.get("itemName") or item_name).strip()
        item_description = (payload.get("itemDescription") or item_description).strip()

    if not item_name or not item_description:
        return jsonify({"error": "itemName and itemDescription are required"}), 400

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO todo_items (item_name, item_description) VALUES (?, ?)",
                (item_name, item_description),
            )
        return jsonify({"message": "Todo item submitted successfully"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    # Never default to debug: the Werkzeug debugger allows code execution
    # and this server is reachable from the internet once deployed.
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
