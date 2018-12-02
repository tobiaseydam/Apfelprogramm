from flaskProg import db
from flaskProg.models import Customer, Fruit, Box, DepositItem, Deposit, Article, Purchase, PurchaseItem

db.drop_all()
db.create_all()

c1 = Customer(name="Tobias Eydam", email="tobiaseydam@web.de", street="", zipcode="", city="", phone="", mobile="")
c2 = Customer(name="Max Mustermann", email="MaxMustermann@web.de", street="", zipcode="", city="", phone="", mobile="")
db.session.add(c1)
db.session.add(c2)
db.session.commit()

f1 = Fruit(name="Apfel", ratio="60", price="5")
f2 = Fruit(name="Quitte", ratio="60", price="8")
db.session.add(f1)
db.session.add(f2)
db.session.commit()

b1 = Box(number=100, content=f1, ended="2018-11-26")
b2 = Box(number=200, content=f2, ended="2018-11-19")
db.session.add(b1)
db.session.add(b2)
db.session.commit()

d1 = Deposit(date="2018-11-25", customer=c1)
db.session.add(d1)
db.session.commit()

di1 = DepositItem(box=b1, amount=100, deposit=d1, amountLiter=60, amountEuro=0)
di2 = DepositItem(box=b2, amount=20, deposit=d1, amountLiter=12, amountEuro=0)
db.session.add(di1)
db.session.add(di2)
db.session.commit()

a1 = Article(name="Apfelsaft klar", desc="klarer Apfelsaft", fruit=f1, amountLiter=1, price=0.55)
a2 = Article(name="Apfelsaft naturtrueb", desc="naturtrueber Apfelsaft", fruit=f1, amountLiter=1, price=0.58)
a3 = Article(name="Quittensaft", desc="klarer Quittensaft", fruit=f2, amountLiter=1, price=0.70)
db.session.add(a1)
db.session.add(a2)
db.session.add(a3)
db.session.commit()

p1 = Purchase(date="2018-11-25", customer=c1)
db.session.add(p1)
db.session.commit()

pi1 = PurchaseItem(article=a1, amount=10, price=a1.price, purchase=p1)
pi2 = PurchaseItem(article=a2, amount=5, price=a2.price, purchase=p1)
db.session.add(pi1)
db.session.add(pi2)
db.session.commit()