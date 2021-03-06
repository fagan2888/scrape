from books.database.utils.database_connection import DatabaseConnection
import sqlite3
import pickle
import sys
sys.setrecursionlimit(100000)

# should be storing book parser objs
def create_db():
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS books(title text primary key, rating text, availability text, price real, book_obj blob)')


def add_books(title, rating, availability, price, book_obj):
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO books VALUES (?,?,?,?,?)', (title, rating, availability, price, pickle.dumps(book_obj)))
        except sqlite3.IntegrityError as e:
            print("book already exists")

def get_books():
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT book_obj FROM books')
        books = [pickle.loads(x[0]) for x in cursor.fetchall()]
    return books

def list_books():
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT* FROM books')
        books = [{"Title": row[0], 'Rating': row[1], 'Stock': row[2], "Price": row[3]} for row in cursor.fetchall()]
    return books


def delete_books(title):
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM books WHERE title = ?', (title, _))
