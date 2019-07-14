from database import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable= False)

    def __repr__(self):
        return f'<User {self.email}, {self.password}>'

class Todos(db.Model):
    todo_id =  db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    todo_title = db.Column(db.String(255), nullable=False)
    todo_body = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Todo {self.todo_id} from User {user_id} Title: {todo_title} Body:\n{todo_body}\n Completed {self.completed}>'

