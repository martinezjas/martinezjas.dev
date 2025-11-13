from typing import Any

from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError

# Constants
MIN_HYMN_NUMBER = 1
MAX_HYMN_NUMBER = 613


def validate_hymn_number(form: Any, field: Any) -> None:
    """Validate hymn number field.

    Accepts either a number or a search string for hymn titles.
    """
    if field.data:
        # Try to convert to int
        try:
            value = int(field.data)
            if not (MIN_HYMN_NUMBER <= value <= MAX_HYMN_NUMBER):
                raise ValidationError(
                    f"Hymn number must be {MIN_HYMN_NUMBER}-{MAX_HYMN_NUMBER}"
                )
        except (ValueError, TypeError):
            # If not a number, validate it's a valid title search
            from helpers.search_engine import search as findr

            results = findr(str(field.data))
            if not results:
                raise ValidationError("No hymn found matching your search")


class hymn_form(FlaskForm):
    number = StringField(
        "Número / Título", validators=[InputRequired(), validate_hymn_number]
    )
    option = RadioField(
        "Opción",
        default="cantado",
        choices=[
            ("cantado", "Cantado"),
            ("instrumental", "Instrumental"),
            ("letra", "Letra"),
        ],
    )
    submit = SubmitField("Buscar")
