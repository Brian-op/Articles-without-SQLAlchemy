import sqlite3
from connection import get_connection


class Magazine:
    def __init__(self, id, name):
        self.id= id
        self.name= name


@classmethod
def get_id(cls,magazine_id):
    conn = get_connection()
    cursor =conn.cursor()
    cursor.execute("SELECT * FROM magazine WHERE id = ?"(magazine_id))
    rows = cursor.fetchall()
    conn.close()
    return rows