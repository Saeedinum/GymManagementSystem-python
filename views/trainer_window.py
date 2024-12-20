from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from controllers.trainer import delete_trainer_by_name, get_all_trainers, search_trainers

def view_trainer_window(frame):

    for widget in frame.winfo_children():
        widget.destroy()

    # Adding a Treeview for displaying trainer details
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


    tree = ttk.Treeview(frame, columns=("ID", "Name", "Phone", "Salary", "Address"), style="Custom.Treeview", show="headings", height=15)
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

    container = Frame(frame, background='#000B58')
    container.pack(pady=10, fill="x")
    Label(container, text="Search by Name or Phone:",  fg="white", bg='#000B58').pack(side="left", padx=10)
    search_entry = Entry(container, width=30, background="#074799",  bd=0, fg="white")
    search_entry.pack(side="left", padx=10)

    container = Frame(frame, background='#000B58')
    container.pack(pady=10, fill="x")
    Label(container, text="Delete Trainer :",  fg="white", bg='#000B58').pack(side="left", padx=10)
    delete_entry = Entry(container, width=30, background="#074799",  bd=0, fg="white")
    delete_entry.pack(side="left", padx=10)

    # Function to display all trainers initially
    def display_all_trainers():
        for row in tree.get_children():
            tree.delete(row)

        rows = get_all_trainers()

        if rows:
            for row in rows:
                tree.insert("", END, values=row)
        else:
            showinfo("No Data", "No trainers found in the database.")

    # delete trainer method
    def delete_trainer():
        trainer_name = delete_entry.get().strip()  # Get the name from the delete entry field
        delete_trainer_by_name(trainer_name)  # Call the database function to delete the trainer
        display_all_trainers()  # Refresh the Treeview to show the updated list

    # Function to search trainers
    def search_trainers_fn():
        search_term = search_entry.get()
        if not search_term:
            display_all_trainers()
            return

        for row in tree.get_children():
            tree.delete(row)

        rows = search_trainers(search_term)

        if rows:
            for row in rows:
                tree.insert("", END, values=row)
        else:
            showinfo("No Results", "No trainers found matching the search term.")

    # Initial display of all trainers
    display_all_trainers()

    # Adding buttons
    Button(frame, text="Search", width=20, command=search_trainers_fn, background='#000B58', fg="white").pack(side="left", padx=10, pady=10)
    Button(frame, text="Delete", width=20, command=delete_trainer, background='#000B58', fg="white").pack(side="left", padx=10, pady=10)
