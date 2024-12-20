from database.db_connection import get_connection
import sqlite3 
from tkinter import * 
from tkinter import ttk
from tkinter.messagebox import showinfo


def fetch_all_trainers():
    con = get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT 
            trainer_id,
            trainer_fname || ' ' || trainer_lname AS name,
            trainer_phone,
            trainer_salary,
            trainer_address
        FROM trainer;
    """)
    trainers = cursor.fetchall()
    con.close()
    return trainers

def add_trainer():
    add_user = Toplevel(Tk())
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

