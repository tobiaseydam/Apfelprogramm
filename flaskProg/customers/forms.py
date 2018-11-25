from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email

class CustomerForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=5, max=20)])
	email = StringField('e-Mail', validators=[DataRequired(), Length(min=5, max=120), Email()])
	submit = SubmitField('Speichern')