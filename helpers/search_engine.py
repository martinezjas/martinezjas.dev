"""Search engine for hymn database with accent-insensitive matching."""

import sqlite3 as sql
import unicodedata


def remove_accents(text):
    """Remove accents from unicode string."""
    if text is None:
        return None
    # Normalize to NFD (decomposed form) and filter out combining characters
    nfd = unicodedata.normalize("NFD", text)
    return "".join(char for char in nfd if unicodedata.category(char) != "Mn")


def search(query):
    """
    Search for hymns by number or title with accent-insensitive matching.

    Args:
        query: Search query (hymn number or title text)

    Returns:
        List of formatted hymn results in "Himno {number}: {title}" format
    """
    con = sql.connect("static/himnario.db")
    cur = con.cursor()

    # Register the custom function with SQLite
    con.create_function("remove_accents", 1, remove_accents)

    out = None
    if query.isdigit():
        query = int(query)
        sql_query = "SELECT number, title FROM hymn WHERE number = ?"
        res = cur.execute(sql_query, (query,))
        out = res.fetchone()
        if out:
            out = [f"Himno {out[0]}: {out[1]}"]
        else:
            out = []
    else:
        # Normalize the query for accent-insensitive search
        normalized_query = remove_accents(query)
        sql_query = (
            "SELECT number, title FROM hymn "
            "WHERE remove_accents(title) LIKE ?"  # noqa: E501
        )
        res = cur.execute(sql_query, (f"%{normalized_query}%",))
        out = res.fetchall()
        out = [f"Himno {i[0]}: {i[1]}" for i in out]
    con.close()
    return out
