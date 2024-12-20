import sqlite3 
from tkinter import * 
from tkinter import ttk
from tkinter.messagebox import showinfo

from database.schema import initialize_schema
from views.trainer_window import view_trainer_window
from views.bill_window import view_bill_window
from views.user_window import view_user_window
from controllers.trainer import add_trainer
from controllers.users import add_user


initialize_schema()

root = Tk() 
root.geometry('1700x500') 
root.title('over View') 

Label(root, text='Welcome back! What will you do today?').pack(pady=10)
buttons = [
    ("Add User", add_user),
    ("View Users Details", view_user_window),
    ("Add Trainer", add_trainer),
    ("View Trainer Details", view_trainer_window)
]

for text, command in buttons:
    Button(root, text=text, width=20, command=command).pack(pady=5)


root.mainloop()

