from tkinter import Button, Entry, Frame, Label

from controllers.users import submit_user

def add_user(frame):
    # Clear previous content in left frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Add User Form
    Label(frame, text="First Name:").pack(pady=10)
    first_name_entry = Entry(frame, width=30)
    first_name_entry.pack(pady=5)

    Label(frame, text="Last Name:").pack(pady=10)
    last_name_entry = Entry(frame, width=30)
    last_name_entry.pack(pady=5)

    Label(frame, text="Phone Number:").pack(pady=10)
    phone_entry = Entry(frame, width=30)
    phone_entry.pack(pady=5)

    Label(frame, text="Trainer Name:").pack(pady=10)
    trainer_name_entry = Entry(frame, width=30)
    trainer_name_entry.pack(pady=5)

    Label(frame, text="Start-Date : ").pack(pady=10)
    start_date_entry = Entry(frame, width=30)
    start_date_entry.pack(pady=5)

    Label(frame, text="End-Date : ").pack(pady=10)
    end_date_entry = Entry(frame, width=30)
    end_date_entry.pack(pady=5)

    Label(frame, text="Price : ").pack(pady=10)
    price_entry = Entry(frame, width=30)
    price_entry.pack(pady=5)

    button_frame = Frame(frame)
    button_frame.pack(pady=20)

    Button(button_frame, text="Submit", width=10, command=submit_user (
        first_name_entry.get(),
        last_name_entry.get(),
        phone_entry.get(),
        trainer_name_entry.get(),
        start_date_entry.get(),
        end_date_entry.get(),
        price_entry.get(),
        frame,
        button_frame
    ) ).grid(row=0, column=0, padx=10, pady=10)
