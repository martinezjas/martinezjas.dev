from helpers.determine_themes import determine_themes
import json


def get_audio_url(hymn_option, hymn_number):
    """
    Given a hymn option and number, returns the corresponding audio URL.
    """
    urls = {
        "instrumental": f"https://archive.org/download/HimnarioPistas/{str(hymn_number).zfill(3)}.mp3",
        "cantado": f"https://archive.org/download/HimnarioAdventista/{str(hymn_number).zfill(3)}.mp3",
    }
    return urls[hymn_option]


def get_lyrics(json_data, verse_data):
    """
    Given the JSON data and verse data, returns a list of lyrics with their corresponding metadata.
    """
    lyrics = []
    for entry in json_data["sequence"]:
        data = {
            "contents": None,
            "ID": entry["id"],
            "verseNumber": None,
            "timestamp": entry["timestamp"],
        }
        if data["timestamp"] is not None:
            for verse in verse_data:
                if verse["ID"] == entry["verseId"]:
                    data["contents"] = verse["contents"]
                    data["verseNumber"] = verse["verseNumber"]
                    lyrics.append(data)
                    break
    return lyrics


def get_verse_data(json_data):
    """
    Given the JSON data, returns a list of verse data with their corresponding metadata.
    """
    verse_data = []
    for verse in json_data["verses"]:
        verse_contents = " ".join([content["content"] for content in verse["contents"]])
        data = {
            "contents": verse_contents,
            "ID": verse["id"],
            "verseNumber": verse["number"],
        }
        verse_data.append(data)
    return verse_data


def pull_data(hymn_option, json_data, hymn_number):
    """
    Given a hymn option, JSON data, and hymn number, returns a tuple of audio URL, title, number, lyrics, background URL, icon, super theme, and sub themes.
    """
    audio_url = get_audio_url(hymn_option, hymn_number)
    title, number = json_data["title"], json_data["number"]
    icon, bg_url, super_theme, sub_themes = determine_themes(hymn_number)
    verse_data = get_verse_data(json_data)
    lyrics = get_lyrics(json_data, verse_data)
    return audio_url, title, number, lyrics, bg_url, icon, super_theme, sub_themes
