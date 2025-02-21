## creating database and app to manage all my games
from DatabaseCode import insert_game

conn = sqlite3.connect("games.db")
cursor = conn.cursor()

cursor.execute("""
SELECT Games.title, Platforms.name AS platform, Stores.name AS store, Games.completion_date 
FROM Games
JOIN Platforms ON Games.platform_id = Platforms.id
JOIN Stores ON Games.store_id = Stores.id
""")
if __name__ == "__main__":
    games = cursor.fetchall()
        for game in games:
            print(game)

    conn.close()
