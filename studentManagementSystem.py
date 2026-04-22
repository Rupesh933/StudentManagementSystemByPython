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

if os.name == 'nt':
    import msvcrt

    def _getch():
        return msvcrt.getwch()
else:
    import tty
    import termios

    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def input_password(prompt='Enter password'):
    print(prompt, end='', flush=True)  # end for prevent new line and flush for immediately show data

    password = ''

    while True:
        char = _getch()
        if char in ('\r', '\n'):
            print()
            break
        elif char == '\x03':  # Ctrl+C
            raise KeyboardInterrupt
        elif char in ('\b', '\x7f'):  # backspace (Windows \b, Unix DEL)
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

def admin_login():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    username = input("Enter userName: ")
    password = input('Enter Password: ')
    
    cursor.execute('SELECT * FROM admin WHERE username=? AND password=?',(username, password))
    admin = cursor.fetchone()
    conn.close()

    if admin:
        print('\nLogin Successful!\n')
        return True
    else:
        print('\nInvalid Credentails! Try again\n')
        return False
    
# menu
def show_menu():
    while True:
        print('\n', '='*50)
        print('          MAIN MENU          ')
        print("="*50)
        print('1. Add Student')
        print('2. View Student')
        print('3. Update Student')
        print('4. Delete Student')
        print('5. Logout/Quit')
        print("="*50)

        choice = input('Enter your choice(1-5): ')
        if choice == '1':
            add_student()
        elif choice == '2':
            view_student()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print('\nLogining Out Successfully!!')
        else:
            print('\nInvalid Choice! Please Enter Valid Option..!!')

def add_student():
    pass
def view_student():
    pass
def update_student():
    pass
def delete_student():
    pass

def main():
    clear_screen()
    show_menu()

if __name__ == '__main__':
    main()