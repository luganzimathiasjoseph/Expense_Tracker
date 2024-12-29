import tkinter as tk
from modules.ui_manager import show_expenses_frame  
from modules.ui_dashboard import show_dashboard
from modules.ui_query import show_query
from modules.settings import show_settings
from modules.db_manager import init_db  
from modules.auth import login_window  
from PIL import Image, ImageTk


init_db()

# Run the authentication window first
if not login_window():  # If authentication fails or the user exits, stop the program
    exit()
    

# Function to switch between frames
def show_frame(frame_name):
    # Hide all frames
    for frame in frames.values():
        frame.pack_forget()

    # Show the selected frame
    frames[frame_name].pack(fill="both", expand=True)

# Function to create the sidebar
def create_sidebar(root, show_expenses_frame, main_content):
    sidebar = tk.Frame(root, bg="#2C3E50", width=400, height=600, padx=10, pady=10)  
    sidebar.pack(side="left", fill="y")

    buttons = [
        ("Home", lambda: show_dashboard(main_content)),  
        ("Expenses", lambda: show_expenses_frame(main_content)), 
        ("Query", lambda: show_query(main_content)),
        ("Settings", lambda: show_settings(main_content))
    ]

    for (text, command) in buttons:
        button = tk.Button(
            sidebar,
            text=text,
            fg="white",
            bg="#34495E",
            font=("Arial", 12),
            command=command,
            width=28  
        )
        button.pack(fill="x", pady=5)

# Main content area (right side)
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("1000x600")  


# Load and set the icon using Pillow 
icon_path = 'resources/icon.png'
icon_image = Image.open(icon_path)
icon_tk = ImageTk.PhotoImage(icon_image)
root.tk.call('wm', 'iconphoto', root._w, icon_tk)

# Main content area
main_content = tk.Frame(root, bg="#ECF0F1", width=600, height=600)
main_content.pack(side="right", fill="both", expand=True)

# Sidebar UI 
create_sidebar(root, show_expenses_frame, main_content)


# Dictionary of frames for easier switching
frames = {
    "home": tk.Frame(main_content),
    "expenses": tk.Frame(main_content),  
    "query": tk.Frame(main_content),
    "settings": tk.Frame(main_content)
}


show_dashboard(main_content)

root.mainloop()
