# Student Management System (Python + SQLite)

A simple console-based Student Management System I built in Python while learning
SQLite and basic CLI app structure. It runs right in your terminal — no web UI,
no extra dependencies — just Python and a local database file.

It lets an admin log in, then add / view / update / delete students.

---

## What can it do?

- **Admin login** — the very first time you run the program, it asks you to create
  an admin username and password. The password is hidden while you type (shown as
  `*`) and stored as a **SHA-256 hash**, not plain text.
- **Add a student** — collects student ID, name, grade, gender, DOB, degree,
  stream, phone, email and address, and saves them to the database.
- **View all students** — prints every student in a nicely formatted table.
- **Update a student** — look up by student ID and edit any field. If you leave
  a field blank it keeps the old value.
- **Delete a student** — look up by student ID, ask for confirmation, and remove.
- **Cross-platform password input** — works on both Windows (`msvcrt`) and
  Linux/macOS (`termios` + `tty`).

---

## Tech stack

- **Python 3** (standard library only — no `pip install` needed)
- **SQLite** (comes with Python via the `sqlite3` module)
- Modules used: `os`, `sys`, `sqlite3`, `hashlib`, `msvcrt` (Windows only),
  `tty` + `termios` (Linux/macOS only)

---

## Project structure

```
StudentManagentSystemByPython/
├── studentManagementSystem.py   # the whole app lives here
├── students.db                  # created automatically on first run
└── README.md                    # you are here
```

---

## How to run it

### 1. Make sure you have Python 3

```bash
python --version
# or
python3 --version
```

If it shows something like `Python 3.x.x` you are good to go.

### 2. Clone or download this project

```bash
git clone <your-repo-url>
cd StudentManagentSystemByPython
```

### 3. Run it

```bash
python studentManagementSystem.py
```

On the **first run** it will ask you to create an admin account:

```
=== ADMIN SETUP ===
Create Admin Username: admin
Create Admin Password: ********
```

On every run after that, it just asks you to log in.

---

## Database

The app uses a single SQLite file called `students.db`, which is created
automatically the first time you run the program. You never need to create it
manually.

### `admin` table
| column   | type    | notes                 |
|----------|---------|-----------------------|
| id       | INTEGER | primary key           |
| username | TEXT    |                       |
| password | TEXT    | stored as SHA-256 hash |

### `students` table
| column      | type    | notes        |
|-------------|---------|--------------|
| id          | INTEGER | primary key  |
| student_id  | TEXT    | must be UNIQUE |
| name        | TEXT    |              |
| grade       | TEXT    |              |
| gender      | TEXT    | Male / Female |
| dob         | TEXT    | format: DD-MM-YYYY |
| degree      | TEXT    |              |
| stream      | TEXT    |              |
| phone       | TEXT    |              |
| email       | TEXT    |              |
| address     | TEXT    |              |

> If you ever want to start fresh (for example, you forgot the admin password),
> just delete `students.db` and run the program again. A brand-new empty
> database will be created.

---

## Menu

Once you log in, the main menu shows up:

```
==================================================
          MAIN MENU
==================================================
1. Add Student
2. View Student
3. Update Student
4. Delete Student
5. Logout/Quit
==================================================
Enter your choice(1-5):
```

Type a number and press **Enter**. If you type something that isn't `1`–`5` it
just tells you "Invalid Choice" and shows the menu again.

---

## Things I learned building this

- How to use `sqlite3` from Python — `connect`, `cursor`, `execute`, `commit`,
  `close`.
- Why you should **never** use string formatting to build SQL queries — always
  use `?` placeholders so SQL injection can't happen and special characters in
  input don't break things.
- `input()` in Python **always returns a string**, so menu comparisons use
  `'1'` and not `1`.
- Password hashing with `hashlib` — you store the hash, and on login you hash
  what the user typed and compare hashes. The password itself is never stored.
- Reading a single character from the terminal is very different on Windows
  vs. Linux — Windows has `msvcrt`, Unix needs `tty` + `termios`.
- `UPDATE` and `DELETE` **must** have a `WHERE` clause — otherwise they hit
  every row in the table. (Found this out the fun way.)
- Always close database connections, even in the "not found" / error paths.

---

## Known limitations / things I might add later

- [ ] **Search** for a student by name or partial match
- [ ] **Sort / filter** the view (by grade, by degree, etc.)
- [ ] Let you **change the admin password** from inside the app
- [ ] Add **multiple admin users**
- [ ] Add a small **salt** to the password hash (right now it's plain SHA-256)
- [ ] **Input validation** — e.g. make sure email looks like an email, phone
      is digits only, DOB is a real date
- [ ] **Export** the student list to CSV
- [ ] **Pagination** when the list of students gets too long to fit on screen

---

## Notes for first-time Python users

- You do **not** need to install anything with `pip`. Everything this project
  uses ships with Python itself.
- You do **not** need to set up a database server. SQLite is just a file.
- If you get `ModuleNotFoundError: No module named 'msvcrt'`, you are running
  on Linux or macOS and the code already handles that — make sure you have the
  latest version of `studentManagementSystem.py`.

---

Thanks for checking out the project! It's a learning project, so if you spot
something that could be cleaner or more correct, feel free to open an issue or
send a PR.
