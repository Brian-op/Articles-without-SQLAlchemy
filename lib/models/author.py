import sqlite3
from connection import get_connection

class Author :
    def __init__(self, id , name):
        self.id = id
        self.name =name

    @classmethod
    def get_by_id(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?",(author_id,))
        rows = cursor.fetchone()
        conn.close()
        return cls(*rows) if rows else None
    
    @classmethod
    def get_articles(self):
        conn = get_connection( )
        cursor =conn.cursor()
        cursor.execute("SELECT * FROM articles  WHERE id =?",(self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles
    