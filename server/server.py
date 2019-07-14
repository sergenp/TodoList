from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from database import app, db
from models import User
from sqlalchemy.exc import IntegrityError
from validator import email_validator, password_validator

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db.create_all()


@cross_origin()
@app.route("/register", methods=['POST'])
def register():
    content = request.get_json()
    email, password = content['email'], content['password']
    email_match, password_match = email_validator(email), password_validator(password)
    if email_match == None:
        abort(400, description="Invalid email")

    elif password_match == None:
        error_msg = "The password provided failed to match the following rules: <br> \
1. It must contain ONLY the following characters: lower case, upper case, numerics.<br> \
2. It must be at least 8 characters in length and not greater than 32 characters in length."
        abort(400, description=error_msg)

    user = User(email=email, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': "You have been succesfully registered! Enjoy.",
        })
    except IntegrityError:
        abort(400, description="This e-mail already in use")

@app.route("/login", methods=['POST'])
def login():
    content = request.get_json()
    email, password = content['email'], content['password']
    return jsonify({
        'message' : 'Logged in'
    })

@app.errorhandler(400)
def bad_request_handler(e):
    e = str(e).replace("400 Bad Request:", "")
    return jsonify(error=(e)), 400

if __name__ == "__main__":
    app.run(port=8081)
