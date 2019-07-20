# library imports
from flask import request, jsonify, abort
from flask_cors import CORS, cross_origin
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import datetime

# custom imports
from database import app, db
from models import User, Todos
from validator import email_validator, password_validator

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['CORS_HEADERS'] = ['Content-Type', 'Authorization']
CORS(app)
jwt = JWTManager(app)
db.create_all()


@cross_origin()
@app.route("/register", methods=['POST'])
def register():
    if not request.is_json:
        abort(400, description="Missing JSON in request")
    content = request.get_json()
    email, password = content['email'], content['password']
    email_match, password_match = email_validator(
        email), password_validator(password)
    if email_match == None:
        abort(400, description="Invalid email")

    elif password_match == None:
        error_msg = "The password provided failed to match the following rules: <br> 1. It must contain ONLY the following characters: lower case, upper case, numerics.<br> 2. It must be at least 8 characters in length and not greater than 32 characters in length."
        abort(400, description=error_msg)

    user = User(email=email, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(
            identity=str(user.email), expires_delta=expires)
        return jsonify({
            'user': {
                'user_id': user.user_id,
                'email': user.email,
            },
            'token': access_token
        })
    except IntegrityError:
        abort(400, description="This e-mail already in use")


@cross_origin()
@app.route("/login", methods=['POST'])
def login():
    if not request.is_json:
        abort(400, description="Missing JSON in request")

    content = request.get_json()
    email, password = content['email'], content['password']
    user = db.session.query(User).filter(User.email == email).first()
    if not user:
        abort(403, description="Login information is incorrect")

    if not (user.validate_password(password)):
        abort(403, description="Login information is incorrect")

    expires = datetime.timedelta(days=7)
    access_token = create_access_token(
        identity=str(user.email), expires_delta=expires)
    return jsonify({
        'user': {
            'user_id': user.user_id,
            'email': user.email
        },
        'token': access_token
    })


@cross_origin()
@app.route("/getTodos", methods=['GET'])
@jwt_required
def getTodos():
    current_user = get_jwt_identity()
    user = db.session.query(User).filter(User.email == current_user).first()
    if user:
        todo_list = []
        todos = db.session.query(Todos).filter(Todos.user_id == user.user_id).all()
        for todo in todos:
            todo_list.append({
                'todo_title' : todo.todo_title,
                'todo_body' : todo.todo_body,
                'completed' : todo.completed,
                'created_at' : todo.created_at,
                'completed_at' : todo.completed_at
            })
        return jsonify(todo_list)
    else:
        abort(401, description="You are not allowed to visit this page")


@cross_origin
@app.route("/saveTodos", methods=['POST'])
@jwt_required
def saveTodos():
    if not request.is_json:
        abort(400, description="Missing JSON in request")

    current_user = get_jwt_identity()
    user = db.session.query(User).filter(User.email == current_user).first()
    if user:
        try:
            num_rows_deleted = db.session.query(Todos).filter(Todos.user_id==user.user_id).delete()
            content = request.get_json()
            for todo in content:
                todo_title = todo['todo_title']
                todo_body = todo['todo_body']
                completed = todo["completed"]
                created_at = todo["created_at"]
                completed_at = todo["completed_at"]
                todoModel = Todos(user_id=user.user_id, todo_title=todo_title, todo_body=todo_body,
                            completed=completed, completed_at=completed_at, created_at=created_at)
                db.session.add(todoModel)
            db.session.commit()
            return jsonify({
                'message' : 'Saved successfully',
                'todo' : content            
            })
        except Exception:
            abort(500)
    else:
        abort(401, description="You are not allowed to visit this page")


@app.errorhandler(403)
def forbidden(e):
    e = str(e).replace("403 Forbidden:", "")
    return(jsonify(error=e)), 403


@app.errorhandler(400)
def bad_request_handler(e):
    e = str(e).replace("400 Bad Request:", "")
    return jsonify(error=(e)), 400


if __name__ == "__main__":
    app.run(port=8081)
