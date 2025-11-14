import logging
import os
from functools import lru_cache
from typing import Optional

import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError

load_dotenv()
logger = logging.getLogger(__name__)


@lru_cache(maxsize=128)
def get_photo_data(photo_id: str) -> Optional[str]:
    """
    Get photo URL from Unsplash API with caching.

    Results are cached to prevent redundant API calls for the same photo_id.
    Cache size is limited to 128 most recent unique photo IDs.

    Args:
        photo_id: The Unsplash photo ID

    Returns:
        The full-size photo URL, or None if the request fails
    """
    try:
        response = requests.get(
            "https://api.unsplash.com/photos/"
            + photo_id
            + "/?client_id="
            + os.environ.get("UNSPLASH_ACCESS_KEY"),
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
