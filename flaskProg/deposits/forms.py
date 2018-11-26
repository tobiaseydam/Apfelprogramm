from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FieldList, FormField, DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email
from flaskProg.models import Customer, Box
from wtforms.fields.html5 import DateField


def get_customers():
	return Customer.query

def get_boxes():
	return Box.query

class DepositItemForm(FlaskForm):
	box = QuerySelectField('Kiste', query_factory=get_boxes)
	amount = DecimalField('Menge', places=2, default=0)

class DepositForm(FlaskForm):
	date = DateField('Datum')
	customer = QuerySelectField('Kunde', query_factory=get_customers, get_label='name')
	items = FieldList(FormField(DepositItemForm), min_entries=5)
	submit = SubmitField('Speichern')

