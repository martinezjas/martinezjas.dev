from helpers.determine_themes import determine_themes


def get_audio_url(hymn_option: str, hymn_number: int) -> str:
    """
    Given a hymn option and number, returns the corresponding audio URL.
    """
    urls = {
        "instrumental": (
            f"https://archive.org/download/HimnarioPistas/"
            f"{str(hymn_number).zfill(3)}.mp3"
        ),
        "cantado": (
            f"https://archive.org/download/HimnarioAdventista/"
            f"{str(hymn_number).zfill(3)}.mp3"
        ),
        "letra": "",
    }
    return urls[hymn_option]


def get_lyrics_data(json_data: dict) -> list[dict]:
    """
    Given the JSON data, returns a list of verse data with metadata.
    """
    lyrics = []
    for entry in json_data["sequence"]:
        data = {
            "verseNumber": None,
            "verseID": entry["verseId"],
            "lineID": entry["verseContentId"],
            "line": None,
            "timeStamp": entry["timestamp"],
        }
        for verse in json_data["verses"]:
            for line in verse["contents"]:
                if line["id"] == data["lineID"]:
                    data["verseNumber"] = verse["number"]
                    data["line"] = line["content"]
                    if all(value is not None for value in data.values()):
                        lyrics.append(data)
                    break
    return lyrics


def pull_data(
    hymn_option: str, json_data: dict, hymn_number: int
) -> tuple[str, str, int, list[dict], str, str, str, str]:
    """
    Return hymn data tuple: audio URL, title, number, lyrics, bg URL,
    icon, super theme, and sub themes.
    """
    audio_url = get_audio_url(hymn_option, hymn_number)
    title, number = json_data["title"], json_data["number"]
    icon, bg_url, super_theme, sub_themes = determine_themes(hymn_number)
    lyrics = get_lyrics_data(json_data)
    return (
        audio_url,
        title,
        number,
        lyrics,
        bg_url,
        icon,
        super_theme,
        sub_themes,
    )  # noqa: E501
