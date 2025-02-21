## creating database and app to manage all my games
from db_operations import insert_game, get_all_games
from db_setup import create_database

# Ensure database is set up before running
create_database()

# Example data insertion
insert_game("Half-Life 2", "PC", "Steam", "2022-03-15")
insert_game("Bloodborne", "PlayStation", "PS4", "2021-08-10")

# Fetch and display all games
games = get_all_games()
for game in games:
    print(f"ID: {game[0]}, Title: {game[1]}, Platform: {game[2]}, Store: {game[3]}, Completed on: {game[4]}")
