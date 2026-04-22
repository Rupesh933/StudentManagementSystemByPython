import os
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')    # nt is for window


import sqlite3
def initialize_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()   # cursor() is used for CRUD operation

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
                   )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   student_id TEXT NOT NULL UNIQUE,
                   name TEXT NOT NULL,
                   grade TEXT NOT NULL,
                   gender TEXT NOT NULL,
                   dob TEXT NOT NULL,
                   degree TEXT NOT NULL,
                   stream TEXT NOT NULL,
                   phone INTEGER NOT NULL,
                   email EMAIL NOT NULL,
                   address TEXT NOT NULL
                   )
    ''')
    conn.commit()
    conn.close()

initialize_database()

# function for generate hashable password
import sys
import msvcrt
def input_password(prompt='Enter password'):
    print(prompt, end='', flush=True)  # end for prevent new line and flush for immediately show data
    
    password = ''

    while True:
        char = msvcrt.getwch()
        if char in ['\r', '\n']:
            print()
            break
        elif char == '\b':  # \b means backspace
            if password:
                sys.stdout.write('\b \b')
                sys.stdout.flush()
            password = password[:-1]
        else:
            sys.stdout.write("*")
            sys.stdout.flush()
            password += char 
    return password 


def create_admin_if_not_exits():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin")
    existing_admin = cursor.fetchone()

    if not existing_admin:
        print("\n=== ADMIN SETUP ===")
        username = input('Create Admin Username: ')
        password = input_password('Create Admin Password: ')

        cursor.execute("INSERT INTO admin (username, password) values(?,?)", (username, password))
        conn.commit()
        print('\nAdmin Create Successfully')
        conn.close()

def main():
    clear_screen()

if __name__ == '__main__':
    main()