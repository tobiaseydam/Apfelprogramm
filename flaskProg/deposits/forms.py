from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FieldList, FormField, DecimalField, HiddenField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email
from flaskProg.models import Customer, Box, Fruit
from wtforms.fields.html5 import DateField
from datetime import datetime


def get_customers():
	return Customer.query

def get_boxes():
	return Box.query
	
def get_fruits():
	return Fruit.query

class FruitListItemForm(FlaskForm):
	id = HiddenField("ID")
	name = HiddenField("Name")
	price = HiddenField("Preis")
	ratio = HiddenField("Tauschverhaeltnis")
	amount = StringField("Gesamt (kg)")
	total = StringField("Gesamt (Liter/Euro)")

class FruitListForm(FlaskForm):
	items = FieldList(FormField(FruitListItemForm))
	
	def __init__(self):
		super(FruitListForm,self).__init__()
		for f in Fruit.query.all():
			item = FruitListItemForm()
			item.id = f.id
			item.name = f.name
			item.price = f.price
			item.ratio = f.ratio
			item.amount = 0
			item.total = 0
			self.items.append_entry(item)		
		item = FruitListItemForm()
		item.id = -1
		item.name = "Euro"
		item.price = "1"
		item.ratio = "1"
		item.amount = "-"
		item.total = 0
		self.items.append_entry(item)
	
class DepositItemForm(FlaskForm):
	boxNumber = StringField('Kiste')
	box = HiddenField('Kiste')
	boxContent = HiddenField('Inhalt')
	amount = DecimalField('Menge', places=2, default=0)
	payOut = BooleanField('Auszahlen', default=False)
	ratio = HiddenField('Tauschverhaeltnis', default=0)
	price = HiddenField('Preis', default=0)
	amountLiter = StringField('Liter', default=0)
	amountEuro = StringField('Euro', default=0)

class EmptyDepositItemForm(FlaskForm):
	boxNumber = StringField('Kiste')
	box = HiddenField('Kiste')
	boxContent = QuerySelectField('Inhalt', query_factory=get_fruits, get_label='name')
	amount = DecimalField('Menge', places=2, default=0)
	payOut = BooleanField('Auszahlen', default=False)
	ratio = HiddenField('Tauschverhaeltnis', default=0)
	price = HiddenField('Preis', default=0)
	amountLiter = StringField('Liter', default=0)
	amountEuro = StringField('Euro', default="0.00")

class DepositForm(FlaskForm):
	date = DateField('Datum', default=datetime.today)
	customer = QuerySelectField('Kunde', query_factory=get_customers, get_label='name')
	customerName = ""
	depositItems = FieldList(FormField(DepositItemForm))
	emptyDepositItems = FieldList(FormField(EmptyDepositItemForm), min_entries=2)
	submit = SubmitField('Speichern')

