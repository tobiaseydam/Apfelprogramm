from flask import Blueprint, render_template, url_for, redirect, flash, request
from flaskProg.models import Deposit, DepositItem
from flaskProg.deposits.forms import DepositForm
from flaskProg import db

deposits = Blueprint('deposits', __name__)

@deposits.route("/deposits")
def viewDeposits():
	deposits = Deposit.query.all()
	return render_template('viewDeposits.html', deposits=deposits)
	
@deposits.route("/addDeposit", methods=['GET','POST'])
def addDeposit():
	form = DepositForm()
	form.validate_on_submit()
	if form.validate_on_submit():
		deposit = Deposit(date=form.date.data, customer=form.customer.data)
		db.session.add(deposit)
		for entry in form.items.entries:
			if entry.amount.data > 0:
				depositItem = DepositItem(box=entry.box.data, amount=entry.amount.data, deposit=deposit)
				db.session.add(depositItem)
		db.session.commit()
		flash('Neue Gutschrift angelegt','success')
		return redirect(url_for("deposits.viewDeposits"))
	return render_template('addDeposit.html', form=form)

@deposits.route("/viewDeposit/<int:deposit_id>", methods=['GET','POST'])
def viewDeposit(deposit_id):
	deposit = Deposit.query.get_or_404(deposit_id)
	return render_template('viewDeposit.html', deposit=deposit)