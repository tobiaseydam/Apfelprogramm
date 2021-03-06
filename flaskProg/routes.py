from flaskProg import app
from flaskProg.customers.routes import customers
from flaskProg.fruits.routes import fruits
from flaskProg.boxes.routes import boxes
from flaskProg.deposits.routes import deposits
from flaskProg.articles.routes import articles
from flaskProg.purchases.routes import purchases

app.register_blueprint(customers)
app.register_blueprint(fruits)
app.register_blueprint(boxes)
app.register_blueprint(deposits)
app.register_blueprint(articles)
app.register_blueprint(purchases)