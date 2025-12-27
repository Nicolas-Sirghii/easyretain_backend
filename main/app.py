from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("databaseCode1", ""),
    "database": os.getenv("DB_NAME", "easyretain2")
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (first_name, last_name, age, job) VALUES (%s,%s,%s,%s)",
        (data["first_name"], data["last_name"], data["age"], data["job"])
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Employee added"}), 201

if __name__ == "__main__":
    app.run(debug=True)
