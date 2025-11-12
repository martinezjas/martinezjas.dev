import requests
from requests.exceptions import HTTPError
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

def get_photo_data(photo_id):
    """
    Given a photo ID, returns the corresponding photo data.
    Returns None if the request fails.
    """
    try:
        response = requests.get(
            "https://api.unsplash.com/photos/"
            + photo_id
            + "/?client_id=" + os.environ.get("UNSPLASH_ACCESS_KEY"),
            timeout=15,
        )
        response.raise_for_status()
        json_data = response.json()
        photo_url = json_data["urls"]["full"]
        return photo_url
    except HTTPError as http_err:
        logger.error(f"HTTP error fetching photo {photo_id}: {http_err}")
        return None
    except Exception as err:
        logger.error(f"Error fetching photo {photo_id}: {err}", exc_info=True)
        return None
