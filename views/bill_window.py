import sqlite3 
from tkinter import * 
from tkinter.messagebox import showinfo

def view_bill_window(customer_id):
    # Create a new window for displaying the bill details
    bill_window = Toplevel(Tk() )
    bill_window.geometry('600x400')
    bill_window.title('Bill Details')

    # Connect to the database
    con = sqlite3.connect("database.db")
    cursor = con.cursor()

    # Query to get customer details and calculate the total amount
    cursor.execute("""
    SELECT
        customers.customer_id,
        customers.cust_fname || ' ' || customers.cust_lname AS Name,
        customers.membership_start AS "Start Date",
        customers.membership_end AS "End Date",
        julianday(customers.membership_end) - julianday(customers.membership_start) AS days,
        customers.price AS Amount
    FROM customers
    WHERE customer_id = ?
    """, (customer_id,))
    row = cursor.fetchone()
    print(row) 
    con.close()

    # If the customer exists, display the information
    if row:
        customer_id, name, start_date, end_date, days, amount = row
        
        # Displaying the details in the new window
        Label(bill_window, text=f"Customer ID: {customer_id}", font=("Arial", 12)).pack(pady=5)
        Label(bill_window, text=f"Name: {name}", font=("Arial", 12)).pack(pady=5)
        Label(bill_window, text=f"Start Date: {start_date}", font=("Arial", 12)).pack(pady=5)
        Label(bill_window, text=f"End Date: {end_date}", font=("Arial", 12)).pack(pady=5)
        Label(bill_window, text=f"Duration: {int(days)} days", font=("Arial", 12)).pack(pady=5)
        Label(bill_window, text=f"Amount Paid: ${amount}", font=("Arial", 12)).pack(pady=5)
    else:
        Label(bill_window, text="Customer not found", font=("Arial", 12), fg="red").pack(pady=5)
