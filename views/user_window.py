import sqlite3 
from tkinter import * 
from tkinter import ttk
from tkinter.messagebox import showinfo


def view_user_window():
    view_user = Toplevel(Tk() )
    view_user.geometry('1700x500')
    view_user.title('User Details')

    # Adding frame
    frame = Frame(view_user)
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)


    # Adding a Treeview for displaying user details
    tree = ttk.Treeview(frame, columns=("ID","Name", "Phone", "Trainer","Start Date", "End Date" , "Price"),show="headings", height=15)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Phone", text="Phone")
    tree.heading("Trainer", text="Trainer")
    tree.heading("Start Date", text="Start Date")
    tree.heading("End Date", text="End Date")
    tree.heading("Price", text="Price")


    tree.column("ID", width=50, anchor=CENTER) 
    tree.column("Name", width=200, anchor=CENTER)
    tree.column("Phone", width=150, anchor=CENTER)
    tree.column("Trainer", width=200, anchor=CENTER)
    tree.column("Start Date", width=150, anchor=CENTER)
    tree.column("End Date", width=150, anchor=CENTER)
    tree.column("Price" , width=100 , anchor=CENTER)
    tree.pack(fill=BOTH, expand=True)

    # Adding a search entry field
    search_label = Label(view_user, text="Search by Name or Phone:")
    search_label.pack(pady=10)
    search_entry = Entry(view_user, width=30)
    search_entry.pack(pady=5)

    #delete user
    delete_label = Label(view_user, text="Delet Customer: ")
    delete_label.pack(pady=10)
    delete_entry = Entry(view_user, width=30)
    delete_entry.pack(pady=5)

    # Function to display all users initially
    def display_all_users():
        # Clear existing rows in the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Connect to the database and fetch all user details
        try:
            con = sqlite3.connect("database.db")
            cursor = con.cursor()

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
        # Connect to the database and delete trainers matching the given name
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
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
            con = sqlite3.connect("database.db")
            cursor = con.cursor()
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


    #connect the DataBase 
    con = sqlite3.connect('database.db')
    cursor=con.cursor()
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
    Button(view_user, text="Search", width=20 , command=search_users).pack(side="left", padx=10, pady=10)
    Button(view_user, text="Delete", width=20 , command=delete_customer).pack(side="left", padx=10, pady=10)

