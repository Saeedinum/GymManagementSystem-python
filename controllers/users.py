import sqlite3 
from tkinter import * 
from tkinter import ttk
from tkinter.messagebox import showinfo

from views.bill_window import view_bill_window


def add_user():
    add_user = Toplevel(Tk())
    add_user.geometry('1700x700')
    add_user.title('Adding User')

    # User First Name input field
    Label(add_user, text="First Name:").pack(pady=10)
    first_name_entry = Entry(add_user, width=30)
    first_name_entry.pack(pady=5)

    # User Last Name input field
    Label(add_user, text="Last Name:").pack(pady=10)
    last_name_entry  = Entry(add_user, width=30)
    last_name_entry.pack(pady=5)

    # Phone Number Field 
    Label(add_user, text="Phone Number:").pack(pady=10)
    phone_entry  = Entry(add_user, width=30)
    phone_entry .pack(pady=5)

    # Trainer Name 
    Label(add_user, text="Trainer Name:").pack(pady=10)
    trainer_name_entry  = Entry(add_user, width=30)
    trainer_name_entry .pack(pady=5)

    # Start Date 
    Label(add_user, text="Start-Date : ").pack(pady=10)
    start_date_entry  = Entry(add_user, width=30)
    start_date_entry .pack(pady=5)

    # The End Date
    Label(add_user, text="End-Date : ").pack(pady=10)
    end_date_entry  = Entry(add_user, width=30)
    end_date_entry .pack(pady=5)

    # Price
    Label(add_user, text="Price : ").pack(pady=10)  
    price_entry  = Entry(add_user, width=30)
    price_entry .pack(pady=5)

    button_frame = Frame(add_user)
    button_frame.pack(pady=20)

    # Submit button function 
    def submit_user():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        phone = phone_entry.get()
        trainer_name = trainer_name_entry.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        price = price_entry.get()

        if not all([first_name, last_name, phone, trainer_name, start_date, end_date, price]):
            Label(add_user, text="Please fill all fields!", fg="red").pack(pady=10)
            return

        # Get trainer ID based on the trainer's name
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("SELECT trainer_id FROM trainer WHERE trainer_fname || ' ' || trainer_lname = ?", (trainer_name,))
        trainer_id = cursor.fetchone()

        if trainer_id is None:
            Label(add_user, text="Trainer not found!", fg="red").pack(pady=10)
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
        Label(add_user, text="User added successfully!", fg="green").pack(pady=10)

        # Pass the customer_id dynamically for the Bill button
        Label(add_user, text="View Bill:").pack(pady=10)
        Button(button_frame, text="Bill", width=10, command=lambda: view_bill_window(customer_id)).grid(row=0, column=1, padx=10, pady=10)

    Button(button_frame, text="Submit", width=10 , command=submit_user).grid(row=0, column=0, padx=10, pady=10)

