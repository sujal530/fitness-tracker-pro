import sqlite3

def connect_db():
    conn = sqlite3.connect("database.db")
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # fitness data table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fitness_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        steps INTEGER,
        calories INTEGER,
        water REAL,
        date TEXT
    )
    """)

    # goals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        step_goal INTEGER
    )
    """)

    conn.commit()
    conn.close()