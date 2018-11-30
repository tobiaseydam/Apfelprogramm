from flaskProg import db
from sqlalchemy import func

class Customer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True, nullable=False)
	street = db.Column(db.String(50), unique=False, nullable=True)
	zipcode = db.Column(db.String(10), unique=False, nullable=True)
	city = db.Column(db.String(50), unique=False, nullable=True)
	email = db.Column(db.String(120), unique=False, nullable=True)
	phone = db.Column(db.String(20), unique=False, nullable=True)
	mobile = db.Column(db.String(20), unique=False, nullable=True)
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
					r[2] -= p[1]
		return res
	
	def depositAmounts(self):
		res = db.session.query(
			Fruit.name,
			func.sum(DepositItem.amount).label('amount'),
			func.sum(DepositItem.amountLiter).label('amountLiter')
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
		
	def history(self):
		list = []
		p = len(self.purchases)-1
		d = len(self.deposits)-1
		while(p+d>-2):
			if(p<0):
				list.append(self.deposits[d])
				d-=1
			elif(d<0):
				list.append(self.purchases[p])
				p-=1
			elif(self.purchases[p].date>self.deposits[d].date):
				list.append(self.purchases[p])
				p-=1
			else:
				list.append(self.deposits[d])
				d-=1
		return list
			

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
	ended = db.Column(db.DateTime, nullable=True)
	depositItems = db.relationship('DepositItem', backref='box', lazy=True)
	
	def __repr__(self):
		return self.number + " - Noch " + str(self.freeAmount()) + " kg frei"
	
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
		return "Gutschrift: " + str(self.id) + " - " + self.date.strftime('%d.%m.%Y') + " - " + self.customer.name
	
	def amounts(self):
		return db.session.query(
			Fruit.name,
			func.sum(DepositItem.amount).label('amount'),
			func.sum(DepositItem.amountLiter).label('amountLiter'),
			func.sum(DepositItem.amountEuro).label('amountEuro')
		).join(DepositItem.deposit
		).join(DepositItem.box
		).join(Box.content
		).filter(Deposit.id==self.id
		).group_by(Fruit.name).all()
	
	def total(self):
		return db.session.query(
			func.sum(DepositItem.amountEuro).label('amountEuro')
		).join(DepositItem.deposit
		).filter(Deposit.id==self.id
		).first()[0]
		
	def type(self):
		return "Gutschrift"

class DepositItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	box_id = db.Column(db.Integer, db.ForeignKey('box.id'), nullable=False)
	amount = db.Column(db.Numeric(5,1), nullable=False)
	price = db.Column(db.Numeric(5,2), unique=False, nullable=False)
	deposit_id = db.Column(db.Integer, db.ForeignKey('deposit.id'), nullable=False)
	amountLiter = db.Column(db.Numeric(5,1), nullable=False)
	amountEuro = db.Column(db.Numeric(5,2), nullable=False)
	
	def __repr__(self):
		return self.id
	
	def __init__(self, box, amount, deposit, amountLiter, amountEuro):
		self.box_id = box.id
		self.price = box.content.price
		self.amount = amount
		self.deposit_id = deposit.id
		self.amountLiter = amountLiter
		self.amountEuro = amountEuro

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
	
	def __repr__(self):
		return "Verkauf: " + str(self.id) + " - " + self.date.strftime('%d.%m.%Y') + " - " + self.customer.name
	
	def total(self):
		return db.session.query(
			func.sum(PurchaseItem.amount*PurchaseItem.price)
		).join(PurchaseItem.purchase
		).filter(Purchase.id==self.id).first()[0]
	
	def amounts(self):
		return db.session.query(
			Fruit.name,
			func.sum(PurchaseItem.amount*Article.amountLiter)
		).join(PurchaseItem.purchase
		).join(PurchaseItem.article
		).join(Article.fruit
		).filter(Purchase.id==self.id
		).group_by(Fruit.name).all()
		
	def type(self):
		return "Verkauf"
		

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

