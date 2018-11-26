from flaskProg import db
from sqlalchemy import func

class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	deposits = db.relationship('Deposit', backref='customer', lazy=True)
	purchases = db.relationship('Purchase', backref='customer', lazy=True)
	
	def __repr__(self):
		return self.name
	
	def amounts(self):
		pa = self.purchaseAmounts()
		da = self.depositAmounts()
		res = []
		fruits = Fruit.query.all()
		for f in fruits:
			res.append([f.name,0,0])
		for d in da:
			for r in res:
				if r[0] == d[0]:
					r[2] += d[2]
		for p in pa:
			for r in res:
				if r[0] == p[0]:
					r[1] -= p[1]
		return res
	
	def depositAmounts(self):
		res = db.session.query(
			Fruit.name,
			func.sum(DepositItem.amount).label('amount'),
			func.sum(DepositItem.amount*Fruit.ratio/100).label('amountLiter')
		).join(DepositItem.deposit
		).join(DepositItem.box
		).join(Box.content
		).filter(Deposit.customer_id==self.id
		).group_by(Fruit.name).all()
		return res
	
	def purchaseAmounts(self):
		res = db.session.query(
			Fruit.name,
			func.sum(PurchaseItem.amount*Article.amountLiter),
		).join(PurchaseItem.purchase
		).join(PurchaseItem.article
		).join(Article.fruit
		).filter(Purchase.customer_id==self.id
		).group_by(Fruit.name).all()
		return res

class Fruit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	ratio = db.Column(db.Numeric(5,2), unique=False, nullable=False)
	price = db.Column(db.Numeric(5,2), unique=False, nullable=False)
	boxes = db.relationship('Box', backref='content', lazy=True)
	articles = db.relationship('Article', backref='fruit', lazy=True)
	
	def __repr__(self):
		return self.name

class Box(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.String(5), nullable=False)
	content_id = db.Column(db.Integer, db.ForeignKey('fruit.id'), nullable=False)
	ended = db.Column(db.DateTime, nullable=False)
	depositItems = db.relationship('DepositItem', backref='box', lazy=True)
	
	def __repr__(self):
		return self.number + " - " + self.content.name + " - Noch " + str(self.freeAmount()) + " kg frei"
	
	def amount(self):
		return sum(depositItem.amount for depositItem in self.depositItems)
	
	def freeAmount(self):
		return 300 - self.amount()

class Deposit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False)
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
	depositItems = db.relationship('DepositItem', backref='deposit', lazy=True)
	
	def __repr__(self):
		return self.id
	
	def amounts(self):
		return db.session.query(
			Fruit.name,
			func.sum(DepositItem.amount).label('amount'),
			func.sum(DepositItem.amount*Fruit.ratio/100).label('amountLiter')
		).join(DepositItem.deposit
		).join(DepositItem.box
		).join(Box.content
		).filter(Deposit.id==self.id
		).group_by(Fruit.name).all()

class DepositItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	box_id = db.Column(db.Integer, db.ForeignKey('box.id'), nullable=False)
	amount = db.Column(db.Numeric(5,1), nullable=False)
	price = db.Column(db.Numeric(5,2), unique=False, nullable=False)
	deposit_id = db.Column(db.Integer, db.ForeignKey('deposit.id'), nullable=False)
	
	def __repr__(self):
		return self.id
	
	def amountLiter(self):
		return self.amount * self.box.content.ratio / 100
	
	def amountEuro(self):
		return self.amount * self.box.content.price / 100
	
	def __init__(self, box, amount, deposit):
		self.box_id = box.id
		self.price = box.content.price
		self.amount = amount
		self.deposit_id = deposit.id

class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True, nullable=False)
	desc = db.Column(db.String(100), unique=False, nullable=False)
	fruit_id = db.Column(db.Integer, db.ForeignKey('fruit.id'), nullable=False)
	price = db.Column(db.Numeric(5,2), unique=False, nullable=False)
	amountLiter = db.Column(db.Numeric(5,2), unique=False, nullable=False)
	purchaseItems = db.relationship('PurchaseItem', backref='article', lazy=True)
	
	def __repr__(self):
		return self.name

class Purchase(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False)
	customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
	purchaseItems = db.relationship('PurchaseItem', backref='purchase', lazy=True)
	
	def total(self):
		return db.session.query(
			func.sum(PurchaseItem.amount*PurchaseItem.price)
		).join(PurchaseItem.purchase
		).filter(Purchase.id==self.id).first()
	
	def amounts(self):
		return db.session.query(
			Fruit.name,
			func.sum(PurchaseItem.amount*Article.amountLiter)
		).join(PurchaseItem.purchase
		).join(PurchaseItem.article
		).join(Article.fruit
		).filter(Purchase.id==self.id
		).group_by(Fruit.name).all()

class PurchaseItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
	amount = db.Column(db.Numeric(5,1), nullable=False)
	price = db.Column(db.Numeric(5,2), unique=False, nullable=True, default=0)
	purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
	
	def amountLiter(self):
		return self.amount * self.article.amountLiter
	
	def total(self):
		return self.amount * self.price

