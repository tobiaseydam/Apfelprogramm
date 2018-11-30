from flask import Blueprint, render_template, url_for, redirect, flash, request
from flaskProg.models import Box
from flaskProg.boxes.forms import BoxForm
from flaskProg import db

boxes = Blueprint('boxes', __name__)

@boxes.route("/boxes")
def viewBoxes():
	boxes = Box.query.all()
	return render_template('viewBoxes.html', boxes=boxes)
	
@boxes.route("/addBox", methods=['GET','POST'])
def addBox():
	form = BoxForm()
	if form.validate_on_submit():
		box = Box(number=form.number.data, content=form.content.data, ended=form.ended.data)
		db.session.add(box)
		db.session.commit()
		flash('Neue Kiste angelegt: %s' % form.number.data, 'success')
		return redirect(url_for("boxes.viewBoxes"))
	return render_template('addBox.html', form=form)
	
@boxes.route("/editBox/<int:box_id>", methods=['GET','POST'])
def editBox(box_id):
	box = Box.query.get_or_404(box_id)
	form = BoxForm()
	if form.validate_on_submit():
		box.number = form.number.data
		box.content = form.content.data
		box.ended = form.ended.data
		db.session.commit()
		flash('Kiste bearbeitet: %s' % box.number, 'success')
		return redirect(url_for("boxes.viewBoxes"))
	elif request.method == 'GET':
		form.number.data = box.number
		form.content.data = box.content
		form.ended.data = box.ended
	return render_template('editBox.html', form=form)
	
@boxes.route("/deleteBox/<int:box_id>", methods=['GET','POST'])
def deleteBox(box_id):
	box = Box.query.get_or_404(box_id)
	db.session.delete(box)
	db.session.commit()
	flash('Kiste geloescht: %s' % box.number, 'success')
	return redirect(url_for("boxes.viewBoxes"))