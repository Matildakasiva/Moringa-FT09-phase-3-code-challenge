from database.connection import get_db_connection

class Magazine:
    TABLE_NAME = 'magazines'

    def __init__(self, id=None, name=None, category=None):
        self._id = id
        self._name = name
        self._category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("The magazine name should be a string")
        if len(value) < 2 or len(value) > 16:
            raise ValueError("The magazine name should have characters between 2 and 16, inclusive")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if not isinstance(new_category, str):
            raise ValueError("The magazine category should be a string")
        if len(new_category) == 0:
            raise ValueError("The magazine category should have characters longer than 0, inclusive")
        self._category = new_category

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = f"INSERT INTO {self.TABLE_NAME} (name, category) VALUES (?, ?)"
        cursor.execute(sql, (self._name, self._category))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = ''' 
            SELECT articles.* 
            FROM articles 
            WHERE magazine_id = ?
        '''
        cursor.execute(sql, (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT authors.* 
            FROM authors 
            JOIN authors_articles ON authors.id = authors_articles.author_id 
            JOIN articles ON authors_articles.article_id = articles.id 
            WHERE articles.magazine_id = ?
        """
        cursor.execute(sql, (self._id,))
        contributors = cursor.fetchall()
        conn.close()
        return contributors
    
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT title 
            FROM articles 
            WHERE magazine_id = ?
        """
        cursor.execute(sql, (self.id,))
        titles = cursor.fetchall()
        conn.close()
        return titles if titles else None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT authors.* 
            FROM authors 
            JOIN (
                SELECT author_id 
                FROM authors_articles 
                JOIN articles ON authors_articles.article_id = articles.id 
                WHERE articles.magazine_id = ? 
                GROUP BY author_id 
                HAVING COUNT(*) > 2
            ) AS contributing_authors ON authors.id = contributing_authors.author_id
        """
        cursor.execute(sql, (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return authors if authors else None