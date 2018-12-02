from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FieldList, FormField, DecimalField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email
from flaskProg.models import Customer, Article
from flaskProg.customers.forms import CustomerDepositForm
from wtforms.fields.html5 import DateField
from datetime import datetime

def get_customers():
	return Customer.query

def get_articles():
	return Article.query

def get_num_articles():
	return 5

class PurchaseItemForm(FlaskForm):
	articleName = StringField('Artikelname', default=0)
	article = HiddenField('Artikel', default=0)
	amount = DecimalField('Menge', default=0, places=0)
	ratio = HiddenField('Tauschverhaeltnis', default=0)
	price = HiddenField('Preis', default=0)
	fruit = HiddenField('Frucht', default=0)
	total = StringField('Summe', default=0)

class PurchaseCompensationForm(FlaskForm):
	fruitName = StringField('Frucht', default=0)
	fruit = HiddenField('Frucht', default=0)
	amount = DecimalField('Menge', default=0, places=0)
	price = DecimalField('Preis', default=0)
	total = DecimalField('Summe', default=0)

class PurchaseForm(FlaskForm):
	date = DateField('Datum', default=datetime.today)
	customer = QuerySelectField('Kunde', query_factory=get_customers, get_label='name')
	customerName = ""
	purchaseItems = FieldList(FormField(PurchaseItemForm))
	purchaseCompensations = FieldList(FormField(PurchaseCompensationForm))
	customerDeposits = FieldList(FormField(CustomerDepositForm))
	submit = SubmitField('Speichern')


