from database.connection import get_db_connection

class Author:
    TABLE_NAME = 'authors'

    def __init__(self, id, name):
        self._id = id
        self._name = name

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name 

    @name.setter
    def name(self, value):
        if hasattr(self, '_name'):
            raise AttributeError("Should not be changed after the author is instantiated")
        if not isinstance(value, str):
            raise TypeError("The author name should be a type of string.")
        if len(value) <= 0:
            raise ValueError("The author name must be longer than 0 characters")
        self._name = value


    def new_author(self):
        conn = get_db_connection()
        cursor = conn.cursor() 
        sql = f"INSERT INTO {self.TABLE_NAME} (name) VALUES (?)"
        cursor.execute(sql, (self._name,))
        conn.commit()
        self._id = cursor.lastrowid
        conn.close()
        

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = ''' 
           SELECT articles.* 
            FROM articles 
            JOIN authors ON article.author_id = author.id
            WHERE author_id =?
        '''
        cursor.execute(sql, (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles
    
    
    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT magazines.* 
            FROM magazines 
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """
        cursor.execute(sql, (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines
    
