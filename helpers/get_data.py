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

            # Optimized: Fetch all verses with their content in a single JOIN query  # noqa: E501
            # This eliminates the N+1 query problem
            verse_content_data = cur.execute(
                """
                SELECT
                    v.id as verse_id,
                    v.number as verse_number,
                    vc.id as content_id,
                    vc.content,
                    vc.ordering
                FROM verse v
                LEFT JOIN verseContent vc ON vc.verseId = v.id
                WHERE v.hymnId = ?
                ORDER BY v.number ASC, vc.ordering ASC
                """,  # noqa: E501
                (out["id"],),
            ).fetchall()

            # Group the results by verse
            verses_dict = {}
            for row in verse_content_data:
                verse_id = row["verse_id"]
                if verse_id not in verses_dict:
                    verses_dict[verse_id] = {
                        "id": verse_id,
                        "number": row["verse_number"],
                        "contents": [],
                    }
                # Add content if it exists (LEFT JOIN may have NULL content)
                if row["content_id"] is not None:
                    verses_dict[verse_id]["contents"].append(
                        {"id": row["content_id"], "content": row["content"]}
                    )

            verses_list = list(verses_dict.values())

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
