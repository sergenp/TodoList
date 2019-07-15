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