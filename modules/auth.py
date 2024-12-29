import tkinter as tk
from tkinter import messagebox
from modules.user_db_manager import authenticate_user  

# Login window function with authentication check
def login_window():
    login_result = False  # Default value

    def attempt_login():
        nonlocal login_result
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Required", "Please enter both username and password.")
            return

        if authenticate_user(username, password):
            login_result = True
            login_window.destroy()  
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    # Create a Tk window for login
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x270")
    login_window.resizable(False, False)

    # Styles
    label_font = ("Arial", 14)
    entry_font = ("Arial", 12)
    button_font = ("Arial", 16)
    entry_width = 20

    # Username field
    tk.Label(login_window, text="Username", font=label_font).pack(pady=10)
    username_entry = tk.Entry(login_window, font=entry_font, width=entry_width)
    username_entry.pack(pady=5)

    # Password field
    tk.Label(login_window, text="Password", font=label_font).pack(pady=10)
    password_entry = tk.Entry(login_window, font=entry_font, show="*", width=entry_width)
    password_entry.pack(pady=5)

    # Login button
    tk.Button(login_window, text="Login", font=button_font, command=attempt_login, width=10, height=1).pack(pady=20)

    # Handle close event
    login_window.protocol("WM_DELETE_WINDOW", lambda: login_window.destroy())

    # Run the login window mainloop
    login_window.mainloop()

    return login_result
