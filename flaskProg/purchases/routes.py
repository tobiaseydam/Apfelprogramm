from flask import Blueprint, render_template, url_for, redirect, flash, request
from flaskProg.models import Purchase, PurchaseItem, Fruit, Article
from flaskProg.purchases.forms import PurchaseForm, PurchaseItemForm
from flaskProg import db

purchases = Blueprint('purchases', __name__)

@purchases.route("/purchases")
def viewPurchases():
	purchases = Purchase.query.all()
	fruits = Fruit.query.all()
	return render_template('viewPurchases.html', purchases=purchases, fruits=fruits)

@purchases.route("/addPurchase", methods=['GET','POST'])
def addPurchase():
	form = PurchaseForm()
	form.validate_on_submit()
	if form.validate_on_submit():
		purchase = Purchase(date=form.date.data, customer=form.customer.data)
		db.session.add(purchase)
		for entry in form.purchaseItems.entries:
			if entry.amount.data > 0:
				article = Article.query.get_or_404(entry.article.data)
				purchaseItem = PurchaseItem(article=article, amount=entry.amount.data, purchase=purchase, price=article.price)
				db.session.add(purchaseItem)
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
		form.purchaseItems.append_entry(item)
	return render_template('addPurchase.html', form=form)

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