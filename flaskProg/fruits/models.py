from flaskProg import db

class Fruit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	ratio = db.Column(db.Numeric(5,2), unique=False, nullable=False)
	price = db.Column(db.Numeric(5,2), unique=False, nullable=False)