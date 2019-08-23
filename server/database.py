from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

try:
    os.mkdir("db")
except FileExistsError:
    pass

file_path = os.path.abspath(os.getcwd())+"\\db\\database.db"
app = Flask("TodosServer")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
