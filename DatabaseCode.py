import sqlite3

# Connect to SQLite (or create database file)
conn = sqlite3.connect("games.db")
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


def insert_game(title, platform, store, completion_date):
    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()

    # Insert platform if it doesn't exist
    cursor.execute("INSERT OR IGNORE INTO Platforms (name) VALUES (?)", (platform,))
    cursor.execute("SELECT id FROM Platforms WHERE name = ?", (platform,))
    platform_id = cursor.fetchone()[0]

    # Insert store if it doesn't exist
    cursor.execute("INSERT OR IGNORE INTO Stores (name) VALUES (?)", (store,))
    cursor.execute("SELECT id FROM Stores WHERE name = ?", (store,))
    store_id = cursor.fetchone()[0]

    # Insert game
    cursor.execute("""
        INSERT INTO Games (title, platform_id, store_id, completion_date) 
        VALUES (?, ?, ?, ?)
    """, (title, platform_id, store_id, completion_date))

    conn.commit()
    conn.close()




