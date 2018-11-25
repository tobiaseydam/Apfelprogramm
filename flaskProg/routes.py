from flaskProg import app
from flaskProg.customers.routes import customers
from flaskProg.fruits.routes import fruits

app.register_blueprint(customers)
app.register_blueprint(fruits)