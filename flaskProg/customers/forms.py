from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length, Email

class CustomerDepositForm(FlaskForm):
	fruitName = StringField('Frucht')
	fruit = HiddenField('Frucht')
	amount = DecimalField('Menge', places=2, default=0)

class CustomerForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=5, max=50)])
	street = StringField('Strasse', validators=[Length(max=50)])
	zipcode = StringField('PLZ', validators=[Length(max=50)])
	city = StringField('Ort', validators=[Length(max=50)])
	email = StringField('e-Mail', validators=[Length(max=120), Email()])
	phone = StringField('Telefon', validators=[Length(max=20)])
	mobile = StringField('Mobil', validators=[Length(max=20)])
	submit = SubmitField('Speichern')