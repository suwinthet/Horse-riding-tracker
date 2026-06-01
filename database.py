import sqlite3
import os

DATABASE_URL = "app.db"

def get_db():
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
    finally:
        conn.close()

def init_db():
    if not os.path.exists(DATABASE_URL):
        conn = sqlite3.connect(DATABASE_URL)
        with open("DB_commands.sql", "r") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
