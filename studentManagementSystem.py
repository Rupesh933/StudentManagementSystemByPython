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
                   phone TEXT NOT NULL,
                   email TEXT NOT NULL,
                   address TEXT NOT NULL
                   )
    ''')
    conn.commit()
    conn.close()

initialize_database()

# function for generate hashable password
import sys
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

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


def create_admin_if_not_exists():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin")
    existing_admin = cursor.fetchone()

    if not existing_admin:
        print("\n=== ADMIN SETUP ===")
        username = input('Create Admin Username: ')
        password = input_password('Create Admin Password: ')

        cursor.execute("INSERT INTO admin (username, password) values(?,?)", (username, hash_password(password)))
        conn.commit()
        print('\nAdmin Create Successfully')
    conn.close()

def admin_login():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    username = input("Enter userName: ")
    password = input_password('Enter Password: ')

    cursor.execute('SELECT * FROM admin WHERE username=? AND password=?', (username, hash_password(password)))
    admin = cursor.fetchone()
    conn.close()

    if admin:
        print('\nLogin Successful!\n')
        return True
    else:
        print('\nInvalid Credentials! Try again\n')
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
            print('\nLogging Out Successfully!!')
            break
        else:
            print('\nInvalid Choice! Please Enter Valid Option..!!')

def add_student():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    print('\n=== ADD NEW STUDENT ===')
    student_id = input('\nEnter Student ID: ')
    name = input('\nEnter your Name: ')
    grade = input('\nEnter your Grade: ')
    gender = input('\nEnter your Gender (Male/Female): ').strip().capitalize()
    while gender not in ['Male', 'Female']:
        print("\nInvalid input! Please enter 'Male' or 'Female'.")
        gender = input('\nEnter your Gender (Male/Female): ').strip().capitalize()
    dob = input('\nEnter your DOB (DD-MM-YYYY): ')
    degree = input('\nEnter your Degree: ')
    stream = input('\nEnter your Stream: ')
    phone = input('\nEnter your Phone: ')
    email = input('\nEnter your Email: ')
    address = input('\nEnter Your Address: ')

    try:
        cursor.execute('''
            INSERT INTO students (student_id, name, grade, gender, dob, degree, stream, phone, email, address) VALUES(?,?,?,?,?,?,?,?,?,?)
            ''', (student_id, name, grade, gender, dob, degree, stream, phone, email, address))
        conn.commit()
        print('\nStudent Add Successfully')
    
    except sqlite3.IntegrityError:
        print('\nError: student_id must be unique')
    except Exception as e:
        print('\nSomething went wrong', e)
    
    conn.commit()
    print('\n===Add New Student===')



def view_student():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()

    if not students:
        print('\nNo Student found!\n')
        return
    
    print('\n' + '='*70)
    print(f'{'ID':<5} {'Student ID':<10} {'Name':<20} {'Grade':<10} {'Gender':<10} {'DOB':<20} {'Degree':<15} {'Stream':<15} {'Phone':<13} {'Email':<22} {'Address':<30}')

    for student in students:
        print(f'{student[0]:<5} {student[1]:<10} {student[2]:<20} {student[3]:<10} {student[4]:<10} {student[5]:<20} {student[6]:<15} {student[7]:<15} {student[8]:<13} {student[9]:<22} {student[10]:<30}') 
    
    print('='*70)


def update_student():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    student_id = input('Enter Student ID to update: ')

    cursor.execute('SELECT * FROM students WHERE student_id=?',(student_id,))
    student = cursor.fetchone()

    if not student:
        print('\nStudent Not Found!!\n')
        conn.close()
        return

    print('\n=== Update Student Details ===')
    print('Leave blank to keep current value: ')

    name = input(f'Enter new Name [{student[2]}]: ') or student[2]
    grade = input(f'Enter new Grade [{student[3]}]: ') or student[3]
    gender = input(f'Enter new Gender [{student[4]}]: ') or student[4]
    dob = input(f'Enter new DOB [{student[5]}]: ') or student[5]
    degree = input(f'Enter new Degree [{student[6]}]: ') or student[6]
    stream = input(f'Enter new Stream [{student[7]}]: ') or student[7]
    phone = input(f'Enter new Phone [{student[8]}]: ') or student[8]
    email = input(f'Enter new Email [{student[9]}]: ') or student[9]
    address = input(f'Enter new Address [{student[10]}]: ') or student[10]

    cursor.execute('''
        UPDATE students SET name=?, grade=?, gender=?, dob=?, degree=?, stream=?, phone=?, email=?, address=?
        WHERE student_id=?
        ''', (name, grade, gender, dob, degree, stream, phone, email, address, student_id))
    conn.commit()
    conn.close()
    print('\nStudent Details Successfully Updated..!!')

def delete_student():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    student_id = input('\nEnter Student ID to delete: ')
    cursor.execute('SELECT * FROM students WHERE student_id=?', (student_id,))
    student = cursor.fetchone()

    if not student:
        print('\nStudent Not Found!!\n')
        conn.close()
        return
    confirm = input(f'Are you sure you want to delete {student[2]} (yes/no): ').strip().lower()

    if confirm == 'yes':
        cursor.execute('DELETE FROM students WHERE student_id=?', (student_id,))
        conn.commit()
        print('\nStudent Deleted successfully..!!\n')
    else:
        print('\nDeletion Cancelled\n')
    conn.close()


def main():
    clear_screen()
    create_admin_if_not_exists()
    while not admin_login():
        pass
    show_menu()

if __name__ == '__main__':
    main()