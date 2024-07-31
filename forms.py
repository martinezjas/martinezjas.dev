from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SubmitField)
from wtforms.validators import InputRequired, NumberRange, ValidationError


class hymn_form(FlaskForm):
    number = IntegerField('Número', validators=[
                          InputRequired(), NumberRange(min=1, max=613)])
    option = RadioField("Opción", default="cantado",
                        choices=[('cantado', 'Cantado'), ('instrumental', 'Instrumental'), ('letra', 'Letra')])
    submit = SubmitField('Buscar')


def validate_hymn_search(form, field):
    if field.data.isdigit():
        value = int(field.data)
        if not (1 <= value <= 613):
            raise ValidationError('Integer must be between 1 and 613')

class hymn_search(FlaskForm):
    search = StringField('Buscar', validators=[InputRequired(), validate_hymn_search])
    submit = SubmitField('Buscar')