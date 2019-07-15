#library imports
from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

#custom imports
from database import app, db
from models import User
from validator import email_validator, password_validator

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['CORS_HEADERS'] = 'Content-Type'
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
    email_match, password_match = email_validator(email), password_validator(password)
    if email_match == None:
        abort(400, description="Invalid email")

    elif password_match == None:
        error_msg = "The password provided failed to match the following rules: <br> 1. It must contain ONLY the following characters: lower case, upper case, numerics.<br> 2. It must be at least 8 characters in length and not greater than 32 characters in length."
        abort(400, description=error_msg)

    user = User(email=email, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=str(user))
        return jsonify({
        'user' : {
            'user_id' : user.user_id, 
            'email' : user.email,
            'password' : user.password
        },
        'token' : access_token
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
    
    access_token = create_access_token(identity=str(user))
    return jsonify({
        'user' : {
            'user_id' : user.user_id, 
            'email' : user.email,
            'password' : user.password
        },
        'token' : access_token
    })

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
