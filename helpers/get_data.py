import sqlite3 as sql


def get_data(query):
    con = sql.connect("static/himnario.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    out = None

    if query.isdigit():
        query = int(query)
        res = cur.execute("SELECT id, number, title FROM hymn WHERE id = ?", (query,))
        out = res.fetchone()
        if not out:
            con.close()
            return None

        verses_data = cur.execute(
            "SELECT id, number from verse where hymnId = ? ORDER BY number ASC",
            (out['id'],)
        ).fetchall()

        verses_list = []
        for v in verses_data:
            contents = cur.execute(
                "SELECT id, content FROM verseContent WHERE verseId = ? ORDER BY ordering ASC",
                (v['id'],)
            ).fetchall()
            verses_list.append(
                {
                    "id": v["id"],
                    "number": v["number"],
                    "contents": [
                        {"id": c["id"], "content": c["content"]} for c in contents
                    ],
                }
            )

        sequence_data = cur.execute(
            "SELECT vs.id, vs.timestamp, vs.verseContentId, vc.verseId FROM verseSequence vs INNER JOIN verseContent vc ON vc.id = vs.verseContentId INNER JOIN verse vv ON vv.id = vc.verseId WHERE vv.hymnId = ? ORDER BY vs.position ASC",
            (out['id'],)
        ).fetchall()

        result = {
            "id": out["id"],
            "number": out["number"],
            "title": out["title"],
            "verses": verses_list,
            "sequence": [
                {
                    "id": s["id"],
                    "timestamp": s["timestamp"],
                    "verseContentId": s["verseContentId"],
                    "verseId": s["verseId"],
                }
                for s in sequence_data
            ],
        }
        con.close()
        return result
    con.close()
    return None
