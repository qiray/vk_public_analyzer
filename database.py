
import sqlite3

def select_all_text(dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    sql = "SELECT text FROM posts"
    cursor.execute(sql)
    data = [x[0] for x in cursor.fetchall()]
    conn.commit()
    conn.close()
    return ' '.join(data)

