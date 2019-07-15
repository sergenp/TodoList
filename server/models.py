from database import db
from passlib.hash import bcrypt

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
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        reprDict = {
            "todo_id" : self.todo_id,
            "todo_title" : self.todo_title,
            "todo_body" : self.todo_body,
            "completed" : self.completed
        }
        return str(reprDict)
