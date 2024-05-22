import sqlite3
from datetime import date, datetime

def valid_birthday(birthday):
    current_date = date.today()
    try:
        birth_date = datetime.strptime(birthday, '%m/%d/%Y').date()
        if birth_date < date(1920, 1, 1) or birth_date > current_date:
            return False
        return True
    except ValueError:
        return False
def get_next_employee_number(db: sqlite3.Connection) -> int:
    cursor = db.cursor()
    cursor.execute("SELECT MAX(employee_number) FROM users")
    result = cursor.fetchone()
    max_employee_number = result[0]
    if max_employee_number is None:
        return 1  # If there are no users, start with 1
    return max_employee_number + 1

def add_user_to_db(db: sqlite3.Connection, first_name: str, last_name: str, birthday: str, employee_number: int):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (first_name, last_name, birthday, employee_number) VALUES (?, ?, ?, ?)",
        (first_name, last_name, birthday, employee_number)
    )
    db.commit()

def get_all_users(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute("SELECT id, first_name, last_name, birthday, employee_number FROM users")
    users = cursor.fetchall()
    return [dict(id=row[0], first_name=row[1], last_name=row[2], birthday=row[3], employee_number=row[4]) for row in users]

def get_next_employee_number(db):
    cursor = db.cursor()
    cursor.execute('SELECT MAX(employee_number) FROM users')
    max_emp_number = cursor.fetchone()[0]
    if max_emp_number is None:
        return 1
    return max_emp_number + 1
