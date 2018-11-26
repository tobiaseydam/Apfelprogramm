from flask import Blueprint, render_template, url_for, redirect, flash, request
from flaskProg.models import Deposit, DepositItem, Fruit, Box
from flaskProg.deposits.forms import DepositItemForm, DepositForm
from flaskProg import db

deposits = Blueprint('deposits', __name__)

@deposits.route("/deposits")
def viewDeposits():
	deposits = Deposit.query.all()
	fruits = Fruit.query.all()
	return render_template('viewDeposits.html', deposits=deposits, fruits=fruits)

@deposits.route("/addDeposit", methods=['GET','POST'])
def addDeposit():
	form = DepositForm()
	form.validate_on_submit()
	if form.validate_on_submit():
		deposit = Deposit(date=form.date.data, customer=form.customer.data)
		db.session.add(deposit)
		for entry in form.depositItems.entries:
			if entry.amount.data > 0:
				box = Box.query.get_or_404(entry.box.data)
				depositItem = DepositItem(box=box, amount=entry.amount.data, deposit=deposit)
				db.session.add(depositItem)
		db.session.commit()
		flash('Neue Gutschrift angelegt','success')
		return redirect(url_for("deposits.viewDeposits"))
	boxes = Box.query.all()
	for b in boxes:
		item = DepositItemForm()
		item.boxNumber = b
		item.box = b.id
		item.amount = 0
		form.depositItems.append_entry(item)
	return render_template('addDeposit.html', form=form)

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