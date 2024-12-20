from database.db_connection import get_connection 
from tkinter import * 


def fetch_all_trainers():
    [con, cursor] = get_connection()
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

def submit_trainer(first_name, last_name, phone, salary, address, add_user):

    if not all([first_name, last_name, phone, salary, address]):
        Label(add_user, text="Please fill all fields!", fg="red", bg='#000B58').pack(pady=10)
        return

    [con, cursor] = get_connection()
    cursor.execute("""
        INSERT INTO trainer (trainer_fname, trainer_lname, trainer_phone, trainer_salary, trainer_address)
        VALUES (?, ?, ?, ?, ?)
    """, (first_name, last_name, phone, salary, address))

    con.commit()
    con.close()

    Label(add_user, text="Trainer added successfully!", fg="green").pack(pady=10)
