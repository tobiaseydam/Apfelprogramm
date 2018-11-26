from flaskProg import db

class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	deposits = db.relationship('Deposit', backref='customer', lazy=True)
	
	def __repr__(self):
		return self.name

class Fruit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	ratio = db.Column(db.Numeric(5,2), unique=False, nullable=False)
	price = db.Column(db.Numeric(5,2), unique=False, nullable=False)
	boxes = db.relationship('Box', backref='content', lazy=True)
	
	def __repr__(self):
		return self.name

class Box(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.String(5), nullable=False)
	content_id = db.Column(db.Integer, db.ForeignKey('fruit.id'), nullable=False)
	ended = db.Column(db.DateTime, nullable=False)
	depositItems = db.relationship('DepositItem', backref='box', lazy=True)
	
	def __repr__(self):
		return self.number + " - " + self.content.name

class Deposit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False)
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
	depositItems = db.relationship('DepositItem', backref='deposit', lazy=True)
	
	def __repr__(self):
		return self.id

class DepositItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	box_id = db.Column(db.Integer, db.ForeignKey('box.id'), nullable=False)
	amount = db.Column(db.Numeric(5,1), nullable=False)
	price = db.Column(db.Numeric(5,2), unique=False, nullable=False)
	deposit_id = db.Column(db.Integer, db.ForeignKey('deposit.id'), nullable=False)
	
	def __repr__(self):
		return self.id
	
	def __init__(self, box, amount, deposit):
		self.box_id = box.id
		self.price = box.content.price
		self.amount = amount
		self.deposit_id = deposit.id



