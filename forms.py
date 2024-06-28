from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SubmitField)
from wtforms.validators import InputRequired, NumberRange


class hymn_form(FlaskForm):
    number = IntegerField('Número', validators=[
                          InputRequired(), NumberRange(min=1, max=613)])
    option = RadioField("Opción", default="cantado",
                        choices=[('cantado', 'Cantado'), ('instrumental', 'Instrumental'), ('letra', 'Letra')])
    submit = SubmitField('Buscar')