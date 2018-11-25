from flask import Blueprint, render_template, url_for, redirect, flash, request
from flaskProg.customers.models import Customer
from flaskProg.customers.forms import CustomerForm
from flaskProg import db

customers = Blueprint('customers', __name__)

@customers.route("/customers")
def viewCustomers():
	customers = Customer.query.all()
	return render_template('viewCustomers.html', customers=customers)
	
@customers.route("/addCustomer", methods=['GET','POST'])
def addCustomer():
	form = CustomerForm()
	if form.validate_on_submit():
		customer = Customer(name=form.name.data, email=form.email.data)
		db.session.add(customer)
		db.session.commit()
		flash('Neuer Kunde angelegt: %s' % form.name.data, 'success')
		return redirect(url_for("customers.viewCustomers"))
	return render_template('addCustomer.html', form=form)
	
@customers.route("/editCustomer/<int:customer_id>", methods=['GET','POST'])
def editCustomer(customer_id):
	customer = Customer.query.get_or_404(customer_id)
	form = CustomerForm()
	if form.validate_on_submit():
		customer.name = form.name.data
		customer.email = form.email.data
		db.session.commit()
		flash('Kunde bearbeitet: %s' % customer.name, 'success')
		return redirect(url_for("customers.viewCustomers"))
	elif request.method == 'GET':
		form.name.data = customer.name
		form.email.data = customer.email
	return render_template('editCustomer.html', form=form)
	
@customers.route("/deleteCustomer/<int:customer_id>", methods=['GET','POST'])
def deleteCustomer(customer_id):
	customer = Customer.query.get_or_404(customer_id)
	db.session.delete(customer)
	db.session.commit()
	flash('Kunde geloescht: %s' % customer.name, 'success')
	return redirect(url_for("customers.viewCustomers"))