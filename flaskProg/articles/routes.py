from flask import Blueprint, render_template, url_for, redirect, flash, request
from flaskProg.models import Article
from flaskProg.articles.forms import ArticleForm
from flaskProg import db

articles = Blueprint('articles', __name__)

@articles.route("/articles")
def viewArticles():
	articles = Article.query.all()
	return render_template('viewArticles.html', articles=articles)
	
@articles.route("/addArticle", methods=['GET','POST'])
def addArticle():
	form = ArticleForm()
	if form.validate_on_submit():
		article = Article(name=form.name.data, desc=form.desc.data, fruit=form.fruit.data, price=form.price.data, amountLiter=form.amountLiter.data)
		db.session.add(article)
		db.session.commit()
		flash('Neuer Artikel angelegt: %s' % form.name.data, 'success')
		return redirect(url_for("articles.viewArticles"))
	return render_template('addArticle.html', form=form)
	
@articles.route("/editArticle/<int:article_id>", methods=['GET','POST'])
def editArticle(article_id):
	article = Article.query.get_or_404(article_id)
	form = ArticleForm()
	if form.validate_on_submit():
		article.name = form.name.data
		article.desc = form.desc.data
		article.fruit = form.fruit.data
		article.price = form.price.data
		article.amountLiter = form.amountLiter.data
		db.session.commit()
		flash('Artikel bearbeitet: %s' % article.name, 'success')
		return redirect(url_for("articles.viewArticles"))
	elif request.method == 'GET':
		form.name.data = article.name
		form.desc.data = article.desc
		form.fruit.data = article.fruit
		form.price.data = article.price
		form.amountLiter.data = article.amountLiter
	return render_template('editArticle.html', form=form)
	
@articles.route("/deleteArticle/<int:article_id>", methods=['GET','POST'])
def deleteArticle(article_id):
	article = Article.query.get_or_404(article_id)
	db.session.delete(article)
	db.session.commit()
	flash('Artikel geloescht: %s' % article.name, 'success')
	return redirect(url_for("articles.viewArticles"))