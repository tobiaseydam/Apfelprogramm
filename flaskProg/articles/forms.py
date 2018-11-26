from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email
from flaskProg.models import Fruit
from wtforms.fields.html5 import DateField


def get_fruits():
	return Fruit.query

class ArticleForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	desc = StringField('Beschreibung', validators=[DataRequired()])
	fruit = QuerySelectField('Frucht', query_factory=get_fruits, get_label='name')
	price = DecimalField('Preis', places=2, validators=[DataRequired()])
	amountLiter = DecimalField('Inhalt (Liter)', places=2, validators=[DataRequired()])
	submit = SubmitField('Speichern')