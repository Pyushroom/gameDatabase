import tkinter as tk
from tkinter import ttk, messagebox
from db_operations import insert_game


def add_game():
    add_window = tk.Toplevel()
    add_window.title("Add New Game")
    add_window.geometry("300x300")

    tk.Label(add_window, text="Title:").pack(pady=2)
    title_entry = tk.Entry(add_window)
    title_entry.pack(pady=2)

    tk.Label(add_window, text="Platform:").pack(pady=2)
    platform_var = tk.StringVar()
    platforms = ["PC", "Xbox", "PlayStation", "Nintendo"]  # Manually defined platforms
    platform_dropdown = ttk.Combobox(add_window, textvariable=platform_var, values=platforms, state="readonly")
    platform_dropdown.pack(pady=2)

    tk.Label(add_window, text="Store:").pack(pady=2)
    store_var = tk.StringVar()
    store_dropdown = ttk.Combobox(add_window, textvariable=store_var, values=[], state="readonly")
    store_dropdown.pack(pady=2)

    tk.Label(add_window, text="Completion Date (YYYY-MM-DD):").pack(pady=2)
    date_entry = tk.Entry(add_window)
    date_entry.pack(pady=2)

    def update_store_options(event):
        """Update store dropdown options based on selected platform."""
        selected_platform = platform_var.get()
        
        store_options = {
            "PC": ["Steam", "Epic Games", "Ubisoft Connect", "GOG", "Battle.net"],
            "Xbox": ["Xbox 360", "Xbox One", "Xbox Series X|S"],
            "PlayStation": ["PS3", "PS4", "PS5"],
            "Nintendo": ["Nintendo Switch", "Nintendo eShop", "Wii U", "3DS eShop"]
        }

        stores = store_options.get(selected_platform, [])  # Get stores for selected platform
        store_dropdown["values"] = stores  # Update dropdown list
        store_var.set(stores[0] if stores else "")  # Auto-select first option if available

    # Bind platform selection to update store list
    platform_dropdown.bind("<<ComboboxSelected>>", update_store_options)

    def save_game():
        """Save the game to the database."""
        title = title_entry.get().strip()
        platform = platform_var.get().strip()
        store = store_var.get().strip()
        completion_date = date_entry.get().strip()

        if title and platform and store and completion_date:
            insert_game(title, platform, store, completion_date)
            messagebox.showinfo("Success", "Game added successfully!")
            add_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    save_button = tk.Button(add_window, text="Add Game", command=save_game)
    save_button.pack(pady=10)
