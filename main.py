import sqlite3

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

def main():
    with sqlite3.connect('products_info.db') as conn:
        init_db(conn)
        seed_data(conn)
        records = fetch_all_products(conn)
        print(records)

if __name__ == '__main__':
    main()