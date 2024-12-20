from database.db_connection import get_connection 
from tkinter import * 
import sqlite3

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

# Function to get all trainers
def get_all_trainers():
    try:
        [con, cursor] = get_connection()
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
        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

# Function to search for trainers based on name or phone
def search_trainers(search_term):
    try:
        [con, cursor] = get_connection()
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
        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

# Function to delete a trainer by name
def delete_trainer_by_name(trainer_name):
    try:
        [con, cursor] = get_connection()
        cursor.execute("""
            DELETE FROM trainer 
            WHERE trainer_fname || ' ' || trainer_lname = ?
        """, (trainer_name,))
        con.commit()
        con.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
