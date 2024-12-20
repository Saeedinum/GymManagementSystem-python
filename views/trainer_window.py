import sqlite3 
from tkinter import * 
from tkinter import ttk
from tkinter.messagebox import showinfo

def view_trainer_window():
    view_trainer = Toplevel(Tk() )
    view_trainer.geometry('1700x500')
    view_trainer.title('User Details')

    # Adding frame
    frame = Frame(view_trainer)
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    # Adding a Treeview for displaying trainer details
    tree = ttk.Treeview(frame, columns=("ID", "Name", "Phone", "Salary", "Address"),show="headings", height=15)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Phone", text="Phone")
    tree.heading("Salary", text="Salary")
    tree.heading("Address", text="Address")

    tree.column("ID", width=50, anchor=CENTER)
    tree.column("Name", width=200, anchor=CENTER)
    tree.column("Phone", width=150, anchor=CENTER)
    tree.column("Salary", width=200, anchor=CENTER)
    tree.column("Address", width=250, anchor=CENTER)
    tree.pack(fill=BOTH, expand=True)


    # Adding a search entry field
    search_label = Label(view_trainer, text="Search by Name or Phone:")
    search_label.pack(pady=10)
    search_entry = Entry(view_trainer, width=30)
    search_entry.pack(pady=5)

    # Adding a delete entry field
    delete_label = Label(view_trainer, text="Delete Trainer :")
    delete_label.pack(pady=10)
    delete_entry = Entry(view_trainer, width=30)
    delete_entry.pack(pady=5)

    # Function to display all trainers initially
    def display_all_trainers():
        for row in tree.get_children():
            tree.delete(row)

        try:
            con = sqlite3.connect("database.db")
            cursor = con.cursor()
            cursor.execute("""
                SELECT 
                    trainer_id,
                    trainer_fname || ' ' || trainer_lname,
                    trainer_phone,
                    trainer_salary,
                    trainer_address
                FROM trainer
            """)
            rows = cursor.fetchall()
            con.close()

            if rows:
                for row in rows:
                    tree.insert("", END, values=row)
            else:
                showinfo("No Data", "No trainers found in the database.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")


    #delete trainer method 
    def delete_trainer():
        trainer_name = delete_entry.get().strip()  # Get the name from the delete entry field
        # Connect to the database and delete trainers matching the given name
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("""
            DELETE FROM trainer 
            WHERE trainer_fname || ' ' || trainer_lname = ?
        """, (trainer_name,))
        con.commit()
        con.close()

        # Refresh the Treeview to show the updated list
        display_all_trainers()

    # Function to display all trainers initially
    def display_all_trainers():
        for row in tree.get_children():
            tree.delete(row)

        try:
            con = sqlite3.connect("database.db")
            cursor = con.cursor()
            cursor.execute("""
                SELECT 
                    trainer_id,
                    trainer_fname || ' ' || trainer_lname,
                    trainer_phone,
                    trainer_salary,
                    trainer_address
                FROM trainer
            """)
            rows = cursor.fetchall()
            con.close()

            if rows:
                for row in rows:
                    tree.insert("", END, values=row)
            else:
                showinfo("No Data", "No trainers found in the database.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")


    # Function to search trainers
    def search_trainers():
        search_term = search_entry.get()
        if not search_term:
            display_all_trainers()
            return

        for row in tree.get_children():
            tree.delete(row)

        try:
            con = sqlite3.connect("database.db")
            cursor = con.cursor()
            cursor.execute("""
                SELECT 
                    trainer_id,
                    trainer_fname || ' ' || trainer_lname,
                    trainer_phone,
                    trainer_salary,
                    trainer_address
                FROM trainer
                WHERE trainer_phone LIKE ? OR trainer_fname || ' ' || trainer_lname LIKE ?
            """, ('%' + search_term + '%', '%' + search_term + '%'))
            rows = cursor.fetchall()
            con.close()

            if rows:
                for row in rows:
                    tree.insert("", END, values=row)
            else:
                showinfo("No Results", "No trainers found matching the search term.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")


    #connect the DataBase 
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("""
    SELECT 
            trainer_id,
            trainer_fname || ' ' || trainer_lname,
            trainer_phone,
            trainer_salary,
            trainer_address
        FROM trainer""")
    rows = cursor.fetchall()
    con.close()

    for row in rows:
        tree.insert("", END, values=row)


    #adding the buttons
    Button(view_trainer, text="Search", width=20 , command=search_trainers).pack(side="left", padx=10, pady=10)
    Button(view_trainer, text="Delete", width=20 , command=delete_trainer).pack(side="left", padx=10, pady=10)
