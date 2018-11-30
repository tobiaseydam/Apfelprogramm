from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email
from flaskProg.models import Fruit
from wtforms.fields.html5 import DateField


def get_fruits():
	return Fruit.query

class BoxForm(FlaskForm):
	number = StringField('Nummer', validators=[DataRequired()])
	content = QuerySelectField('Inhalt', query_factory=get_fruits, get_label='name')
	ended = DateField('Abzugeben am', format='%Y-%m-%d')
	submit = SubmitField('Speichern')