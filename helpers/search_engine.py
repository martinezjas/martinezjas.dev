"""Search engine for hymn database with accent-insensitive matching."""

import sqlite3 as sql
import unicodedata
from typing import Optional


def remove_accents(text: Optional[str]) -> Optional[str]:
    """Remove accents from unicode string."""
    if text is None:
        return None
    # Normalize to NFD (decomposed form) and filter out combining characters
    nfd = unicodedata.normalize("NFD", text)
    return "".join(char for char in nfd if unicodedata.category(char) != "Mn")


def search(query: str) -> list[str]:
    """
    Search for hymns by number or title with accent-insensitive matching.

    Args:
        query: Search query (hymn number or title text)

    Returns:
        List of formatted hymn results in "Himno {number}: {title}" format
    """
    with sql.connect("static/himnario.db") as con:
        cur = con.cursor()

        # Register the custom function with SQLite
        con.create_function("remove_accents", 1, remove_accents)

        if query.isdigit():
            hymn_number = int(query)
            sql_query = "SELECT number, title FROM hymn WHERE number = ?"
            res = cur.execute(sql_query, (hymn_number,))
            out = res.fetchone()
            if out:
                return [f"Himno {out[0]}: {out[1]}"]
            else:
                return []
        else:
            # Normalize the query for accent-insensitive search
            normalized_query = remove_accents(query)
            sql_query = (
                "SELECT number, title FROM hymn "
                "WHERE remove_accents(title) LIKE ?"  # noqa: E501
            )
            res = cur.execute(sql_query, (f"%{normalized_query}%",))
            out = res.fetchall()
            return [f"Himno {i[0]}: {i[1]}" for i in out]
