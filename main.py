import sqlite3 
from tkinter import * 
from tkinter import ttk
from tkinter.messagebox import showinfo

from database.schema import initialize_schema


# Initialize the database schema
initialize_schema()

root = Tk() 
root.geometry('1700x500') 
root.title('over View') 

def view_bill_window(customer_id):
    # Create a new window for displaying the bill details
    bill_window = Toplevel(root)
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


def view_trainer_window():
    view_trainer = Toplevel(root)
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

def view_user_window():
    view_user = Toplevel(root)
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


#here for adding the Trainer
def add_trainer():
    add_user = Toplevel(root)
    add_user.geometry('1700x500')
    add_user.title('Adding Trainer')

    #Trainer fName 
    Label(add_user, text="Trainer First Name:").pack(pady=10)
    first_name_entry = Entry(add_user, width=30)
    first_name_entry.pack(pady=5)
    #Trainer lName 
    Label(add_user, text="Trainer last Name:").pack(pady=10)
    last_name_entry = Entry(add_user, width=30)
    last_name_entry.pack(pady=5)

    #Phone Number Field 
    Label(add_user, text="Phone Number:").pack(pady=10)
    phone_entry = Entry(add_user, width=30)
    phone_entry.pack(pady=5)

    # The salary  
    Label(add_user, text="salary : ").pack(pady=10)
    salary_entry = Entry(add_user, width=30)
    salary_entry.pack(pady=5)

    # Address 
    Label(add_user, text="Address : ").pack(pady=10)
    address_entry = Entry(add_user, width=30)
    address_entry.pack(pady=5)
        # submit button function 
    def submit_trainer():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        phone = phone_entry.get()
        salary = salary_entry.get()
        address = address_entry.get()

        if not all([first_name, last_name, phone, salary, address]):
            Label(add_user, text="Please fill all fields!", fg="red").pack(pady=10)
            return

        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO trainer (trainer_fname, trainer_lname, trainer_phone, trainer_salary, trainer_address)
            VALUES (?, ?, ?, ?, ?)
        """, (first_name, last_name, phone, salary, address))

        con.commit()
        con.close()

        Label(add_user, text="Trainer added successfully!", fg="green").pack(pady=10)

    Button(add_user,text="submit" , width=10 , command=submit_trainer).pack(side='bottom',pady=10)


#here for adding the user 
def add_user():
    add_user = Toplevel(root)
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


def new_window():
    new_window = Toplevel(root)
    new_window.geometry('1700x500')
    new_window.title('Start Menu')
    Label(new_window, text='Welcome back! What will you do today?').pack(pady=10)
    buttons = [
        ("Add User", add_user),
        ("View Users Details", view_user_window),
        ("Add Trainer", add_trainer),
        ("View Trainer Details", view_trainer_window)
    ]
    for text, command in buttons:
        Button(new_window, text=text, width=20, command=command).pack(pady=5)


Label(text='click next to continue').pack()
Label(text='maked by : ').pack(pady=5)


teamFrame = Frame(root)
teamFrame.pack(pady=10)
members = ['Mohamed Sarhan', 'Mohamed Alsaeed', 'Saif Yahia', 'Mina Nabile', 'Mohamed Esmail']
for member in members:
    Label(teamFrame, text=member).pack(pady=2)


Button(text="start" , command=new_window).pack(side="bottom",pady=20)


root.mainloop()

