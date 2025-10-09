import sqlite3
import tkinter as tk

def init_db(conn):
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        category TEXT,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    )
    ''')
    conn.commit()

def seed_data(conn):
    products = [
        ('筆記型電腦', '高效能筆電，16GB RAM', 35900, 10, '電子產品'),
        ('滑鼠', '無線藍芽滑鼠', 590, 50, '周邊設備'),
        ('鍵盤', '機械式鍵盤，青軸', 1290, 30, '周邊設備'),
    ]
    cur = conn.cursor()
    cur.executemany('''
    INSERT INTO products (name, description, price, stock, category)
    VALUES (?, ?, ?, ?, ?)
    ''', products)
    conn.commit()

def fetch_all_products(conn):
    cur = conn.cursor()
    cur.execute('SELECT id, name, description, price, stock, category, created_at FROM products')
    return cur.fetchall()

# --- Student DB bootstrap ---
def init_student_db(conn_student):
    cur = conn_student.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS DB_student (
        db_student_id TEXT PRIMARY KEY,
        db_student_name TEXT NOT NULL
    )
    ''')
    conn_student.commit()


# --- Tkinter GUI for Student Management ---
def launch_student_gui():
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

    # connect to student database and ensure table
    conn_student = sqlite3.connect('Student.db')
    cursor_student = conn_student.cursor()
    init_student_db(conn_student)

    # setting function
    def print_student():
        student_id = entry_id.get()
        student_name = entry_name.get().lower()

        print('Student ID: {}'.format(student_id))
        print('Student_Name: {}'.format(student_name))
        print('-' * 30)

    # create student
    def create_student():
        student_id = entry_id.get()
        student_name = entry_name.get()

        cursor_student.execute(
            'INSERT INTO DB_student (db_student_id, db_student_name) VALUES(?, ?)',
            (student_id, student_name)
        )
        conn_student.commit()

        print('Student ID: {}'.format(student_id))
        print('Student_Name: {}'.format(student_name))
        print('-' * 30)

    def overview_student():
        cursor_student.execute('SELECT * from DB_student')
        overview = cursor_student.fetchall()
        print(overview)

    # buttons
    button_print = tk.Button(root, text='Print', command=print_student)
    button_print.pack(pady=15)

    button_create = tk.Button(root, text='Create', command=create_student)
    button_create.pack(pady=20)

    button_overview = tk.Button(root, text='Overview', command=overview_student)
    button_overview.pack(pady=25)

    def on_close():
        try:
            cursor_student.close()
        except Exception:
            pass
        conn_student.close()
        root.destroy()

    root.protocol('WM_DELETE_WINDOW', on_close)
    root.mainloop()


def main():
    # Initialize and seed products DB (existing behavior), then launch GUI
    with sqlite3.connect('products_info.db') as conn:
        init_db(conn)
        seed_data(conn)
        records = fetch_all_products(conn)
        print(records)
    launch_student_gui()

if __name__ == '__main__':
    main()