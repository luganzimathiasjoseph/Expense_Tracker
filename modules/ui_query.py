import tkinter as tk
from tkinter import ttk
from datetime import datetime
from modules.db_manager import query_expenses, fetch_categories

def show_query(main_content):
    # Clear previous content in the main content frame
    for widget in main_content.winfo_children():
        widget.destroy()

    # Create the query frame
    show_query_frame = tk.Frame(main_content, bg="#ECF0F1")
    show_query_frame.pack(fill="both", expand=True)

    # Configure Treeview style 
    style = ttk.Style()
    style.configure(
        "Treeview",
        font=("Arial", 18),  
        rowheight=25  
    )
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"))  

    # Apply Filters for button
    style.configure(
        "Apply.TButton",
        font=("Arial", 16, "bold")
    )

    # Split the page into two columns
    content_frame = tk.Frame(show_query_frame, bg="#ECF0F1")
    content_frame.pack(fill="both", expand=True)

    left_frame = tk.Frame(content_frame, bg="#ECF0F1")
    left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    right_frame = tk.Frame(content_frame, bg="#ECF0F1", width=300)
    right_frame.pack(side="left", fill="both", padx=10, pady=10, expand=False)

    # Left frame: Treeview table
    expenses_label = tk.Label(
        left_frame, text="Query Expenses",
        bg="#ECF0F1", font=("Arial", 18, "bold")
    )
    expenses_label.pack(pady=10)

    columns = ("ID", "Amount", "Item", "Category", "Date")

    # Treeview for expenses
    treeview = ttk.Treeview(
        left_frame,
        columns=columns,
        show="headings",
        height=10
    )
    treeview.pack(fill="both", expand=True)

    # Define headings for the table
    column_widths = {"ID": 5, "Amount": 80, "Item": 80, "Category": 80, "Date": 100}
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=column_widths[col], anchor="w")

    # Right frame: Filters
    filters_label = tk.Label(
        right_frame, text="Filters",
        bg="#ECF0F1", font=("Arial", 16, "bold")
    )
    filters_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Category filter
    category_label = tk.Label(
        right_frame, text="Category:",
        bg="#ECF0F1", font=("Arial", 16)
    )
    category_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    categories = fetch_categories()
    categories.insert(0, "All")

    category_var = tk.StringVar(value="All")
    category_combobox = ttk.Combobox(
        right_frame,
        textvariable=category_var,
        values=categories,
        state="readonly"
    )
    category_combobox.grid(row=1, column=1, padx=10, pady=5)


    # Start date filter
    start_date_label = tk.Label(
        right_frame, text="Start Date (dd/mm/yyyy):",
        bg="#ECF0F1", font=("Arial", 16)
    )
    start_date_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    start_date_var = tk.StringVar()
    start_date_entry = ttk.Entry(
        right_frame, textvariable=start_date_var, width=20
    )
    start_date_entry.grid(row=2, column=1, padx=10, pady=5)

    # End date filter
    end_date_label = tk.Label(
        right_frame, text="End Date (dd/mm/yyyy):",
        bg="#ECF0F1", font=("Arial", 16)
    )
    end_date_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

    end_date_var = tk.StringVar()
    end_date_entry = ttk.Entry(
        right_frame, textvariable=end_date_var, width=20
    )
    end_date_entry.grid(row=3, column=1, padx=10, pady=5)

    # Total label
    total_label = tk.Label(
        right_frame,
        text="Total Amount: 0.00",
        bg="#ECF0F1",
        font=("Arial", 16, "bold")
    )
    total_label.grid(row=5, column=0, columnspan=2, pady=20)

    # Function to refresh Treeview with filtered data
    def refresh_treeview():
        # Clear existing rows
        for item in treeview.get_children():
            treeview.delete(item)

        # Get filter values
        category = category_var.get()
        start_date = start_date_var.get()
        end_date = end_date_var.get()

        if category == "All":
            category = None

        start_date_obj = None
        end_date_obj = None

        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")
            except ValueError:
                print("Invalid start date format! Expected format: dd/mm/yyyy")
                return
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, "%d/%m/%Y")
            except ValueError:
                print("Invalid end date format! Expected format: dd/mm/yyyy")
                return

        expenses = query_expenses(
            category=category,
            start_date=start_date_obj if start_date_obj else None,
            end_date=end_date_obj if end_date_obj else None
        )

        for expense in expenses:
            # Format the amount with commas
            formatted_expense = (
                expense[0],  # ID
                f"{int(expense[1]):,}",  
                expense[2],
                expense[3], 
                expense[4]   
            )
            treeview.insert("", "end", values=formatted_expense)

        # Calculate total amount
        try:
            total_amount = sum(float(expense[1]) for expense in expenses)
        except ValueError:
            print("Error: Amount contains non-numeric data.")
            total_amount = 0

        # Format the total amount 
        total_label.config(text=f"Total Amount: {total_amount:,}")

    # Apply filters button
    apply_filters_button = ttk.Button(
        right_frame, text="Apply Filters", style="Apply.TButton", command=refresh_treeview
    )
    apply_filters_button.grid(row=4, column=0, columnspan=2, pady=20, padx=10, ipadx=20, ipady=10)

    # Populate the Treeview 
    refresh_treeview()
