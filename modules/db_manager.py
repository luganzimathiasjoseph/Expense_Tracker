from datetime import datetime
import sqlite3

DB_PATH = "database/expenses.db"


def init_db():
    """Initialize the database and create the expenses table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY UNIQUE,
            amount INT,
            item TEXT,
            category TEXT,
            date DATE
        )
    ''')
    conn.commit()
    conn.close()


def add_expense(id, amount, item, category, date):
    """Add a new expense to the database and return its generated ID."""
    # Convert the date to DATETIME format (YYYY-MM-DD )
    date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (id, amount, item, category, date) VALUES (?, ?, ?, ?, ?)", (id, amount, item, category, date))
    conn.commit()
    last_inserted_id = cursor.lastrowid
    conn.close()
    return last_inserted_id

def update_expense(expense_id, amount, item, category, date):
    """Update an existing expense in the database."""
    # Convert the date to DATETIME format (YYYY-MM-DD HH:MM:SS)
    date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE expenses SET amount = ?, item = ?, category = ?, date = ? WHERE id = ?",
        (amount, item, category, date, expense_id)
    )
    conn.commit()
    conn.close()


def get_expenses():
    """Fetch all expenses from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_expense(expense_id):
    """Delete an expense from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    
    
def check_expense_id_exists(expense_id):
    """Check if an expense ID already exists in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM expenses WHERE id = ?", (expense_id,))
    result = cursor.fetchone()  
    conn.close()
    return bool(result)  


def query_expenses(category=None, start_date=None, end_date=None):
    """
    Fetch expenses from the database filtered by category and/or date range.
    """
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Build the query with optional filters
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = ?"
        params.append(category)
    
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    
    # Execute the query with the parameters
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_categories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM expenses")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories