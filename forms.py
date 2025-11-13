from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError


def validate_hymn_number(form, field):
    """Validate hymn number field.

    Accepts either a number or a search string for hymn titles.
    """
    if field.data:
        # Try to convert to int
        try:
            value = int(field.data)
            if not (1 <= value <= 613):
                raise ValidationError("Hymn number must be between 1 and 613")
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
