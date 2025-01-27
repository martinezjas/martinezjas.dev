import json
import requests
from requests.exceptions import HTTPError
from flask import Flask, render_template, url_for

def get_photo_data(photo_id):
    """
    Given a photo ID, returns the corresponding photo data.
    """
    try:
        response = requests.get(
            "https://api.unsplash.com/photos/"
            + photo_id
            + "/?client_id=79eEcwNs0cO3F41gthTFarJYUSCcR_zSyOdzn0hdykI",
            timeout=15,
        )
        response.raise_for_status()
        json_data = response.json()
        photo_url = json_data["urls"]["full"]
        return photo_url
    except HTTPError as http_err:
        return render_template(
            "error_handle.html", message="An HTTP error occurred: " + str(http_err)
        )
    except Exception as err:
        return render_template(
            "error_handle.html", message="An non-HTTP error occurred: " + str(err)
        )
