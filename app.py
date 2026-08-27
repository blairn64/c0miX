from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, abort, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.getenv("COMIX_DB", BASE_DIR / "data" / "comix.db"))

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_db() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS series (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                publisher TEXT,
                year_start INTEGER,
                year_end INTEGER
            );

            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                series_id INTEGER NOT NULL,
                issue_number REAL NOT NULL,
                title TEXT,
                cover_date TEXT,
                variant_key TEXT NOT NULL DEFAULT 'standard',
                is_reprint INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (series_id) REFERENCES series(id) ON DELETE CASCADE,
                UNIQUE(series_id, issue_number, variant_key)
            );

            CREATE TABLE IF NOT EXISTS collection (
                issue_id INTEGER PRIMARY KEY,
                owned INTEGER NOT NULL DEFAULT 0,
                read INTEGER NOT NULL DEFAULT 0,
                notes TEXT NOT NULL DEFAULT '',
                FOREIGN KEY (issue_id) REFERENCES issues(id) ON DELETE CASCADE
            );
            """
        )


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(row)


@app.before_request
def ensure_database() -> None:
    init_db()


@app.get("/")
def index():
    with get_db() as db:
        series = db.execute(
            "SELECT id, name, publisher, year_start, year_end FROM series ORDER BY name"
        ).fetchall()
    return render_template("index.html", series=series)


@app.get("/series/<int:series_id>")
def series_detail(series_id: int):
    with get_db() as db:
        series = db.execute("SELECT * FROM series WHERE id = ?", (series_id,)).fetchone()
        if series is None:
            abort(404)
        issues = db.execute(
            """
            SELECT i.*, COALESCE(c.owned, 0) AS owned, COALESCE(c.read, 0) AS read,
                   COALESCE(c.notes, '') AS notes
            FROM issues i
            LEFT JOIN collection c ON c.issue_id = i.id
            WHERE i.series_id = ?
            ORDER BY i.issue_number, i.variant_key
            """,
            (series_id,),
        ).fetchall()
    return render_template("series.html", series=series, issues=issues)


@app.post("/series")
def create_series():
    payload = request.get_json(silent=True) or request.form
    name = str(payload.get("name", "")).strip()
    if not name:
        return jsonify({"error": "name is required"}), 400

    with get_db() as db:
        try:
            cursor = db.execute(
                "INSERT INTO series(name, publisher, year_start, year_end) VALUES (?, ?, ?, ?)",
                (
                    name,
                    payload.get("publisher"),
                    payload.get("year_start") or None,
                    payload.get("year_end") or None,
                ),
            )
        except sqlite3.IntegrityError:
            return jsonify({"error": "series already exists"}), 409
    return jsonify({"id": cursor.lastrowid, "name": name}), 201


@app.post("/series/<int:series_id>/issues")
def create_issue(series_id: int):
    payload = request.get_json(silent=True) or request.form
    with get_db() as db:
        if db.execute("SELECT 1 FROM series WHERE id = ?", (series_id,)).fetchone() is None:
            abort(404)
        try:
            cursor = db.execute(
                """
                INSERT INTO issues(series_id, issue_number, title, cover_date, variant_key, is_reprint)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    series_id,
                    payload.get("issue_number"),
                    payload.get("title"),
                    payload.get("cover_date"),
                    payload.get("variant_key", "standard"),
                    int(bool(payload.get("is_reprint", False))),
                ),
            )
        except (sqlite3.IntegrityError, TypeError, ValueError):
            return jsonify({"error": "invalid or duplicate issue"}), 400
    return jsonify({"id": cursor.lastrowid}), 201


@app.post("/issues/<int:issue_id>/collection")
def update_collection(issue_id: int):
    payload = request.get_json(silent=True) or request.form
    try:
        owned = int(bool(payload.get("owned", False)))
        read = int(bool(payload.get("read", False)))
    except (TypeError, ValueError):
        return jsonify({"error": "owned/read must be boolean-like values"}), 400

    with get_db() as db:
        if db.execute("SELECT 1 FROM issues WHERE id = ?", (issue_id,)).fetchone() is None:
            abort(404)
        db.execute(
            """
            INSERT INTO collection(issue_id, owned, read, notes)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(issue_id) DO UPDATE SET
                owned = excluded.owned,
                read = excluded.read,
                notes = excluded.notes
            """,
            (issue_id, owned, read, str(payload.get("notes", ""))),
        )
    return jsonify({"issue_id": issue_id, "owned": owned, "read": read})


@app.get("/api/series")
def api_series():
    with get_db() as db:
        rows = db.execute(
            """
            SELECT s.id, s.name, s.publisher, s.year_start, s.year_end,
                   COUNT(i.id) AS issue_count,
                   COALESCE(SUM(CASE WHEN c.owned = 1 THEN 1 ELSE 0 END), 0) AS owned_count,
                   COALESCE(SUM(CASE WHEN c.read = 1 THEN 1 ELSE 0 END), 0) AS read_count
            FROM series s
            LEFT JOIN issues i ON i.series_id = s.id
            LEFT JOIN collection c ON c.issue_id = i.id
            GROUP BY s.id
            ORDER BY s.name
            """
        ).fetchall()
    return jsonify([row_to_dict(row) for row in rows])


@app.get("/api/series/<int:series_id>/missing")
def api_missing(series_id: int):
    with get_db() as db:
        series = db.execute("SELECT * FROM series WHERE id = ?", (series_id,)).fetchone()
        if series is None:
            abort(404)
        rows = db.execute(
            """
            SELECT i.id, i.issue_number, i.title, i.variant_key
            FROM issues i
            LEFT JOIN collection c ON c.issue_id = i.id
            WHERE i.series_id = ? AND COALESCE(c.owned, 0) = 0 AND i.is_reprint = 0
            ORDER BY i.issue_number, i.variant_key
            """,
            (series_id,),
        ).fetchall()
    return jsonify([row_to_dict(row) for row in rows])


if __name__ == "__main__":
    init_db()
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
