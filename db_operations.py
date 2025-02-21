import sqlite3

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

def get_all_games():
    """Fetch all games from the database."""
    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Games.id, Games.title, Platforms.name, Stores.name, Games.completion_date
        FROM Games
        JOIN Platforms ON Games.platform_id = Platforms.id
        JOIN Stores ON Games.store_id = Stores.id
    """)

    games = cursor.fetchall()
    conn.close()
    return games
