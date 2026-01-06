"""
Database utility functions for SQLite operations.
"""

import sqlite3
from pathlib import Path
from src.config import DATABASE_PATH


def get_connection():
    """
    Create and return a SQLite database connection.
    """
    Path("output").mkdir(exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """
    Initialize database by executing schema.sql.
    """
    conn = get_connection()
    cursor = conn.cursor()

    with open("schema.sql", "r") as f:
        cursor.executescript(f.read())

    conn.commit()
    return conn
