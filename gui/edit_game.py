import tkinter as tk
from tkinter import messagebox
from db_operations import update_game, get_game_by_id

def edit_game(game_id, display_data):  # Accept display_data as a parameter
    # Retrieve the current game data from the database
    game_data = get_game_by_id(game_id)
    if not game_data:
        messagebox.showerror("Error", "Game not found.")
        return

    # Create a new window for editing the game details
    edit_window = tk.Toplevel()
    edit_window.title("Edit Game Details")

    # Define labels and entry fields
    tk.Label(edit_window, text="Title:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    title_var = tk.StringVar(value=game_data[1])  # Pre-fill with the current title
    title_entry = tk.Entry(edit_window, textvariable=title_var, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Platform:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    platform_var = tk.StringVar(value=game_data[2])  # Pre-fill with the current platform
    platform_entry = tk.Entry(edit_window, textvariable=platform_var, width=40)
    platform_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Store:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    store_var = tk.StringVar(value=game_data[3])  # Pre-fill with the current store
    store_entry = tk.Entry(edit_window, textvariable=store_var, width=40)
    store_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Completion Date:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    completion_date_var = tk.StringVar(value=game_data[4])  # Pre-fill with the current completion date
    completion_date_entry = tk.Entry(edit_window, textvariable=completion_date_var, width=40)
    completion_date_entry.grid(row=3, column=1, padx=10, pady=5)

    # Function to save the updated data to the database
    def save_changes():
        updated_title = title_var.get()
        updated_platform = platform_var.get()
        updated_store = store_var.get()
        updated_completion_date = completion_date_var.get()

        if not updated_title or not updated_platform or not updated_store or not updated_completion_date:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        # Update the game in the database
        update_game(game_id, updated_title, updated_platform, updated_store, updated_completion_date)
        # Close the edit window and refresh the main window
        edit_window.destroy()
        
        # Refresh the data in the main window
        display_data(search_query="", selected_platform="All", sort_column=None, sort_reverse=False)

    # Function to cancel the edit
    def cancel_edit():
        edit_window.destroy()

    # Buttons for saving or canceling
    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

    cancel_button = tk.Button(edit_window, text="Cancel", command=cancel_edit)
    cancel_button.grid(row=5, column=0, columnspan=2, pady=5)

    # Run the edit window
    edit_window.mainloop()
