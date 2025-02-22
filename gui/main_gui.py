import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db_operations import get_all_games, get_all_platforms, update_game, delete_game  # Import DB functions
from gui.add_game import add_game  # Import the add_game function
from gui.edit_game import edit_game  # Import the edit_game function

# Function to display data in the Treeview (table)
def display_data(search_query="", selected_platform="All", sort_column=None, sort_reverse=False):
    data = get_all_games()

    # Sort the data if required
    if sort_column:
        data = sorted(data, key=lambda x: x[sort_column], reverse=sort_reverse)

    # Clear existing data in the Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Insert filtered and sorted data into the table
    for row in data:
        title = row[1]  # Title is at index 1
        platform = row[2]  # Platform is at index 2
        
        if (search_query.lower() in title.lower()) and (selected_platform == "All" or selected_platform == platform):
            tree.insert("", "end", values=row)

def filter_data_by_platform(event):
    display_data(search_query=search_var.get(), selected_platform=platform_var.get(), sort_column=current_sort_column, sort_reverse=current_sort_reverse)

# Function to handle column sorting
def sort_column_by(event, col_index):
    global current_sort_column, current_sort_reverse
    if current_sort_column == col_index:
        current_sort_reverse = not current_sort_reverse  # Toggle sorting order
    else:
        current_sort_column = col_index
        current_sort_reverse = False  # Default to ascending if a new column is selected
    
    display_data(search_query=search_var.get(), selected_platform=platform_var.get(), sort_column=col_index, sort_reverse=current_sort_reverse)

# Context menu for right-click options (edit and delete)
def show_context_menu(event):
    item = tree.identify_row(event.y)
    if item:
        tree.selection_set(item)
        context_menu.post(event.x_root, event.y_root)

# Edit selected game in a separate window
def edit_selected_game():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No selection", "Please select a game to edit.")
        return
    
    game_id = tree.item(selected_item[0])["values"][0]  # Get the game ID from the selected row
    edit_game(game_id, display_data)  # Pass display_data to the edit_game function
    

# Delete selected game from the database
def delete_selected_game():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No selection", "Please select a game to delete.")
        return

    game_id = tree.item(selected_item[0])["values"][0]  # Get the game ID from the selected row
    result = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this game?")
    
    if result:
        delete_game(game_id)  # Call function to delete from DB
        display_data()  # Refresh the table

# Function to create the right-click menu (context menu)
def create_context_menu():
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Edit", command=edit_selected_game)
    context_menu.add_command(label="Delete", command=delete_selected_game)
    return context_menu

def create_gui():
    global root, current_sort_column, current_sort_reverse, tree, context_menu
    root = tk.Tk()
    root.title("Game Database")

    # Initialize sorting state (default sorting by "Title")
    current_sort_column = 1  # Index of "Title" column
    current_sort_reverse = False  # Default to ascending

    # Create a frame to hold all controls in a single row
    top_frame = tk.Frame(root)
    top_frame.pack(fill="x", padx=10, pady=10)  # Expands horizontally

    # Search Bar
    tk.Label(top_frame, text="Search:").pack(side="left", padx=5)
    global search_var
    search_var = tk.StringVar()
    search_entry = tk.Entry(top_frame, textvariable=search_var)
    search_entry.pack(side="left", padx=5)

    # Search Button
    search_button = tk.Button(top_frame, text="Search", command=lambda: display_data(search_var.get(), platform_var.get(), sort_column=current_sort_column, sort_reverse=current_sort_reverse))
    search_button.pack(side="left", padx=5)

    # Platform Dropdown
    tk.Label(top_frame, text="Platform:").pack(side="left", padx=5)
    global platform_var
    platform_var = tk.StringVar(value="All")  
    platforms = ["All"] + get_all_platforms()
    platform_dropdown = ttk.Combobox(top_frame, textvariable=platform_var, values=platforms, state="readonly")
    platform_dropdown.pack(side="left", padx=5)
    platform_dropdown.bind("<<ComboboxSelected>>", filter_data_by_platform)

    # Add Game Button (Aligned to the Right)
    add_button = tk.Button(top_frame, text="Add Game", command=add_game)
    add_button.pack(side="right", padx=5)

    # Set up Treeview (Table) widget
    columns = ("ID", "Title", "Platform", "Store", "Completion Date")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    # Define the columns and bind the headers to sorting function
    for col_index, col in enumerate(columns):
        tree.heading(col, text=col, command=lambda c=col_index: sort_column_by(None, c))
        tree.column(col, width=150)

    tree.pack(pady=20)

    # Bind right-click to show context menu
    context_menu = create_context_menu()
    tree.bind("<Button-3>", show_context_menu)

    display_data()  # Initially show all data

    root.mainloop()
