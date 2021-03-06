from flask import Blueprint, render_template, url_for, redirect, flash, request
from flaskProg.models import Customer, Fruit
from flaskProg.customers.forms import CustomerForm
from flaskProg import db

customers = Blueprint('customers', __name__)

@customers.route("/customers")
def viewCustomers():
	customers = Customer.query.all()
	fruits = Fruit.query.all()
	return render_template('viewCustomers.html', customers=customers, fruits=fruits)
	
@customers.route("/addCustomer", methods=['GET','POST'])
def addCustomer():
	form = CustomerForm()
	if form.validate_on_submit():
		customer = Customer(name=form.name.data, street=form.street.data, zipcode=form.zipcode.data, city=form.city.data, email=form.email.data, phone=form.phone.data, mobile=form.mobile.data)
		db.session.add(customer)
		db.session.commit()
		flash('Neuer Kunde angelegt: %s' % form.name.data, 'success')
		return redirect(url_for("customers.viewCustomers"))
	return render_template('addCustomer.html', form=form)
	
@customers.route("/editCustomer/<int:customer_id>", methods=['GET','POST'])
def editCustomer(customer_id):
	customer = Customer.query.get_or_404(customer_id)
	form = CustomerForm()
	form.validate_on_submit()
	if form.validate_on_submit():
		customer.name = form.name.data
		customer.street = form.street.data
		customer.zipcode = form.zipcode.data
		customer.city = form.city.data
		customer.email = form.email.data
		customer.phone = form.phone.data
		customer.mobile = form.mobile.data
		db.session.commit()
		flash('Kunde bearbeitet: %s' % customer.name, 'success')
		return redirect(url_for("customers.viewCustomers"))
	elif request.method == 'GET':
		form.name.data = customer.name
		form.street.data = customer.street
		form.zipcode.data = customer.zipcode
		form.city.data = customer.city
		form.email.data = customer.email
		form.phone.data = customer.phone
		form.mobile.data = customer.mobile
	return render_template('editCustomer.html', form=form)
	

@customers.route("/viewCustomer/<int:customer_id>", methods=['GET','POST'])
def viewCustomer(customer_id):
	customer = Customer.query.get_or_404(customer_id)
	fruits = Fruit.query.all()
	return render_template('viewCustomer.html', customer=customer, fruits=fruits)	

@customers.route("/deleteCustomer/<int:customer_id>", methods=['GET','POST'])
def deleteCustomer(customer_id):
	customer = Customer.query.get_or_404(customer_id)
	db.session.delete(customer)
	db.session.commit()
	flash('Kunde geloescht: %s' % customer.name, 'success')
	return redirect(url_for("customers.viewCustomers"))