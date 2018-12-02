from flask import Blueprint, render_template, url_for, redirect, flash, request
from flaskProg.models import Fruit
from flaskProg.fruits.forms import FruitForm
from flaskProg import db

fruits = Blueprint('fruits', __name__)

@fruits.route("/fruits")
def viewFruits():
	fruits = Fruit.query.all()
	return render_template('viewFruits.html', fruits=fruits)
	
@fruits.route("/addFruit", methods=['GET','POST'])
def addFruit():
	form = FruitForm()
	if form.validate_on_submit():
		fruit = Fruit(name=form.name.data, ratio=form.ratio.data, price=form.price.data, pricePerLiter=form.pricePerLiter.data)
		db.session.add(fruit)
		db.session.commit()
		flash('Neue Frucht angelegt: %s' % form.name.data, 'success')
		return redirect(url_for("fruits.viewFruits"))
	return render_template('addFruit.html', form=form)
	
@fruits.route("/editFruit/<int:fruit_id>", methods=['GET','POST'])
def editFruit(fruit_id):
	fruit = Fruit.query.get_or_404(fruit_id)
	form = FruitForm()
	if form.validate_on_submit():
		fruit.name = form.name.data
		fruit.ratio = form.ratio.data
		fruit.price = form.price.data
		fruit.pricePerLiter = form.pricePerLiter.data
		db.session.commit()
		flash('Frucht bearbeitet: %s' % fruit.name, 'success')
		return redirect(url_for("fruits.viewFruits"))
	elif request.method == 'GET':
		form.name.data = fruit.name
		form.ratio.data = fruit.ratio
		form.price.data = fruit.price
		form.pricePerLiter.data = fruit.pricePerLiter
	return render_template('editFruit.html', form=form)
	
@fruits.route("/deleteFruit/<int:fruit_id>", methods=['GET','POST'])
def deleteFruit(fruit_id):
	fruit = Fruit.query.get_or_404(fruit_id)
	db.session.delete(fruit)
	db.session.commit()
	flash('Frucht geloescht: %s' % fruit.name, 'success')
	return redirect(url_for("fruits.viewFruits"))