from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, FieldList, FormField, DecimalField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email
from flaskProg.models import Customer, Article
from wtforms.fields.html5 import DateField
from datetime import datetime

def get_customers():
	return Customer.query

def get_articles():
	return Article.query

def get_num_articles():
	return 5#Article.query.count()

class PurchaseItemForm(FlaskForm):
	articleName = StringField('Artikelname', default=0)
	article = HiddenField('Artikel', default=0)
	amount = DecimalField('Menge', default=0, places=0)
	price = StringField('Preis', default=0)

class PurchaseForm(FlaskForm):
	date = DateField('Datum', default=datetime.today)
	customer = QuerySelectField('Kunde', query_factory=get_customers, get_label='name')
	purchaseItems = FieldList(FormField(PurchaseItemForm))
	submit = SubmitField('Speichern')


