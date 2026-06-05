import sqlite3

def db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db_connection()
    # We have a new table for the todo categories
    conn.execute('''CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, category_name TEXT NOT NULL UNIQUE)''')
    # Now we have a foreign key to the categories
    conn.execute('''CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY AUTOINCREMENT, todo_text TEXT NOT NULL UNIQUE, category_id INTEGER NOT NULL, FOREIGN KEY(category_id) REFERENCES categories(id))''')

    c = conn.cursor()
    categories = ['DIS', 'House chores']
    for category in categories:
        c.execute('INSERT OR IGNORE INTO categories (category_name) VALUES (?)', (category,))

    todos = [('Assignment 1', 'DIS'), ('Groceries', 'House chores'), ('Assignment 2', 'DIS'), ('Project', 'DIS')]
    for (todo, category) in todos:
        c.execute('INSERT OR IGNORE INTO todos (todo_text, category_id) VALUES (?, (SELECT id FROM categories WHERE category_name = ?))', (todo, category))

    conn.commit()
    conn.close()
