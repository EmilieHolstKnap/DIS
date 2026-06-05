from database import db_connection

class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

def list_categories():
    conn = db_connection()
    db_categories = conn.execute('SELECT id, category_name FROM categories').fetchall()
    categories = []
    for db_category in db_categories:
        categories.append(Category(db_category['id'], db_category['category_name']))
    conn.close()
    return categories

def insert_category(category_name):
    conn = db_connection()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO categories (category_name) VALUES (?)', (category_name,))
    conn.commit()
    conn.close()
