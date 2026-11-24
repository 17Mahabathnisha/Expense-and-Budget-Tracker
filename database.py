import os
import psycopg
from dotenv import load_dotenv
from psycopg.errors import UniqueViolation

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not configured.")

    return psycopg.connect(DATABASE_URL)


def create_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id BIGSERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount DOUBLE PRECISION NOT NULL,
                category TEXT NOT NULL,
                payment_mode TEXT NOT NULL
            )
        """)


def create_users_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGSERIAL PRIMARY KEY,
                full_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)


def register_user(full_name, username, email, password):
    try:
        with get_connection() as connection:
            connection.execute("""
                INSERT INTO users
                (full_name, username, email, password)
                VALUES (%s, %s, %s, %s)
            """, (full_name, username, email, password))

        return True

    except UniqueViolation:
        return False


def get_user(username):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT id, full_name, username, email, password
            FROM users
            WHERE username = %s
        """, (username,))

        return cursor.fetchone()


def add_expense(username, date, description, amount, category, payment_mode):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO expenses
            (username, date, description, amount, category, payment_mode)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, date, description, amount, category, payment_mode))


def get_saved_expenses(username):
    with get_connection() as connection:
        cursor = connection.execute("""
            SELECT date, description, amount, category, payment_mode
            FROM expenses
            WHERE username = %s
            ORDER BY id
        """, (username,))

        rows = cursor.fetchall()

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