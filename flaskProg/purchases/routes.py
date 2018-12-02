from flask import Blueprint, render_template, url_for, redirect, flash, request
from flaskProg.models import Purchase, PurchaseItem, PurchaseCompensation, Fruit, Article, Customer
from flaskProg.purchases.forms import PurchaseForm, PurchaseItemForm, PurchaseCompensationForm
from flaskProg.deposits.forms import FruitListForm
from flaskProg.customers.forms import CustomerDepositForm
from flaskProg import db

purchases = Blueprint('purchases', __name__)

@purchases.route("/purchases")
def viewPurchases():
	purchases = Purchase.query.all()
	fruits = Fruit.query.all()
	return render_template('viewPurchases.html', purchases=purchases, fruits=fruits)

@purchases.route("/addPurchase", methods=['GET','POST'])
@purchases.route("/addPurchase/<int:customer_id>", methods=['GET','POST'])
def addPurchase(customer_id=-1):
	form = PurchaseForm()
	form.validate_on_submit()
	print(form.errors)
	if form.validate_on_submit():
		purchase = Purchase(date=form.date.data, customer=form.customer.data)
		db.session.add(purchase)
		for entry in form.purchaseItems.entries:
			if entry.amount.data > 0: 
				article = Article.query.get_or_404(entry.article.data)
				purchaseItem = PurchaseItem(article=article, amount=entry.amount.data, purchase=purchase, price=article.price)
				db.session.add(purchaseItem)
		for entry in form.purchaseCompensations.entries:
			if entry.amount.data > 0: 
				fruit = Fruit.query.get_or_404(entry.fruit.data)
				purchaseCompensation = PurchaseCompensation(fruit_id=entry.fruit.data, amount=entry.amount.data, purchase=purchase, price=fruit.pricePerLiter)
				db.session.add(purchaseCompensation)
		db.session.commit()
		flash('Neuer Verkauf angelegt','success')
		return redirect(url_for("purchases.viewPurchases"))
	articles = Article.query.all()
	for a in articles:
		item = PurchaseItemForm()
		item.articleName = a.name
		item.article = a.id
		item.amount = 0
		item.price = a.price
		item.fruit = a.fruit.name
		item.ratio = a.amountLiter
		item.total = 0
		form.purchaseItems.append_entry(item)
	fruits = Fruit.query.all()
	for f in fruits:
		item = PurchaseCompensationForm()
		item.fruitName = f.name
		item.fruit = f.id
		item.amount = 0
		item.price = f.pricePerLiter
		item.total = 0
		form.purchaseCompensations.append_entry(item)
	customer = None
	if customer_id!=-1:
		customer = Customer.query.get_or_404(customer_id)
		deposits = customer.amounts()
		for d in deposits:
			item = CustomerDepositForm()
			item.fruitName = d[0]
			item.fruit = d[3]
			item.amount = d[2]
			form.customerDeposits.append_entry(item)
		form.customer.data = customer
		form.customerName = customer.name
	return render_template('addPurchase.html', form=form, fruits=FruitListForm(), customer=customer, emptyCustomer=(customer_id==-1))

@purchases.route("/viewPurchase/<int:purchase_id>", methods=['GET','POST'])
def viewPurchase(purchase_id):
	purchase = Purchase.query.get_or_404(purchase_id)
	return render_template('viewPurchase.html', purchase=purchase)

@purchases.route("/deletePurchase/<int:purchase_id>", methods=['GET','POST'])
def deletePurchase(purchase_id):
	purchase = Purchase.query.get_or_404(purchase_id)
	for purchaseItem in purchase.purchaseItems:
		db.session.delete(purchaseItem)
	db.session.delete(purchase)
	db.session.commit()
	flash('Verkauf geloescht', 'success')
	return redirect(url_for("purchases.viewPurchases"))