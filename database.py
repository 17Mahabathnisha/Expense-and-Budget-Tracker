import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "data" / "expenses.db"


def get_connection():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_FILE)


def create_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            payment_mode TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_expense(username, date, description, amount, category, payment_mode):
    connection = get_connection()

    connection.execute("""
        INSERT INTO expenses
        (username, date, description, amount, category, payment_mode)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, date, description, amount, category, payment_mode))

    connection.commit()
    connection.close()
def get_saved_expenses(username):
    connection = get_connection()
    
    cursor = connection.execute("""
        SELECT date, description, amount, category, payment_mode
        FROM expenses
        WHERE username = ?
    """, (username,))

    rows = cursor.fetchall()
    connection.close()

    expenses = []

    for row in rows:
        expenses.append({
            "Date": row[0],
            "Description": row[1],
            "Amount": row[2],
            "Category": row[3],
            "Payment_mode": row[4]
        })

    return expenses

def create_users_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()
def register_user(full_name, username, email, password):
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO users (full_name, username, email, password)
            VALUES (?, ?, ?, ?)
        """, (full_name, username, email, password))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def get_user(username):
    connection = get_connection()

    cursor = connection.execute("""
        SELECT id, full_name, username, email, password
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    connection.close()

    return user

def check_registered_user(username):
    user = get_user(username)

    if user:
        print("User found:", user[2])
    else:
        print("User not found")
        
if __name__ == "__main__":
    create_table()
    create_users_table()
    print("Database tables created successfully!")