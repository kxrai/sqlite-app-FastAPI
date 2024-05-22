import sqlite3

def get_db():
    try:
        db = sqlite3.connect('myList.db', check_same_thread=False)
        yield db
    finally:
        db.close()

def create_table():
    db = sqlite3.connect('myList.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT,
                        last_name TEXT,
                        birthday TEXT,
                        employee_number INTEGER
                      )''')
    db.commit()
    db.close()
