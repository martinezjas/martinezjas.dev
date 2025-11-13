import sqlite3 as sql
from typing import Optional


def get_data(query: str) -> Optional[dict]:
    with sql.connect("static/himnario.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()

        if query.isdigit():
            query = int(query)
            res = cur.execute(
                "SELECT id, number, title FROM hymn WHERE id = ?", (query,)
            )
            out = res.fetchone()
            if not out:
                return None

            verses_data = cur.execute(
                "SELECT id, number from verse where hymnId = ? ORDER BY number ASC",  # noqa: E501
                (out["id"],),
            ).fetchall()

            verses_list = []
            for v in verses_data:
                contents = cur.execute(
                    "SELECT id, content FROM verseContent WHERE verseId = ? ORDER BY ordering ASC",  # noqa: E501
                    (v["id"],),
                ).fetchall()
                verses_list.append(
                    {
                        "id": v["id"],
                        "number": v["number"],
                        "contents": [
                            {"id": c["id"], "content": c["content"]}
                            for c in contents  # noqa: E501
                        ],
                    }
                )

            sequence_data = cur.execute(
                "SELECT vs.id, vs.timestamp, vs.verseContentId, vc.verseId FROM verseSequence vs INNER JOIN verseContent vc ON vc.id = vs.verseContentId INNER JOIN verse vv ON vv.id = vc.verseId WHERE vv.hymnId = ? ORDER BY vs.position ASC",  # noqa: E501
                (out["id"],),
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
            return result

        return None
