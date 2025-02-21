import sqlite3
import os

DB_NAME = "games.db"

def create_database():
    """Creates the database and tables if the database file does not exist."""
    if os.path.exists(DB_NAME):
        print("Database already exists. Skipping creation.")
        return  # Exit early if database exists

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Platforms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Stores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        platform_id INTEGER,
        store_id INTEGER,
        completion_date TEXT,
        FOREIGN KEY (platform_id) REFERENCES Platforms(id),
        FOREIGN KEY (store_id) REFERENCES Stores(id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database created successfully.")

# Run setup when script is executed directly
if __name__ == "__main__":
    create_database()
