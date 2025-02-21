import tkinter as tk
from tkinter import ttk
from db_operations import get_all_games  # Import function to fetch data from the database

# Function to display data in the Treeview (table)
def display_data():
    # Fetch data from the database
    data = get_all_games()

    # Clear existing data in the Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Insert new data into the table
    for row in data:
        tree.insert("", "end", values=row)

# Set up the main Tkinter window
def create_gui():
    root = tk.Tk()
    root.title("Game Database")

    # Set up Treeview (Table) widget
    columns = ("Title", "Platform", "Store", "Completion Date")
    global tree  # Make the treeview accessible to other functions
    tree = ttk.Treeview(root, columns=columns, show="headings")

    # Define columns
    for col in columns:
        tree.heading(col, text=col)

    # Place the Treeview on the window
    tree.pack(pady=20)

    # Add a button to fetch and display data
    button = tk.Button(root, text="Show Data", command=display_data)
    button.pack(pady=10)

    # Start the Tkinter loop
    root.mainloop()
