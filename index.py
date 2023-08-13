from flask import Flask, render_template, url_for
from forms import hymn_form
from requests.exceptions import HTTPError
from helpers.pull_info import pull_data
import requests
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "d3f1fdf354bc63bc3c348ddf4abd39fe"


@app.route("/favicon.ico")
def favicon():
    return url_for("static", filename="images/favicon/favicon.ico")


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/himnario", methods=["POST", "GET"])
def himnario():
    form = hymn_form()
    if form.validate_on_submit():
        hymn_number = form.number.data
        hymn_option = form.option.data
        try:
            response = requests.get(
                "https://sdah.my.to/hymn/" + str(hymn_number), timeout=15
            )
            response.raise_for_status()
            json_data = response.json()
            (
                audio_url,
                title,
                number,
                lyrics,
                bg_url,
                icon,
                super_theme,
                sub_theme,
            ) = pull_data(hymn_option, json_data, hymn_number)
            return render_template(
                "himnario_play.html",
                audio_url=audio_url,
                title=title,
                number=number,
                lyrics=lyrics,
                bg_url=bg_url,
                icon=icon,
                super_theme=super_theme,
                sub_theme=sub_theme,
            )
        except HTTPError as http_err:
            return render_template(
                "error_handle.html", message="An HTTP error occurred: " + str(http_err)
            )
        except Exception as err:
            return render_template(
                "error_handle.html", message="An non-HTTP error occurred: " + str(err)
            )
    else:
        return render_template("himnario_search.html", form=form)


@app.route("/hdoc")
def hdoc():
    return render_template("himnario_doc.html")


@app.route("/bible")
def bible():
    return render_template("bible.html")

if __name__ == "__main__":
    app.run(debug=True)