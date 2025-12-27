from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)

# Enable CORS for your frontend domain only
FRONTEND_DOMAIN = os.getenv("https://easyretain.com/")  # Replace * with your domain in production
CORS(app, origins=[FRONTEND_DOMAIN])

# Database configuration via environment variables
DB_CONFIG = {
    "host": os.getenv("localhost"),
    "user": os.getenv("root"),
    "password": os.getenv("databaseCode1"),
    "database": os.getenv("easyretain2")
}

def get_db_connection():
    """Create and return a new database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        raise

# Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "ok", "db": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "db": "unreachable", "error": str(e)}), 500

# Get all employees
@app.route("/users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users ORDER BY id DESC")
        users = cursor.fetchall()
        conn.close()
        return jsonify(users), 200
    except Exception as e:
        print("Error fetching users:", e)
        return jsonify({"error": str(e)}), 500

# Add a new employee
@app.route("/users", methods=["POST"])
def add_user():
    try:
        data = request.json
        print("Received data:", data)

        # Validate required fields
        required_fields = ["first_name", "last_name", "age", "job"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (first_name, last_name, age, job) VALUES (%s, %s, %s, %s)",
            (data["first_name"], data["last_name"], data["age"], data["job"])
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Employee added"}), 201

    except Exception as e:
        print("Error adding user:", e)
        return jsonify({"error": str(e)}), 500

# Run server (local testing)
if __name__ == "__main__":
    app.run(debug=True)
