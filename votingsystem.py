from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, "voting.db")

parties = ["NOTA", "Party A", "Party B", "Party C", "Party D"]

def get_db_connection():
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def determine_winner(totals):
    if not totals:
        return {
            "parties": [],
            "votes": 0,
            "is_tie": False,
        }

    highest = max(totals.values())
    if highest == 0:
        return {
            "parties": [],
            "votes": 0,
            "is_tie": False,
        }

    winners = [party for party, count in totals.items() if count == highest]
    return {
        "parties": winners,
        "votes": highest,
        "is_tie": len(winners) > 1,
    }

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_code TEXT UNIQUE NOT NULL,
            age INTEGER NOT NULL,
            party TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

init_db()

def reset_votes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM votes")
    conn.commit()
    conn.close()

@app.route("/")
def index():
    reset_votes()
    return render_template("index.html", parties=parties)

@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json() or {}
    user_code = str(data.get("user_code", "")).strip()
    age_value = data.get("age")
    party = data.get("party")

    if not user_code:
        return jsonify({"status": "error", "message": "Unique code is required."}), 400

    try:
        age = int(age_value)
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Age must be a number."}), 400

    if age < 18:
        return jsonify({"status": "error", "message": "You must be at least 18 years old to vote."}), 400
    if party not in parties:
        return jsonify({"status": "error", "message": "Please select a valid party."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    try:
        cursor.execute(
            "INSERT INTO votes (user_code, age, party, created_at) VALUES (?, ?, ?, ?)",
            (user_code, age, party, created_at),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        return jsonify({"status": "error", "message": "This code has already voted."}), 409

    conn.close()
    return jsonify({"status": "success", "message": "Vote cast successfully."})

@app.route("/results")
def results():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, age, party, created_at FROM votes")
    rows = cursor.fetchall()
    conn.close()

    totals = {party: 0 for party in parties}
    details = {party: [] for party in parties}

    for row in rows:
        totals[row[2]] += 1
        details[row[2]].append({
            "user_code": row[0],
            "age": row[1],
            "created_at": row[3],
        })

    winner = determine_winner(totals)
    return jsonify({
        "totals": totals,
        "details": details,
        "total_votes": len(rows),
        "winner": winner,
    })

@app.route("/admin")
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_code, age, party, created_at FROM votes ORDER BY created_at DESC LIMIT 100")
    votes = cursor.fetchall()
    totals = {}
    for party in parties:
        cursor.execute("SELECT COUNT(*) FROM votes WHERE party = ?", (party,))
        totals[party] = cursor.fetchone()[0]
    conn.close()

    winner = determine_winner(totals)
    return render_template("admin.html", votes=votes, totals=totals, winner=winner)

if __name__ == "__main__":
    app.run(debug=True)
