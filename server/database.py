from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

try:
	os.mkdir("db")
except FileExistsError:
	pass
	
file_path = os.path.abspath(os.getcwd())+"\\db\\database.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username