from database import db_connection
from models.category import Category

class Todo:
    def __init__(self, id, text, category):
        self.id = id
        self.text = text
        self.category = category

def list_todos():
    conn = db_connection()
    db_todos = conn.execute('SELECT todos.id as tid, todo_text, categories.id as cid, category_name FROM todos JOIN categories ON todos.category_id = categories.id').fetchall()
    todos = []
    for db_todo in db_todos:
        todos.append(Todo(db_todo['tid'], db_todo['todo_text'], Category(db_todo['cid'], db_todo['category_name'])))

    conn.close()
    return todos

def insert_todo(text, category_id):
    conn = db_connection()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO todos (todo_text, category_id) VALUES (?, ?)', (text, category_id))
    conn.commit()
    conn.close()
