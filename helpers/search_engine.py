import sqlite3 as sql

def search(query):
    con = sql.connect('static/himnario.db')
    cur = con.cursor()
    out = None
    if query.isdigit():
        query = int(query)
        res = cur.execute("SELECT number, title FROM hymn WHERE number = ?", (query,))
        out = res.fetchone()
        if out:
            out = [f"Himno {out[0]}: {out[1]}"]
        else:
            out = []
    else:
        res = cur.execute("SELECT number, title FROM hymn WHERE title LIKE ?", (f"%{query}%",))
        out = res.fetchall()
        out = [f"Himno {i[0]}: {i[1]}" for i in out]
    con.close()
    return out