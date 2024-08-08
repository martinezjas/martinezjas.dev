from flask import Flask, render_template, url_for, redirect, session
from forms import hymn_form, hymn_search
from requests.exceptions import HTTPError
from helpers.pull_info import pull_data
import requests
from helpers.search_engine import search as findr

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
            session["hymn_data"] = {
                "audio_url": audio_url,
                "title": title,
                "number": number,
                "lyrics": lyrics,
                "bg_url": bg_url,
                "icon": icon,
                "super_theme": super_theme,
                "sub_theme": sub_theme,
            }
            return redirect(url_for("himnario_play", hymn_number=hymn_number))
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


@app.route("/himnario/<int:hymn_number>")
def himnario_play(hymn_number):
    hymn_data = session.get("hymn_data")
    if hymn_data:
        copy = hymn_data.copy()
        session.pop("hymn_data")
        return render_template(
            "himnario_play.html",
            audio_url=copy["audio_url"],
            title=copy["title"],
            number=copy["number"],
            lyrics=copy["lyrics"],
            bg_url=copy["bg_url"],
            icon=copy["icon"],
            super_theme=copy["super_theme"],
            sub_theme=copy["sub_theme"],
        )
    else:
        return redirect(url_for("himnario"))


@app.route("/hdoc")
def hdoc():
    return render_template("himnario_doc.html")


@app.route("/search", methods=["POST", "GET"])
def search():
    form = hymn_search()
    if form.validate_on_submit():
        query = form.search.data
        try:
            results = findr(query)
            return render_template("search_results.html", results=results)
        except Exception as err:
            return render_template(
                "error_handle.html", message="An error occurred: " + str(err)
            )
    else:
        return render_template("search.html", form=form)


if __name__ == "__main__":
    app.run()
