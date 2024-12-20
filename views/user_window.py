import sqlite3 
from tkinter import * 
from tkinter import ttk
from tkinter.font import Font
from tkinter.messagebox import showinfo

from database.db_connection import get_connection

def view_user_window(frame):
        # Clear previous content in left frame
    for widget in frame.winfo_children():
        widget.destroy()

    [con, cursor] = get_connection()
    # Adding a Treeview for displaying user details
    style = ttk.Style()
    style.configure("Custom.Treeview",
                    background='#000B58',  # Row background color
                    foreground="white",    # Text color
                    fieldbackground="red",  # Treeview background
                    font=('Arial', 14))    # Font style and size

    style.configure("Custom.Treeview.Heading",
                    background="red",  # Header background color
                    foreground="black",    # Header text color
                    font=('Arial', 18, 'bold'))

    style.map("Custom.Treeview",
              background=[("selected", "#074799")],  # Selected row background color
              foreground=[("selected", "black")])   # Selected row text color

    # Adding a Treeview for displaying user details
    tree = ttk.Treeview(frame, columns=("ID", "Name", "Phone", "Trainer", "Start Date", "End Date", "Price"),
                        style="Custom.Treeview", show="headings", height=15)

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Phone", text="Phone")
    tree.heading("Trainer", text="Trainer")
    tree.heading("Start Date", text="Start Date")
    tree.heading("End Date", text="End Date")
    tree.heading("Price", text="Price")

    tree.column("ID", width=50, anchor=CENTER ) 
    tree.column("Name", width=200, anchor=CENTER)
    tree.column("Phone", width=150, anchor=CENTER)
    tree.column("Trainer", width=200, anchor=CENTER)
    tree.column("Start Date", width=150, anchor=CENTER)
    tree.column("End Date", width=150, anchor=CENTER)
    tree.column("Price" , width=100 , anchor=CENTER)
    tree.pack(fill=BOTH, expand=True)

    container = Frame(frame, background='#000B58')
    container.pack(pady=10, fill="x")
    Label(container, text="Search by Name or Phone:",  fg="white", bg='#000B58').pack(side="left", padx=10)
    search_entry = Entry(container, width=30, background="#074799",  bd=0, fg="white")
    search_entry.pack(side="left", padx=10)

    container = Frame(frame, background='#000B58')
    container.pack(pady=10, fill="x")
    Label(container, text="Delet Customer: " ,  fg="white", bg='#000B58').pack(side="left", padx=10)
    delete_entry = Entry(container, width=30, background="#074799",  bd=0, fg="white")
    delete_entry.pack(side="left", padx=10)

    # Function to display all users initially
    def display_all_users():
        # Clear existing rows in the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Connect to the database and fetch all user details
        try:
            # Query to get all user details
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
            rows = cursor.fetchall()
            con.close()

            if rows:
                for row in rows:
                    tree.insert("", END, values=row)
            else:
                showinfo("No Data", "No users found in the database.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    #delete customer method
    def delete_customer():
        customer_name = delete_entry.get().strip()  # Get the name from the delete entry field
        cursor.execute("""
            DELETE FROM customers WHERE cust_fname || ' ' || cust_lname = ?
        """, (customer_name,))
        con.commit()
        con.close()
        display_all_users()

    
    # Function to search users
    def search_users():
        search_term = search_entry.get()
        if not search_term:
            display_all_users()
            return

        for row in tree.get_children():
            tree.delete(row)

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
            rows = cursor.fetchall()
            con.close()

            if rows:
                for row in rows:
                    tree.insert("", END, values=row)
            else:
                showinfo("No Results", "No users found matching the search term.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    cursor.execute("""
        SELECT 
            customers.customer_id AS ID,
            customers.cust_fname || ' ' || customers.cust_lname AS Name,
            customers.cust_phone AS Phone,
            trainer.trainer_fname || ' ' || trainer.trainer_lname AS Trainer,
            customers.membership_start AS "Start Date",
            customers.membership_end AS "End Date" , 
            customers.price as "amount"
        FROM customers
        JOIN trainer ON customers.trainer_id = trainer.trainer_id;
    """)
    rows = cursor.fetchall()
    con.close()

    for row in rows:
        tree.insert("", END, values=row)

    #adding the buttons
    Button(frame, text="Search", width=20 , command=search_users , background='#000B58' , fg="white"  ).pack(side="left", padx=10, pady=10)
    Button(frame, text="Delete", width=20 , command=delete_customer , background='#000B58' , fg="white").pack(side="left", padx=10, pady=10)

