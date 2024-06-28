import sqlite3
from datetime import datetime
import logging
from contextlib import contextmanager
# util/config.py
# from config import DATABASE_NAME, TAX_RATE

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATABASE_NAME = 'billing_system.db'
TAX_RATE = 0.05

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn
    finally:
        conn.close()

def setup_database():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )''')

        # Create invoices table with auto-increment id
        c.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            total REAL NOT NULL,
            tax REAL NOT NULL,
            grand_total REAL NOT NULL
        )''')
        conn.commit()
    logging.info("Database setup completed.")

def add_product(name, price):
    if not name or price <= 0:
        logging.error("Invalid product name or price.")
        return "Invalid product name or price."
    
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
    logging.info(f"Product added: {name}, Price: {price}")
    return "Product added successfully!"

def calculate_total():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT SUM(price) FROM products")
        total = c.fetchone()[0] or 0
    logging.info(f"Total calculated: {total}")
    return total

def generate_invoice():
    total = calculate_total()
    tax = total * TAX_RATE
    grand_total = total + tax
    created_at = datetime.now().isoformat()

    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO invoices (created_at, total, tax, grand_total) VALUES (?, ?, ?, ?)",
                  (created_at, total, tax, grand_total))
        conn.commit()
    
    invoice = f"Date: {created_at}\nTotal: {total:.2f}\nTax: {tax:.2f}\nGrand Total: {grand_total:.2f}"
    logging.info("Invoice generated.")
    return invoice

def main():
    setup_database()
    
    while True:
        print("\nBilling System")
        print("1. Add Product")
        print("2. Calculate Total")
        print("3. Generate Invoice")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            try:
                price = float(input("Enter product price: "))
                message = add_product(name, price)
                print(message)
            except ValueError:
                logging.error("Invalid price input.")
                print("Invalid price. Please enter a valid number.")
        
        elif choice == '2':
            total = calculate_total()
            print(f"Total: {total:.2f}")

        elif choice == '3':
            invoice = generate_invoice()
            print("\nInvoice")
            print(invoice)

        elif choice == '4':
            break

        else:
            logging.warning("Invalid choice entered.")
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()