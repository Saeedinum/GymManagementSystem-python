from tkinter import *
from tkinter import ttk
from database.schema import initialize_schema
from views.trainer_window import view_trainer_window
from views.user_window import view_user_window
from controllers.trainer import add_trainer
from controllers.users import add_user

initialize_schema()

root = Tk()
root.geometry('1700x800')
root.resizable(width=False, height=False)
root.title('GYM Management System')
root.config(bg='#000B58')

right_frame = Frame(root, bg='#000B58')
right_frame.pack(side="right", fill="y", padx=10, pady=10)

style = ttk.Style()

style.configure("Rounded.TButton",
                font=('Arial', 12, 'bold'),
                padding=5,
                background='#000B58',
                foreground='#000B58',
                relief="flat",
                borderwidth=10,
                width=15)

def create_button(frame, text, command):
    button = ttk.Button(
        frame,
        text=text,
        command=command,
        style="Rounded.TButton"
    )
    button.pack(pady=10, padx=10, fill='x')
    return button

create_button(right_frame, "Add User", lambda: add_user(left_frame))
create_button(right_frame, "View Users", view_user_window)
create_button(right_frame, "Add Trainer", add_trainer)
create_button(right_frame, "View Trainer", view_trainer_window)

left_frame = Frame(root, bg='#000B58')
left_frame.pack(side="left", expand=True, fill="both")


root.mainloop()
