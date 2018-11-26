from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FieldList, FormField, DecimalField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email
from flaskProg.models import Customer, Box
from wtforms.fields.html5 import DateField
from datetime import datetime


def get_customers():
	return Customer.query

def get_boxes():
	return Box.query

def get_num_boxes():
	return 5

class DepositItemForm(FlaskForm):
	boxNumber = StringField('Kiste')
	box = HiddenField('Kiste')
	amount = DecimalField('Menge', places=2, default=0)

class DepositForm(FlaskForm):
	date = DateField('Datum', default=datetime.today)
	customer = QuerySelectField('Kunde', query_factory=get_customers, get_label='name')
	depositItems = FieldList(FormField(DepositItemForm))
	submit = SubmitField('Speichern')

