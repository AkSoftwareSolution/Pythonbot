from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import mysql.connector
from decimal import Decimal

app = FastAPI(title="FastAPI MySQL CRUD", version="1.0")

# ---------------- MySQL Helper ----------------
def get_mysql_connection():
    """Create a new MySQL connection"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root1234",
        database="startersql"
    )

def serialize_rows(rows: List[dict]):
    """Convert Decimal, date, datetime to JSON serializable"""
    serialized = []
    for row in rows:
        new_row = {}
        for k, v in row.items():
            if isinstance(v, Decimal):
                new_row[k] = float(v)
            elif hasattr(v, 'isoformat'):  # date/datetime
                new_row[k] = v.isoformat()
            else:
                new_row[k] = v
        serialized.append(new_row)
    return serialized

# ---------------- Routes ----------------

@app.get("/")
def get_all_users():
    """Get all users"""
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return JSONResponse(content=serialize_rows(rows))
    except mysql.connector.Error as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/users/{user_id}")
def get_single_user(user_id: int):
    """Get single user by ID"""
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="User Not Found")
        return JSONResponse(content=serialize_rows([row])[0])
    except mysql.connector.Error as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/users/")
def create_user(name: str, email: str, gender: str, salary: float = 0.0):
    """Create a new user"""
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO users (name, email, gender, salary) VALUES (%s, %s, %s, %s)",
            (name, email, gender, salary)
        )
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE id=%s", (cursor.lastrowid,))
        new_user = cursor.fetchone()
        cursor.close()
        conn.close()
        return JSONResponse(content=serialize_rows([new_user])[0])
    except mysql.connector.Error as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, email: str, gender: str, salary: float = 0.0):
    """Update existing user"""
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        existing_user = cursor.fetchone()
        if not existing_user:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="User Not Found")

        cursor.execute(
            "UPDATE users SET name=%s, email=%s, gender=%s, salary=%s WHERE id=%s",
            (name, email, gender, salary, user_id)
        )
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        updated_user = cursor.fetchone()
        cursor.close()
        conn.close()
        return JSONResponse(content=serialize_rows([updated_user])[0])
    except mysql.connector.Error as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Delete a user"""
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        existing_user = cursor.fetchone()
        if not existing_user:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="User Not Found")

        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "User deleted successfully"}
    except mysql.connector.Error as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
