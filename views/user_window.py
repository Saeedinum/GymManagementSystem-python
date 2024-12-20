# view_user_window.py
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from database.db_connection import get_connection
from controllers.users import fetch_all_users, search_users, delete_customer_by_name

def view_user_window(frame):
    # Clear previous content in left frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Get the database connection and cursor
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

    tree = ttk.Treeview(frame, columns=("ID", "Name", "Phone", "Trainer", "Start Date", "End Date", "Price"),
                        style="Custom.Treeview", show="headings", height=15)

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
    tree.column("Price", width=100, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True)

    container = Frame(frame, background='#000B58')
    container.pack(pady=10, fill="x")
    Label(container, text="Search by Name or Phone:",  fg="white", bg='#000B58').pack(side="left", padx=10)
    search_entry = Entry(container, width=30, background="#074799",  bd=0, fg="white")
    search_entry.pack(side="left", padx=10)

    container = Frame(frame, background='#000B58')
    container.pack(pady=10, fill="x")
    Label(container, text="Delete Customer: ",  fg="white", bg='#000B58').pack(side="left", padx=10)
    delete_entry = Entry(container, width=30, background="#074799",  bd=0, fg="white")
    delete_entry.pack(side="left", padx=10)

    # Function to display all users initially
    def display_all_users():
        for row in tree.get_children():
            tree.delete(row)

        rows = fetch_all_users(cursor)
        if rows:
            for row in rows:
                tree.insert("", END, values=row)
        else:
            showinfo("No Data", "No users found in the database.")

    # Delete customer method
    def delete_customer():
        customer_name = delete_entry.get().strip()
        delete_customer_by_name(cursor, customer_name)
        con.commit()  # Commit after deletion
        display_all_users()

    # Function to search users
    def search_users():
        search_term = search_entry.get()
        if not search_term:
            display_all_users()
            return

        for row in tree.get_children():
            tree.delete(row)

        rows = search_users(cursor, search_term)
        if rows:
            for row in rows:
                tree.insert("", END, values=row)
        else:
            showinfo("No Results", "No users found matching the search term.")

    # Initially load all users
    display_all_users()

    # Adding buttons
    Button(frame, text="Search", width=20, command=search_users, background='#000B58', fg="white").pack(side="left", padx=10, pady=10)
    Button(frame, text="Delete", width=20, command=delete_customer, background='#000B58', fg="white").pack(side="left", padx=10, pady=10)

    # Close the database connection when the window is closed
    con.close()
