from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Email

class FruitForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
	ratio = DecimalField('Tauschverhaeltnis (Liter pro 100kg)', places=2, validators=[DataRequired()])
	price = DecimalField('Preis pro 100kg', places=2, validators=[DataRequired()])
	pricePerLiter = DecimalField('Preis pro Liter im Freiverkauf', places=2, validators=[DataRequired()])
	submit = SubmitField('Speichern')