import sqlite3
from tkinter import Button, Label

from views.bill_window import view_bill_window

# Submit button function
def submit_user(first_name, last_name, phone, trainer_name, start_date, end_date, price , frame,button_frame):

    if not all([first_name, last_name, phone, trainer_name, start_date, end_date, price]):
        Label(frame, text="Please fill all fields!", fg="red").pack(pady=10)
        return

    # Get trainer ID based on the trainer's name
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
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
