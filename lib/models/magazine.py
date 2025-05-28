from connection import get_connection
from article import Article
from author import Author

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.strip():
            self._name = value
        else:
            raise ValueError("Magazine Name must be included and is a string.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and value.strip():
            self._category = value
        else:
            raise ValueError("Category must included and should be a valid string.")

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (self.name, self.category)
        )
        conn.commit()
        conn.close()

    @classmethod
    def get_by_id(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (magazine_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def get_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def get_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    # Relationship Methods

    def articles(self):
        return Article.find_all_by_magazine(self.id)

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(*row) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, COUNT(ar.id) as article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING article_count > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(*row[:2]) for row in rows]  