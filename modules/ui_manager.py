import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from modules.db_manager import add_expense, get_expenses, delete_expense, update_expense, check_expense_id_exists 
from modules.ui_dashboard import show_dashboard
from modules.ui_query import show_query
from modules.settings import show_settings

# Function to format the amount 
def format_amount(amount):
    try:
        amount_int = int(amount)
        formatted_amount = f"{amount_int:}"
        return formatted_amount
    except ValueError:
        return None 
    
    
# Function to validate the date format
def validate_date(date):
    try:
        formatted_date = datetime.strptime(date, "%d/%m/%Y")
        return formatted_date.strftime("%d/%m/%Y")
    except ValueError:
        return None  

# Expenses frame creation
def show_expenses_frame(main_content):
    # Clear previous content in the main content frame
    for widget in main_content.winfo_children():
        widget.destroy()

    # Create the frame 
    expense_frame = tk.Frame(main_content, bg="#ECF0F1")
    expense_frame.pack(fill="both", expand=True)
    

    expenses_label = tk.Label(expense_frame, text="Expense List", bg="#ECF0F1", font=("Arial", 16, "bold"))
    expenses_label.pack(pady=20)

    # Create a Treeview to display the expenses
    columns = ("ID", "Amount", "item", "Category", "Date")
    treeview = ttk.Treeview(expense_frame, columns=columns, show="headings")
    treeview.pack(fill="both", expand=True)

    # Define headings for the table
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=100)

    # Fetch data from the database and populate the table
    expenses = get_expenses()
    for expense in expenses:
        treeview.insert("", "end", values=expense)

    # Add Expense Button 
    def add_expense_window():
        add_window = tk.Toplevel(expense_frame)
        add_window.title("Add Expense")
        add_window.geometry("300x380") 

        id_label = tk.Label(add_window, text="ID:")
        id_label.pack(pady=5)
        id_entry = tk.Entry(add_window)
        id_entry.pack(pady=5)

        amount_label = tk.Label(add_window, text="Amount (integer):")
        amount_label.pack(pady=5)
        amount_entry = tk.Entry(add_window)
        amount_entry.pack(pady=5)
        
        
        item_label = tk.Label(add_window, text="Item:")
        item_label.pack(pady=5)
        item_entry = tk.Entry(add_window)
        item_entry.pack(pady=5)

        category_label = tk.Label(add_window, text="Category:")
        category_label.pack(pady=5)

    # Dropdown box for categories
        categories = ["Food", "Medical", "Utilities", "Others"]
        category_combobox = ttk.Combobox(add_window, values=categories, state="readonly")
        category_combobox.pack(pady=5)
        category_combobox.set(categories[0]) 

        date_label = tk.Label(add_window, text="Date (dd/mm/yyyy):")
        date_label.pack(pady=5)
        date_entry = tk.Entry(add_window)
        date_entry.pack(pady=5)

        # Function to submit the expense data
        def submit_expense():
            expense_id = id_entry.get()
            amount = amount_entry.get()
            item = item_entry.get()
            category = category_combobox.get()
            date = date_entry.get()

            # Check if the expense ID already exists
            if check_expense_id_exists(expense_id):
                messagebox.showerror("Duplicate ID", "This expense ID already exists. Please use a unique ID.")
                return

            # Validate the amount (ensure it's an integer)
            formatted_amount = format_amount(amount)
            if formatted_amount is None:
                messagebox.showerror("Invalid Amount", "Please enter a valid integer amount!")
                return

            # Validate the date format
            formatted_date = validate_date(date)
            if formatted_date is None:
                messagebox.showerror("Invalid Date", "Please enter a valid date in the format dd/mm/yyyy!")
                return

            # Ensure all fields are filled
            if not expense_id or not category or not date:
                messagebox.showerror("Missing Data", "Please fill in all fields!")
                return

            # Add the expense to the database 
            add_expense(expense_id, formatted_amount, item, category, formatted_date)
            treeview.insert("", "end", values=(expense_id, formatted_amount, item, category, formatted_date))

            # Close the add expense window
            add_window.destroy()

        # Submit button to call submit_expense
        submit_button = tk.Button(add_window, text="Submit Expense", command=submit_expense)
        submit_button.pack(pady=10)
        
        

    # Function to open the update expense window and pre-fill the data
    def update_expense_window():
        selected_item = treeview.selection()
        if selected_item:
            expense_id = treeview.item(selected_item)['values'][0]
            amount = treeview.item(selected_item)['values'][1]
            item = treeview.item(selected_item)['values'][2]
            category = treeview.item(selected_item)['values'][3]
            date = treeview.item(selected_item)['values'][4]

            update_window = tk.Toplevel(expense_frame)
            update_window.title("Update Expense")
            update_window.geometry("300x380")

            # Input fields for updating the expense
            id_label = tk.Label(update_window, text="ID:")
            id_label.pack(pady=5)
            id_entry = tk.Entry(update_window)
            id_entry.insert(0, expense_id)  
            id_entry.config(state="disabled")  
            id_entry.pack(pady=5)

            amount_label = tk.Label(update_window, text="Amount (integer):")
            amount_label.pack(pady=5)
            amount_entry = tk.Entry(update_window)
            amount_entry.insert(0, amount)  
            amount_entry.pack(pady=5)
            
            
            item_label = tk.Label(update_window, text="Item:")
            item_label.pack(pady=5)
            item_entry = tk.Entry(update_window)
            item_entry.insert(0, item)  
            item_entry.pack(pady=5)

            category_label = tk.Label(update_window, text="Category:")
            category_label.pack(pady=5)

            # Dropdown box for categories
            categories = ["Food", "Medical", "Utilities", "Others"]
            category_combobox = ttk.Combobox(update_window, values=categories, state="readonly")
            category_combobox.pack(pady=5)
            category_combobox.set(category)

            date_label = tk.Label(update_window, text="Date (dd/mm/yyyy):")
            date_label.pack(pady=5)
            date_entry = tk.Entry(update_window)
            date_entry.insert(0, date)  
            date_entry.pack(pady=5)

            # Function to submit the updated expense data
            def submit_updated_expense():
                new_amount = amount_entry.get()
                new_item = item_entry.get()
                new_category = category_combobox.get()
                new_date = date_entry.get()

                # Validate the amount (ensure it's an integer)
                formatted_amount = format_amount(new_amount)
                if formatted_amount is None:
                    messagebox.showerror("Invalid Amount", "Please enter a valid integer amount!")
                    return

                # Validate the date format
                formatted_date = validate_date(new_date)
                if formatted_date is None:
                    messagebox.showerror("Invalid Date", "Please enter a valid date in the format dd/mm/yyyy!")
                    return
                
                # Ensure all fields are filled
                if not new_item or not new_date:
                    messagebox.showerror("Missing Data", "Please fill in all fields.")
                    return

                # Ensure all fields are filled
                if not new_category or not new_date:
                    messagebox.showerror("Missing Data", "Please fill in all fields.")
                    return

                # Update the expense in the database
                update_expense(expense_id, formatted_amount, new_item, new_category, formatted_date)
                treeview.item(selected_item, values=(expense_id, formatted_amount, new_item, new_category, formatted_date))

                # Close the update window
                update_window.destroy()

            # Submit button to call submit_updated_expense
            submit_button = tk.Button(update_window, text="Submit Changes", command=submit_updated_expense)
            submit_button.pack(pady=10)
   
    
    # Function to save changes to the selected expense
    def save_changes():
        selected_item = treeview.selection()
        if selected_item:
            expense_id = treeview.item(selected_item)['values'][0]
            amount = treeview.item(selected_item)['values'][1]
            item = treeview.item(selected_item)['values'][2]
            category = treeview.item(selected_item)['values'][3]
            date = treeview.item(selected_item)['values'][4]
            
            update_expense(expense_id, amount, item, category, date)



    # Function to delete the selected expense
    def delete_selected_expense():
        selected_item = treeview.selection()
        if selected_item:
            expense_id = treeview.item(selected_item)['values'][0]
            delete_expense(expense_id)
            treeview.delete(selected_item)

    # Container for the buttons 
    button_frame = tk.Frame(expense_frame, bg="#ECF0F1")
    button_frame.pack(pady=10)

    # Button to open the add expense window
    add_button = tk.Button(button_frame, text="Add Expense", font=("Arial", 16), command=add_expense_window)
    add_button.pack(side="left", padx=5)

    # Save Changes Button
    save_button = tk.Button(button_frame, text="Save Changes", font=("Arial", 16), command=save_changes)
    save_button.pack(side="left", padx=5)
    
    # Update Expense Button
    update_button = tk.Button(button_frame, text="Update Expense", font=("Arial", 16), command=update_expense_window)
    update_button.pack(side="left", padx=5, )

    # Delete Expense Button
    delete_button = tk.Button(button_frame, text="Delete Expense", font=("Arial", 16), command=delete_selected_expense)
    delete_button.pack(side="left", padx=5)

# Sidebar creation
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
        button = tk.Button(sidebar, text=text, fg="white", bg="#34495E", font=("Arial", 15), command=command)
        button.pack(fill="x", pady=8)
