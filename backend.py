from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # Allow requests from your frontend

# --- MySQL Connection ---
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",       # Change if your MySQL is on another host
            user="root",            # Replace with your MySQL username
            password="databaseCode1",# Replace with your MySQL password
            database="easyretain"   # Your database name
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# --- Registration Route ---
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("Received data:", data)  # Log incoming data

    if not data:
        return jsonify({"success": False, "message": "No data received"})

    conn = create_connection()
    if not conn:
        return jsonify({"success": False, "message": "Database connection failed"})

    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO users (first_name, last_name, age, gender, job, email, phone)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data.get('first_name'),
            data.get('last_name'),
            data.get('age'),
            data.get('gender'),
            data.get('job'),
            data.get('email'),
            data.get('phone')
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("Data inserted successfully")
        return jsonify({"success": True, "message": "Registration successful!"})
    except Error as e:
        print(f"Error inserting data: {e}")
        return jsonify({"success": False, "message": str(e)})

# --- Run the Flask App ---
if __name__ == '__main__':
    app.run(debug=True)
