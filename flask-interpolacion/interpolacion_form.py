from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField
from wtforms.validators import DataRequired


class interpolacionForm(FlaskForm):
    numDatos = IntegerField('numDatos', validators=[DataRequired()])
    submit = SubmitField('calcular')