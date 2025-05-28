import sqlite3
from connection import get_connection
from author import Author
from magazine import Magazine

class Article:
    def __init__(self, id, title, author_id, magazine_id ):
        self.id = id
        self.author_id = author_id
        self.title= title
        self.magazine_id =magazine_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and value.strip():
            self._title = value
        else:
            raise ValueError("Article Title must be placed and it should be a string.")
        


    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (self.title, self.author_id, self.magazine_id)
        )
        conn.commit()
        conn.close()

    @classmethod
    def get_article_by_id(cls,article_id):
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
    
    