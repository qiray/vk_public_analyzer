
import sqlite3

class DataBase(object):
    """Class for working with database"""

    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.names = ('Posts', 'Likes', 'Reposts', 'Comments', 'Views', 'Ads', 'Attachments')
        self.columns = ('likes_count', 'reposts_count', 'comments_count', 'views_count', 'marked_as_ads', 'attachments_count')
        self.attachments = ('Audios', 'Docs', 'Links', 'Photos', 'Polls', 'Videos')

    def get_names__and_columns(self):
        return self.names, self.columns

    def start_connection(self):
        """Open database and return connection with cursor to it"""
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        return conn, cursor

    def end_connecion(self, conn):
        """Commit and close connection to database"""
        conn.commit()
        conn.close()

    def select_all_text(self):
        conn, cursor = self.start_connection()
        sql = "SELECT text FROM posts"
        cursor.execute(sql)
        data = [x[0] for x in cursor.fetchall()]
        self.end_connecion(conn)
        return ' '.join(data)

    def get_common_data(self):
        conn, cursor = self.start_connection()
        cursor.execute("SELECT COUNT(), SUM(likes_count), SUM(reposts_count), SUM(comments_count),\
            SUM(views_count), SUM(marked_as_ads), SUM(attachments_count) from posts")
        result = cursor.fetchone()
        self.end_connecion(conn)
        return result, self.names, self.columns

    def get_column_data(self, column):
        conn, cursor = self.start_connection()
        cursor.execute("SELECT %s from posts" % (column))
        result = cursor.fetchall()
        self.end_connecion(conn)
        return [x[0] for x in result]

    def get_zero_data(self, column):
        conn, cursor = self.start_connection()
        cursor.execute("SELECT COUNT() from posts WHERE %s = 0" % (column))
        result = cursor.fetchone()
        self.end_connecion(conn)
        return result[0]

    def get_zero_texts(self):
        conn, cursor = self.start_connection()
        cursor.execute("SELECT COUNT() from posts WHERE LENGTH(text) = 0")
        result = cursor.fetchone()
        self.end_connecion(conn)
        return result[0]

    def get_texts_length(self):
        conn, cursor = self.start_connection()
        cursor.execute("SELECT LENGTH(text) from posts")
        result = cursor.fetchall()
        self.end_connecion(conn)
        return [x[0] for x in result]

    def get_top_data(self, column, top_count=10, find_max=True):
        extremum_type = "DESC" if find_max else "ASC"
        conn, cursor = self.start_connection()
        cursor.execute("SELECT %s, id FROM posts ORDER BY %s %s LIMIT %d" % (column, column, extremum_type, top_count))
        result = cursor.fetchall()
        self.end_connecion(conn)
        return result

    def get_top_texts(self, top_count=10, find_max=True):
        extremum_type = "DESC" if find_max else "ASC"
        conn, cursor = self.start_connection()
        cursor.execute("SELECT LENGTH(text), id FROM posts ORDER BY LENGTH(text) %s LIMIT %d" % (extremum_type, top_count))
        result = cursor.fetchall()
        self.end_connecion(conn)
        return result

    def get_attachments_types(self):
        conn, cursor = self.start_connection()
        cursor.execute("SELECT type, COUNT(type) FROM attachments GROUP BY type")
        result = cursor.fetchall()
        self.end_connecion(conn)
        return result, self.attachments

    def get_posts_by_authors(self):
        conn, cursor = self.start_connection()
        cursor.execute("SELECT signer_id, COUNT(signer_id), SUM(likes_count) FROM posts GROUP BY signer_id ORDER BY COUNT(signer_id) DESC")
        result = cursor.fetchall()
        self.end_connecion(conn)
        return result

    def get_posts_by_author(self, author_id):
        conn, cursor = self.start_connection()
        cursor.execute("SELECT likes_count, * FROM posts WHERE signer_id = %s" % (author_id))
        result = cursor.fetchall()
        self.end_connecion(conn)
        return result
