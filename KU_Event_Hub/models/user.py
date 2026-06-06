from database import db_connection
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, password):
    conn = db_connection()
    cur = conn.cursor()

    password_hash = generate_password_hash(password)

    cur.execute(
        """
        INSERT INTO users (username, password_hash)
        VALUES (%s, %s)
        ON CONFLICT (username) DO NOTHING
        RETURNING id, username, password_hash
        """,
        (username, password_hash)
    )

    user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return user

def get_user_by_username(username):
    conn = db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, password_hash FROM users WHERE username = %s",
        (username,)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()
    return user

def check_login(username, password):
    user = get_user_by_username(username)

    if user is None:
        return None

    if check_password_hash(user[2], password):
        return user

    return None