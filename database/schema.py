from .db_connection import get_connection

def initialize_schema():
    con = get_connection()
    cursor = con.cursor()

    # Trainer Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trainer (
        trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        trainer_fname TEXT NOT NULL,
        trainer_lname TEXT NOT NULL,
        trainer_phone TEXT NOT NULL,
        trainer_salary INTEGER NOT NULL,
        trainer_address TEXT NOT NULL
    );
    """)

    # Customer Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        trainer_id INTEGER NOT NULL,
        cust_fname TEXT NOT NULL,
        cust_lname TEXT NOT NULL,
        cust_phone TEXT NOT NULL,
        membership_start DATE NOT NULL,
        membership_end DATE NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id)
    );
    """)

    con.commit()
    con.close()
