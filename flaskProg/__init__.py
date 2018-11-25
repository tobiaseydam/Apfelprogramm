from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FPyIEWFIS2henqadkOh4NrqVarUhbefX6h56QIAc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passwd@localhost/Apfeldb'
db = SQLAlchemy(app)

from flaskProg import routes