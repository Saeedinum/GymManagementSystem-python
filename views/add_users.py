from tkinter import Entry, Frame, Label, ttk
from tkinter.font import Font
from controllers.users import submit_user

def add_user(frame):
    # Clear previous content in left frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Define font style for labels
    label_font = Font(size=14)  # Font size 14
    background = '#000B58'
    text_color = 'white'

    # Function to create a labeled entry field
    def create_labeled_entry(parent, label_text, entry_width, **entry_options):
        container = Frame(parent, bg=background)
        container.pack(pady=10, fill="x")
        Label(container, text=label_text, font=label_font, fg=text_color, bg=background).pack(side="left", padx=10)
        entry = Entry(container, width=entry_width, background="#074799", font=label_font, bd=0, foreground=text_color)
        entry.pack(side="left", padx=10)
        return entry

    # Create labeled entry fields
    first_name_entry = create_labeled_entry(frame, "First Name:", 40)
    last_name_entry = create_labeled_entry(frame, "Last Name:", 40, )
    phone_entry = create_labeled_entry(frame, "Phone Number:", 40)
    trainer_name_entry = create_labeled_entry(frame, "Trainer Name:", 40)
    start_date_entry = create_labeled_entry(frame, "Start-Date:", 40)
    end_date_entry = create_labeled_entry(frame, "End-Date:", 40)
    price_entry = create_labeled_entry(frame, "Price:", 40)

    # Button Frame
    button_frame = Frame(frame, bg=background)
    button_frame.pack(pady=20)

    style = ttk.Style()
    style.configure("TButton",
                    font=Font(size=14),
                    background="white",
                    foreground="black",
                    padding=10)
    # style.map("TButton",
    #           background=[("active", "#218838"), ("pressed", "#1e7e34")],
    #           foreground=[("active", "white"), ("pressed", "white")])

    submit_button = ttk.Button(button_frame, text="Submit", style="TButton", command=lambda: submit_user(
        first_name_entry.get(),
        last_name_entry.get(),
        phone_entry.get(),
        trainer_name_entry.get(),
        start_date_entry.get(),
        end_date_entry.get(),
        price_entry.get(),
        frame,
        button_frame
    ))
    submit_button.grid(row=0, column=0, padx=10, pady=10)