import tkinter as tk
import sqlite3

# basic GUI
root = tk.Tk()
root.title('INTEGRATION')
root.geometry('300x350')

# new label and input
label_id = tk.Label(root, text='Student ID')
label_id.pack(pady=(15, 5))
entry_id = tk.Entry(root, width=25)
entry_id.pack()

label_name = tk.Label(root, text='Student NAME')
label_name.pack(pady=(10, 5))
entry_name = tk.Entry(root, width=25)
entry_name.pack()

# connect to database
conn = sqlite3.connect('Student.db')
cursor = conn.cursor()

# ensure table exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS DB_student (
    db_student_id TEXT PRIMARY KEY,
    db_student_name TEXT
)
''')
conn.commit()

# setting function
def print_student():
    student_id = entry_id.get()
    student_name = entry_name.get().lower()

    print('Student ID: {}'.format(student_id))
    print('Student_Name: {}'.format(student_name))
    print('-' * 30)

# new button: print
button_print = tk.Button(root, text='Print', command=print_student)
button_print.pack(pady=15)

# def a create_student()
def create_student():
    student_id = entry_id.get()
    student_name = entry_name.get()

    cursor.execute(
        'INSERT INTO DB_student (db_student_id, db_student_name) VALUES(?, ?)',
        (student_id, student_name),
    )
    conn.commit()

    print('Student ID: {}'.format(student_id))
    print('Student_Name: {}'.format(student_name))
    print('-' * 30)

button_create = tk.Button(root, text='Create', command=create_student)
button_create.pack(pady=20)

def overview_student():
    cursor.execute('SELECT * from DB_student')
    overview = cursor.fetchall()
    print(overview)

botton_overview = tk.Button(root, text='Overview', command=overview_student)
botton_overview.pack(pady=25)

root.mainloop()  # must be put the end of programming code


