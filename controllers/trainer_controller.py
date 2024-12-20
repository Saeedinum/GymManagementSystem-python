from database.db_connection import get_connection

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
