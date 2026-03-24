from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
import sys

# Fix import path
sys.path.append('../')

from model import train_model
from data.generator import generate_data

app = Flask(__name__)

# =======================
# ML MODEL (Optional now)
# =======================
df = generate_data()
model = train_model(df)

# =======================
# SMART PREDICTION LOGIC 🔥
# =======================
def predict_delay(orders, workers, safety, productivity):

    load_per_worker = orders / workers

    risk_score = 0

    if load_per_worker > 30:
        risk_score += 2
    elif load_per_worker > 20:
        risk_score += 1

    # ✅ FIXED FOR 0–5 SCALE
    if safety <= 2:
        risk_score += 1

    if productivity < 60:
        risk_score += 1

    if risk_score >= 2:
        return 1
    else:
        return 0

# =======================
# DATABASE
# =======================
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

# LOGS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orders INT,
    workers INT,
    safety INT,
    productivity INT,
    prediction INT
)
""")

# DEFAULT USER
cursor.execute("""
INSERT OR IGNORE INTO users (id, username, password, role)
VALUES (1, 'admin', 'admin', 'manager')
""")

conn.commit()

# =======================
# LOGIN API
# =======================
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    ).fetchone()

    if user:
        return jsonify({
            "status": "success",
            "role": user[3]
        })
    else:
        return jsonify({"status": "fail"})


# =======================
# PREDICT API
# =======================
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    orders = data["orders"]
    workers = data["workers"]
    safety = data["safety"]
    productivity = data["productivity"]

    # 🔥 Use SMART LOGIC instead of ML
    prediction = predict_delay(orders, workers, safety, productivity)

    # Save to DB
    cursor.execute("""
    INSERT INTO logs (orders, workers, safety, productivity, prediction)
    VALUES (?, ?, ?, ?, ?)
    """, (
        orders,
        workers,
        safety,
        productivity,
        int(prediction)
    ))
    conn.commit()

    # 🔥 Alert system
    if prediction == 1:
        alert = "🚨 DELAY RISK"
    else:
        alert = "✅ SAFE"

    return jsonify({
        "prediction": int(prediction),
        "alert": alert
    })


# =======================
# LOGS API
# =======================
@app.route("/logs", methods=["GET"])
def logs():
    df = pd.read_sql_query("SELECT * FROM logs", conn)
    return df.to_json(orient="records")


# =======================
# RUN SERVER
# =======================
if __name__ == "__main__":
    app.run(debug=True)