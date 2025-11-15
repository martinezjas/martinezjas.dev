import logging
import os

from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from requests.exceptions import HTTPError

from forms import hymn_form
from helpers.get_data import get_data
from helpers.pull_info import pull_data
from helpers.search_engine import search as findr

load_dotenv()

# Configuration constants
SESSION_TIMEOUT_SECONDS = 3600  # 1 hour
RATE_LIMIT_HIMNARIO = "30 per minute"
RATE_LIMIT_AUTOCOMPLETE = "60 per minute"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Session security configuration
app.config["SESSION_COOKIE_HTTPONLY"] = (
    True  # Prevent JavaScript access to session cookie
)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # CSRF protection
app.config["SESSION_COOKIE_SECURE"] = (
    os.environ.get("FLASK_ENV") == "production"
)  # HTTPS only in production
app.config["PERMANENT_SESSION_LIFETIME"] = SESSION_TIMEOUT_SECONDS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


# Security headers
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses."""
    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Enable XSS protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    # HSTS - Force HTTPS (only in production)
    if os.environ.get("FLASK_ENV") == "production":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' "
        "https://cdn.tailwindcss.com https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' "
        "https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "img-src 'self' data: https:; "
        "font-src 'self' "
        "https://cdn.jsdelivr.net https://fonts.gstatic.com; "
        "connect-src 'self' https://cdn.jsdelivr.net; "
        "media-src 'self' https://archive.org https://*.archive.org; "
        "frame-ancestors 'self'; "
        "form-action 'self';"
    )
    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    # Permissions Policy
    response.headers["Permissions-Policy"] = (
        "geolocation=(), microphone=(), camera=()"  # noqa: E501
    )
    return response


@app.route("/favicon.ico")
def favicon():
    return url_for("static", filename="images/favicon/favicon.ico")


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/himnario", methods=["POST", "GET"])
@limiter.limit(RATE_LIMIT_HIMNARIO)
def himnario():
    form = hymn_form()
    if form.validate_on_submit():
        hymn_input = form.number.data
        hymn_option = form.option.data

        # Convert text search to hymn number if needed
        if not str(hymn_input).isdigit():
            search_results = findr(str(hymn_input))
            if search_results:
                # Extract number from "Himno 123: Title" format
                first_result = search_results[0]
                if first_result.startswith("Himno "):
                    hymn_str = first_result.split(": ")[0]
                    hymn_number = int(hymn_str.replace("Himno ", ""))
                else:
                    return render_template(
                        "error_handle.html",
                        message="Could not find a matching hymn.",
                    )
            else:
                return render_template(
                    "error_handle.html",
                    message="No hymn found matching your search.",
                )
        else:
            hymn_number = int(hymn_input)

        try:
            local_data = get_data(str(hymn_number))
            if not local_data:
                return render_template(
                    "error_handle.html",
                    message="The hymn number you entered does not exist.",
                )
            (
                audio_url,
                title,
                number,
                lyrics,
                bg_url,
                icon,
                super_theme,
                sub_theme,
            ) = pull_data(hymn_option, local_data, hymn_number)
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
            logger.error(f"HTTP error in himnario route: {http_err}")
            return render_template(
                "error_handle.html",
                message="Unable to load hymn. Please try again later.",
            )
        except Exception as err:
            logger.error(f"Error in himnario route: {err}", exc_info=True)
            return render_template(
                "error_handle.html",
                message=(
                    "An error occurred while processing your request. "
                    "Please try again."
                ),
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


@app.route("/api/search/autocomplete", methods=["GET"])
@limiter.limit(RATE_LIMIT_AUTOCOMPLETE)
def search_autocomplete():
    """API endpoint for live search autocomplete."""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    try:
        results = findr(query)
        # Convert results to structured JSON format
        json_results = []
        for result in results:  # Return all results
            # Parse "Himno 123: Title" format
            if result.startswith("Himno "):
                parts = result.split(": ", 1)
                if len(parts) == 2:
                    number = parts[0].replace("Himno ", "")
                    title = parts[1]
                    json_results.append(
                        {"number": number, "title": title, "display": result}
                    )
        return jsonify(json_results)
    except Exception as err:
        logger.error(f"Error in autocomplete route: {err}", exc_info=True)
        return jsonify({"error": "An error occurred"}), 500


if __name__ == "__main__":
    app.run()
