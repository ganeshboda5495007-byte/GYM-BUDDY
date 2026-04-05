import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection


def create_user(
    username,
    email,
    password,
    full_name=None,
    age=None,
    gender=None,
    diet_type="non-vegetarian",
    is_admin=0,
):
    conn = get_db_connection()
    cursor = conn.cursor()

    password_hash = generate_password_hash(password)

    try:
        cursor.execute(
            """INSERT INTO users (username, email, password_hash, full_name, age, gender, diet_type, is_admin)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                username,
                email,
                password_hash,
                full_name,
                age,
                gender,
                diet_type,
                is_admin,
            ),
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {"success": True, "user_id": user_id}
    except sqlite3.IntegrityError:
        conn.close()
        return {"success": False, "error": "Username or email already exists"}


def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user["password_hash"], password):
        return dict(user)
    return None


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, email, full_name, age, gender, height, weight, diet_type, goal, is_admin FROM users WHERE id = ?",
        (user_id,),
    )
    user = cursor.fetchone()
    conn.close()

    return dict(user) if user else None


def update_user_profile(user_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()

    fields = []
    values = []

    for key in ["full_name", "age", "gender", "height", "weight", "diet_type", "goal"]:
        if key in data and data[key] is not None:
            fields.append(f"{key} = ?")
            values.append(data[key])

    if not fields:
        return False

    values.append(user_id)

    cursor.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()
    conn.close()
    return True


def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, email, full_name, is_admin, created_at FROM users"
    )
    users = cursor.fetchall()
    conn.close()

    return [dict(user) for user in users]


def create_admin_user():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if cursor.fetchone():
        conn.close()
        return {"success": True, "message": "Admin already exists"}

    password_hash = generate_password_hash("admin123")

    try:
        cursor.execute(
            """INSERT INTO users (username, email, password_hash, full_name, is_admin)
               VALUES (?, ?, ?, ?, ?)""",
            ("admin", "admin@ai-gym.com", password_hash, "Owner / Admin", 1),
        )
        conn.commit()
        conn.close()
        return {
            "success": True,
            "message": "Admin created - Username: admin, Password: admin123",
        }
    except Exception as e:
        conn.close()
        return {"success": False, "error": str(e)}
