
import sqlite3

class DataBase(object):
    """Class for working with database"""

    def __init__(self, dbpath):
        self.dbpath = dbpath

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
        cursor.execute("SELECT COUNT(), SUM(likes_count), SUM(reposts_count), SUM(comments_count), SUM(views_count), SUM(marked_as_ads) from posts")
        result = cursor.fetchone()
        cursor.execute("SELECT COUNT() from attachments")
        result += cursor.fetchone()
        self.end_connecion(conn)
        names = ('Posts', 'Likes', 'Reposts', 'Comments', 'Views', 'Ads', 'Attachments')
        return result, names

    def get_column_data(self, column):
        conn, cursor = self.start_connection()
        cursor.execute("SELECT %s from posts" % (column))
        result = cursor.fetchall()
        self.end_connecion(conn)
        return [x[0] for x in result]
