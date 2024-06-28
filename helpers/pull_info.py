from helpers.determine_themes import determine_themes
import json


def get_audio_url(hymn_option, hymn_number):
    """
    Given a hymn option and number, returns the corresponding audio URL.
    """
    urls = {
        "instrumental": f"https://archive.org/download/HimnarioPistas/{str(hymn_number).zfill(3)}.mp3",
        "cantado": f"https://archive.org/download/HimnarioAdventista/{str(hymn_number).zfill(3)}.mp3",
        "letra": "",
    }
    return urls[hymn_option]


def get_lyrics_data(json_data):
    """
    Given the JSON data, returns a list of verse data with their corresponding metadata.
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


def pull_data(hymn_option, json_data, hymn_number):
    """
    Given a hymn option, JSON data, and hymn number, returns a tuple of audio URL, title, number, lyrics, background URL, icon, super theme, and sub themes.
    """
    audio_url = get_audio_url(hymn_option, hymn_number)
    title, number = json_data["title"], json_data["number"]
    icon, bg_url, super_theme, sub_themes = determine_themes(hymn_number)
    lyrics = get_lyrics_data(json_data)
    return audio_url, title, number, lyrics, bg_url, icon, super_theme, sub_themes
