
import sqlite3

def start_connection(dbpath):
    """Open database and return connection with cursor to it"""
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    return conn, cursor

def end_connecion(conn):
    """Commit and close connection to database"""
    conn.commit()
    conn.close()

def select_all_text(dbpath):
    conn, cursor = start_connection(dbpath)
    sql = "SELECT text FROM posts"
    cursor.execute(sql)
    data = [x[0] for x in cursor.fetchall()]
    end_connecion(conn)
    return ' '.join(data)

def get_common_data(dbpath):
    conn, cursor = start_connection(dbpath)
    cursor.execute("SELECT COUNT(), SUM(likes_count), SUM(reposts_count), SUM(comments_count), SUM(views_count), SUM(marked_as_ads) from posts")
    result = cursor.fetchone()
    cursor.execute("SELECT COUNT() from attachments")
    result += cursor.fetchone()
    end_connecion(conn)
    names = ('Posts', 'Likes', 'Reposts', 'Comments', 'Views', 'Ads', 'Attachments')
    return result, names

