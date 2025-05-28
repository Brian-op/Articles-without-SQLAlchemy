from connection import get_connection
from lib.models.article import Article
from lib.models.magazine import Magazine

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
    def get_by_name(cls, name):
        conn= get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls (*row)if row else None
     
    def get_articles(self):
        conn = get_connection( )
        cursor =conn.cursor()
        cursor.execute("SELECT * FROM articles  WHERE author_id =?",(self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(*row)for row in rows]
