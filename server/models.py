from database import db
from passlib.hash import bcrypt
from time import gmtime, strftime

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable= False)

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
    todo_id =  db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    todo_title = db.Column(db.String(255), nullable=False)
    todo_body = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    finished_at = db.Column(db.DateTime, nullable=True, default=None)

    def __init__(self, user_id, todo_title, todo_body, completed):
        self.user_id = user_id
        self.todo_title = todo_title
        self.todo_body = todo_body
        self.completed = completed

    def __repr__(self):
        reprDict = {
            "todo_id" : self.todo_id,
            "todo_title" : self.todo_title,
            "todo_body" : self.todo_body,
            "completed" : self.completed
        }
        return str(reprDict)
