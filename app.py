import hashlib
import sqlite3
from flask import Flask, request, render_template, jsonify
from database import init_db

app = Flask(__name__)

# ---- NORMALIZE: fixes false positives (e.g. "John " vs "john") ----
def normalize(value):
    return value.strip().lower()

# ---- HASH: creates a unique fingerprint for each record ----
def generate_hash(name, email):
    combined = normalize(name) + normalize(email)
    return hashlib.sha256(combined.encode()).hexdigest()

# ---- CLASSIFY: checks if data is redundant or unique ----
def add_record(name, email):
    data_hash = generate_hash(name, email)
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # Check for duplicate
    cursor.execute("SELECT * FROM records WHERE data_hash = ?", (data_hash,))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return "REDUNDANT"  # duplicate found — do not insert

    # Insert unique record
    cursor.execute(
        "INSERT INTO records (name, email, data_hash) VALUES (?, ?, ?)",
        (name, email, data_hash)
    )
    conn.commit()
    conn.close()
    return "INSERTED"  # unique data — successfully added

# ---- ROUTES ----
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return jsonify({"status": "ERROR", "message": "Fields cannot be empty"})

    result = add_record(name, email)
    return jsonify({"status": result})

@app.route("/records", methods=["GET"])
def view_records():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM records")
    rows = cursor.fetchall()
    conn.close()
    return jsonify({"records": rows})

# ---- START APP ----
if __name__ == "__main__":
    init_db()
    app.run(debug=True)