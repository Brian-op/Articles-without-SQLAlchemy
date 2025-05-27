import sqlite3
from connection import get_connection

class Articles:
    def __init__(self, id, title, content, author_id, magazine_id ):
        self.id = id
        self.author_id = author_id
        self.title= title
        self.content= content
        self.magazine_id =magazine_id

    @classmethod
    def get_by_id(cls,article_id):
        conn =get_connection()
        cursor =conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id= ?", (article_id))
        rows =cursor.fetchone()
        conn.close()
        return cls(*rows) if rows else None

    # foreign keys  AKA RELATIONSHIP
    def get_author(self):
        from author import Author
        return Author.get_by_id(self.author_id)
    
    def get_magazine(self):
        from magazine import Magazine
        return Magazine.get_by_id(self.magazine_id)
    
    