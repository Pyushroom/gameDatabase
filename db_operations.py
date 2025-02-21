import sqlite3

def normalize_name(name):
    """Standardizes platform and store names (e.g., 'pc', 'Pc' → 'PC')."""
    name = name.strip().lower()  # Remove spaces and convert to lowercase
    name_map = {
        "pc": "PC",
        "steam": "Steam",
        "epic": "Epic Games",
        "ps3": "PS3",
        "ps4": "PS4",
        "playstation": "PlayStation",
        "xbox": "Xbox",
        "xbox one": "Xbox One",
        "xbox 360": "Xbox 360",
    }
    return name_map.get(name, name.capitalize())  # Default: capitalize first letter

def insert_game(title, platform, store, completion_date):
    """Inserts a game into the database, ensuring consistent platform/store names."""
    conn = sqlite3.connect("games.db")
    cursor = conn.cursor()

    # Normalize platform and store names
    platform = normalize_name(platform)
    store = normalize_name(store)

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
