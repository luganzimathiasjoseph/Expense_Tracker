import tkinter as tk
from tkinter import ttk
from modules.db_manager import get_expenses  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Dashboard frame creation
def show_dashboard(main_content):
    
    # Clear previous content in the main content frame
    for widget in main_content.winfo_children():
        widget.destroy()

    # Create the dashboard frame
    dashboard_frame = tk.Frame(main_content, bg="#ECF0F1")
    dashboard_frame.pack(fill="both", expand=True)

    # Configure Treeview style 
    style = ttk.Style()
    style.configure(
        "Treeview",
        font=("Arial", 17),  
        rowheight=30  
    )
    style.configure("Treeview.Heading", font=("Arial", 18, "bold"))  

   
    welcome_label = tk.Label(
        dashboard_frame, text="Manage your Expenses", 
        bg="#ECF0F1", font=("Arial", 20, "bold")  
    )
    welcome_label.pack(pady=30)
    

    # Split the page into two columns 
    content_frame = tk.Frame(dashboard_frame, bg="#ECF0F1")
    content_frame.pack(fill="both", expand=True)

    # Using grid for layout control
    left_frame = tk.Frame(content_frame, bg="#ECF0F1")
    left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    right_frame = tk.Frame(content_frame, bg="#ECF0F1")
    right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    # Style grid
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    # Left frame: Treeview table
    expenses_label = tk.Label(
        left_frame, text="Summary of Expenses", 
        bg="#ECF0F1", font=("Arial", 20, "bold")  
    )
    expenses_label.pack(pady=15)

    columns = ("ID", "Amount", "item", "Category", "Date")
    treeview = ttk.Treeview(
        left_frame,
        columns=columns,
        show="headings",
        height=10  
    )
    treeview.pack(fill="both", expand=True)

    # Define headings for the table
    column_widths = {"ID": 3, "Amount": 80,  "item" :80, "Category": 80, "Date": 100}
    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, width=column_widths[col], anchor="w")

    # Fetch data from the database 
    expenses = get_expenses()  
    for expense in expenses:
        formatted_expense = (
            expense[0],  # ID
            f"{int(expense[1]):,}",  #Amount
            expense[2],  # Item
            expense[3],  # Category
            expense[4]   # Date
        )
        treeview.insert("", "end", values=formatted_expense)

    # Right frame: Graph section
    graph_label = tk.Label(
        right_frame, text="Expenses Graph", 
        bg="#ECF0F1", font=("Arial", 20, "bold" )  
    )
    graph_label.pack(expand=True)

    # Plot the graph
    plot_expenses_graph(right_frame)


def plot_expenses_graph(right_frame):
    
    # Fetch expenses from the database and group them by category
    category_expenses = fetch_expenses_data()

    if not category_expenses:
        return
    
    # Style graph bars
    fig, ax = plt.subplots(figsize=(2, 7.5))  
    
    bar_width = 0.4  
    ax.bar(category_expenses.keys(), category_expenses.values(), color='skyblue', width=bar_width)
    ax.set_xlabel('Category', fontsize=12)  
    ax.set_ylabel('Amount', fontsize=12)  
    ax.set_title('Expenses by Category', fontsize=14)  

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def fetch_expenses_data():
    """Fetch expenses from the database and group them by category."""
    expenses = get_expenses()
    category_expenses = {}

    for expense in expenses:
        amount = expense[1]  
        category = expense[3] 
        category_expenses[category] = category_expenses.get(category, 0) + amount

    return category_expenses
