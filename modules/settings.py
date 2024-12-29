import tkinter as tk
from tkinter import messagebox
from modules.user_db_manager import change_credentials, get_users  

# Fetch user data
users = get_users()

# Check if there are any users returned
if users:
    username = users[0].get('username', 'user123')
    password = users[0].get('password', 'password123')
else:
    username, password = "user123", "password123"  # Fallback default values

default_settings = {
    "username": username,
    "password": password,
    "notifications": ["Notification 1"]
}

def change_username():
    new_username = username_entry.get()
    if new_username:
        success = change_credentials(old_username=username, new_username=new_username)
        if success:
            default_settings["username"] = new_username
            messagebox.showinfo("Success", f"Username changed to: {default_settings['username']}")
        else:
            messagebox.showerror("Error", "Failed to change username. Please check your old credentials.")
    else:
        messagebox.showerror("Error", "Invalid username.")
        

def change_password():
    old_password = old_password_entry.get()
    new_password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()

    if new_password == confirm_password:
        if old_password == password:  
            success = change_credentials( old_password=old_password, new_password=new_password)
            if success:
                default_settings["password"] = new_password
                messagebox.showinfo("Success", "Password updated successfully.")
            else:
                messagebox.showerror("Error", "Failed to change password. Please check your old password.")
        else:
            messagebox.showerror("Error", "Old password is incorrect.")
    else:
        messagebox.showerror("Error", "New password and confirmation do not match.")
        

def show_user_details(main_content):
    # Clear previous content in the main content frame
    for widget in main_content.winfo_children():
        widget.destroy()

    # Create the user details frame 
    user_details_frame = tk.Frame(main_content, bg="#ECF0F1")
    user_details_frame.pack(fill="both", expand=True)

    # Username section
    tk.Label(user_details_frame, text="New Username:", font=("Arial", 14), bg="#ECF0F1").grid(row=2, column=0, padx=10, pady=5)
    global username_entry
    username_entry = tk.Entry(user_details_frame, font=("Arial", 14))
    username_entry.grid(row=2, column=1, padx=10, pady=5)
    username_entry.insert(0, default_settings["username"])  

    tk.Button(user_details_frame, text="Change Username", command=change_username, font=("Arial", 14)).grid(row=2, column=2, padx=10, pady=5)

    # Password section
    tk.Label(user_details_frame, text="Old Password:", font=("Arial", 14), bg="#ECF0F1").grid(row=3, column=0, padx=10, pady=5)
    global old_password_entry
    old_password_entry = tk.Entry(user_details_frame, show="*", font=("Arial", 14))
    old_password_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(user_details_frame, text="New Password:", font=("Arial", 14), bg="#ECF0F1").grid(row=4, column=0, padx=10, pady=5)
    global new_password_entry
    new_password_entry = tk.Entry(user_details_frame, show="*", font=("Arial", 14))
    new_password_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(user_details_frame, text="Confirm New Password:", font=("Arial", 14), bg="#ECF0F1").grid(row=5, column=0, padx=10, pady=5)
    global confirm_password_entry
    confirm_password_entry = tk.Entry(user_details_frame, show="*", font=("Arial", 14))
    confirm_password_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(user_details_frame, text="Change Password", command=change_password, font=("Arial", 14)).grid(row=5, column=2, padx=10, pady=5)

    # Button to return to settings page
    tk.Button(user_details_frame, text="Back to Settings", command=lambda: show_settings(main_content), font=("Arial", 14)).grid(row=6, column=0, columnspan=3, pady=20)

def show_about(main_content):
    # Clear previous content in the main content frame
    for widget in main_content.winfo_children():
        widget.destroy()

    # Create the about section frame 
    about_frame = tk.Frame(main_content, bg="#ECF0F1")
    about_frame.pack(fill="both", expand=True)

    about_text = (
        "Expense Tracker Application\n"
        "Version: 1.0\n"
        "Developed by: MATT\n"
        "Track your expenses with ease!"
    )
    tk.Label(about_frame, text=about_text, bg="#ECF0F1", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=20)

    # Button to return to settings page
    tk.Button(about_frame, text="Back to Settings", command=lambda: show_settings(main_content), font=("Arial", 14)).grid(row=1, column=0, pady=10)

def show_user_manual(main_content):
    # Clear previous content in the main content frame
    for widget in main_content.winfo_children():
        widget.destroy()

    # Create the user manual section frame 
    manual_frame = tk.Frame(main_content, bg="#ECF0F1")
    manual_frame.pack(fill="both", expand=True)

    manual_text = (
        "User Manual:\n"
        "1. To track expenses, go to the dashboard and analyze the Expense Summary and Graph'.\n"
        "2. To add, udate, delete and save expenses, go to the Expenses page'.\n"
        "3. View your query of expense in the 'Query' section.\n"
        "4. Modify settings in the 'Settings' section.\n"
        "5. For assistance, visit our support page."
    )
    tk.Label(manual_frame, text=manual_text, bg="#ECF0F1", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=20)

    # Button to return to settings page
    tk.Button(manual_frame, text="Back to Settings", command=lambda: show_settings(main_content), font=("Arial", 14)).grid(row=1, column=0, pady=10)

def show_notifications(main_content):
    # Clear previous content in the main content frame
    for widget in main_content.winfo_children():
        widget.destroy()

    # Create the notifications 
    notifications_frame = tk.Frame(main_content, bg="#ECF0F1")
    notifications_frame.pack(fill="both", expand=True)

    if default_settings["notifications"]:
        notifications_text = "\n".join([f"{idx + 1}. {notif}" for idx, notif in enumerate(default_settings["notifications"])])
        tk.Label(notifications_frame, text=notifications_text, bg="#ECF0F1", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=20)
    else:
        tk.Label(notifications_frame, text="No notifications available.", bg="#ECF0F1", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=20)

    # Button to return to settings page
    tk.Button(notifications_frame, text="Back to Settings", command=lambda: show_settings(main_content), font=("Arial", 14)).grid(row=1, column=0, pady=10)

def show_settings(main_content):
    # Clear previous content in the main content frame
    for widget in main_content.winfo_children():
        widget.destroy()

    # Create the settings frame (simulate tab switch)
    settings_frame = tk.Frame(main_content, bg="#ECF0F1")
    settings_frame.pack(fill="both", expand=True)
    
   
    tk.Label(settings_frame, text="Settings", font=("Arial", 28, "bold"), bg="#ECF0F1").pack(pady=10, anchor='center')
    tk.Label(settings_frame, text=f"Username: {default_settings['username']}", font=("Arial", 20, "bold"), bg="#ECF0F1").pack(pady=20, anchor='w')


    tk.Button(settings_frame, text="User Details", command=lambda: show_user_details(main_content), font=("Arial", 14)).pack(fill="x", padx=20, pady=10, anchor='w')
    tk.Button(settings_frame, text="About Us", command=lambda: show_about(main_content), font=("Arial", 14)).pack(fill="x", padx=20, pady=10, anchor='w')
    tk.Button(settings_frame, text="User Manual", command=lambda: show_user_manual(main_content), font=("Arial", 14)).pack(fill="x", padx=20, pady=10, anchor='w')
    tk.Button(settings_frame, text="Notifications", command=lambda: show_notifications(main_content), font=("Arial", 14)).pack(fill="x", padx=20, pady=10, anchor='w')
