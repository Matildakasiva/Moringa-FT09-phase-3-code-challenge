from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    TABLE_NAME = 'articles'

    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'
    
    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = f"INSERT INTO {self.TABLE_NAME} (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (self._title, self._content, self._author_id, self._magazine_id))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise Exception("Title must be a string")
        if len(value) < 5 or len(value) > 50:
            raise Exception("Title must be a string between 5 and 50 characters long")
        self._title = value

    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT authors.* 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id 
            WHERE articles.id =?
        """
        cursor.execute(sql, (self.id,))
        author = cursor.fetchone()
        conn.close()
        return Author(author[0], author[1]) if author else None

    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT magazines.* 
            FROM magazines 
            JOIN articles ON magazines.id = articles.magazine_id 
            WHERE articles.id =?
        """
        cursor.execute(sql, (self.id,))
        magazine = cursor.fetchone()
        conn.close()
        return Magazine(magazine[0], magazine[1], magazine[2]) if magazine else None
