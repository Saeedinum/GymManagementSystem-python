import sqlite3
from tkinter import Button, Label

from database.db_connection import get_connection
from views.bill_window import view_bill_window

# Submit button function
def submit_user(first_name, last_name, phone, trainer_name, start_date, end_date, price , frame,button_frame):

    if not all([first_name, last_name, phone, trainer_name, start_date, end_date, price]):
        Label(frame, text="Please fill all fields!", fg="red", background='#000B58').pack(pady=10)
        return

    # Get trainer ID based on the trainer's name
    [con, cursor] = get_connection()
    cursor.execute("SELECT trainer_id FROM trainer WHERE trainer_fname || ' ' || trainer_lname = ?", (trainer_name,))
    trainer_id = cursor.fetchone()

    if trainer_id is None:
        Label(frame, text="Trainer not found!", fg="red").pack(pady=10)
        con.close()
        return

    trainer_id = trainer_id[0]  # Extract trainer_id from the tuple

    # Insert into the customers table
    cursor.execute("""
        INSERT INTO customers (trainer_id, cust_fname, cust_lname, cust_phone, membership_start, membership_end, price)
        VALUES (?, ?, ?, ?, ?, ? ,?)
    """, (trainer_id, first_name, last_name, phone, start_date, end_date, price))

    con.commit()

    # Fetch the last inserted customer_id
    customer_id = cursor.lastrowid
    con.close()

    # Display success message
    Label(frame, text="User added successfully!", fg="green").pack(pady=10)

    # Pass the customer_id dynamically for the Bill button
    Label(frame, text="View Bill:").pack(pady=10)
    Button(button_frame, text="Bill", width=10, command=lambda: view_bill_window(customer_id)).grid(row=0, column=1, padx=10, pady=10)

# db_connection.py
import sqlite3

def fetch_all_users(cursor):
    """Fetches all users from the database."""
    try:
        cursor.execute("""
            SELECT 
                customers.customer_id AS ID,
                customers.cust_fname || ' ' || customers.cust_lname AS Name,
                customers.cust_phone AS Phone,
                trainer.trainer_fname || ' ' || trainer.trainer_lname AS Trainer,
                customers.membership_start AS "Start Date",
                customers.membership_end AS "End Date"
            FROM customers
            JOIN trainer ON customers.trainer_id = trainer.trainer_id;
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")
        return []

def delete_customer_by_name(cursor, customer_name):
    """Deletes a customer from the database by name."""
    try:
        cursor.execute("""
            DELETE FROM customers WHERE cust_fname || ' ' || cust_lname = ?
        """, (customer_name,))
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")

def search_users(cursor, search_term):
    """Searches for users by name or phone."""
    try:
        cursor.execute("""
            SELECT 
                customers.customer_id AS ID,
                customers.cust_fname || ' ' || customers.cust_lname AS Name,
                customers.cust_phone AS Phone,
                trainer.trainer_fname || ' ' || trainer.trainer_lname AS Trainer,
                customers.membership_start AS "Start Date",
                customers.membership_end AS "End Date"
            FROM customers
            JOIN trainer ON customers.trainer_id = trainer.trainer_id
            WHERE customers.cust_phone LIKE ? OR customers.cust_fname || ' ' || customers.cust_lname LIKE ?
        """, ('%' + search_term + '%', '%' + search_term + '%'))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error searching users: {e}")
        return []
