from flaskProg import db
from flaskProg.models import Customer, Fruit, Box, DepositItem, Deposit

db.drop_all()
db.create_all()

c1 = Customer(name="Tobias Eydam", email="tobiaseydam@web.de")
c2 = Customer(name="Max Mustermann", email="MaxMustermann@web.de")
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

di1 = DepositItem(box=b1, amount=10, deposit=d1)
di2 = DepositItem(box=b2, amount=20, deposit=d1)
db.session.add(di1)
db.session.add(di2)
db.session.commit()