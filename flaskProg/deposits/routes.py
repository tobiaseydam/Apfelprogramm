from flask import Blueprint, render_template, url_for, redirect, flash, request
from flaskProg.models import Deposit, DepositItem, Fruit, Box, Customer
from flaskProg.deposits.forms import EmptyDepositItemForm, DepositItemForm, DepositForm, FruitListForm
from flaskProg import db
from datetime import datetime

deposits = Blueprint('deposits', __name__)

@deposits.route("/deposits")
def viewDeposits():
	deposits = Deposit.query.all()
	fruits = Fruit.query.all()
	return render_template('viewDeposits.html', deposits=deposits, fruits=fruits)

@deposits.route("/addDeposit", methods=['GET','POST'])
@deposits.route("/addDeposit/<int:customer_id>", methods=['GET','POST'])
def addDeposit(customer_id=-1):
	form = DepositForm()
	form.validate_on_submit()
	if form.validate_on_submit():
		deposit = Deposit(date=form.date.data, customer=form.customer.data)
		db.session.add(deposit)
		for entry in form.depositItems.entries:
			if entry.amount.data > 0:
				box = Box.query.get_or_404(entry.box.data)
				depositItem = DepositItem(box=box, amount=entry.amount.data, deposit=deposit, amountLiter=entry.amountLiter.data, amountEuro=entry.amountEuro.data)
				db.session.add(depositItem)
		for entry in form.emptyDepositItems.entries:
			if entry.amount.data > 0:
				box = Box(number=entry.boxNumber.data, content=entry.boxContent.data)
				db.session.add(box)
				db.session.commit()
				depositItem = DepositItem(box=box, amount=entry.amount.data, deposit=deposit, amountLiter=entry.amountLiter.data, amountEuro=entry.amountEuro.data)
				db.session.add(depositItem)
		db.session.commit()
		flash('Neue Gutschrift angelegt','success')
		return redirect(url_for("deposits.viewDeposits"))
	if len(form.depositItems) == 0:
		boxes = Box.query.all()
		for b in boxes:
			item = DepositItemForm()
			item.boxNumber = b
			item.box = b.id
			item.amount = 0
			item.boxContent = b.content.name
			item.payOut = False
			item.ratio = b.content.ratio
			item.price = b.content.price
			item.amountLiter = 0
			item.amountEuro = "0.00"
			form.depositItems.append_entry(item)
		if(customer_id!=-1):
			customer = Customer.query.get_or_404(customer_id)
			form.customer.data = customer
			form.customerName = customer.name
	return render_template('addDeposit.html', form=form, fruits=FruitListForm(), emptyCustomer=(customer_id==-1))

@deposits.route("/viewDeposit/<int:deposit_id>", methods=['GET','POST'])
def viewDeposit(deposit_id):
	deposit = Deposit.query.get_or_404(deposit_id)
	return render_template('viewDeposit.html', deposit=deposit)

@deposits.route("/deleteDeposit/<int:deposit_id>", methods=['GET','POST'])
def deleteDeposit(deposit_id):
	deposit = Deposit.query.get_or_404(deposit_id)
	for depositItem in deposit.depositItems:
		db.session.delete(depositItem)
	db.session.delete(deposit)
	db.session.commit()
	flash('Gutschrift geloescht', 'success')
	return redirect(url_for("deposits.viewDeposits"))