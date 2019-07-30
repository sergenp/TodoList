from database import db
from passlib.hash import bcrypt
from time import gmtime, strftime

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable= False)
    todos = db.relationship('Todos', backref='user', lazy=True)
    todosCategories = db.relationship('TodosCategories', backref='user', lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.encrypt(password)

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)

    def __repr__(self):
        reprDict = {
            "email" : self.email,
            "password" : self.password
        }
        return str(reprDict)

class Todos(db.Model):
    todo_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    todo_title = db.Column(db.String(255), nullable=False)
    todo_body = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.String(255), nullable=False, default=None)
    completed_at = db.Column(db.String(255), nullable=True, default=None)
    todosCategories = db.relationship('TodosCategories', backref='todos', lazy=True)

    def __repr__(self):
        reprDict = {
            "user_id" : self.user_id,
            "todo_id" : self.todo_id,
            "todo_title" : self.todo_title,
            "todo_body" : self.todo_body,
            "completed" : self.completed,
            "created_at" : self.created_at,
            "completed_at" : self.completed_at
        }
        return str(reprDict)

class TodosCategories(db.Model):
    todo_category_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todos.todo_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    todo_category_desc = db.Column(db.String(255), nullable=False)
    todo_category_title = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        reprDict = {
            "user_id" : self.user_id,
            "todo_id" : self.todo_id,
            "todo_title" : self.todo_title,
            "todo_body" : self.todo_body,
            "completed" : self.completed,
            "created_at" : self.created_at,
            "completed_at" : self.completed_at
        }
        return str(reprDict)