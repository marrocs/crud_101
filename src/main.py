from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@123@localhost:5432/crud_app'
db.init_app(app)

@app.route('/')
def helloWorld():
    return "<p>Home</p>"

@app.route('/create-order?product=<product>&quantity=<quantity>')
def createOrder():
    return

