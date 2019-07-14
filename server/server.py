from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from database import db
from models import User

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db.create_all()


@cross_origin()
@app.route("/register", methods=['POST'])
async def register():
    content = request.get_json()
    email = content['email']
    password = content['password']
    user = await User(email=email, password=password)
    return jsonify({
        'message' : "Succesfully created",
        'User' : user
    })

if __name__ == "__main__":
    app.run(port=8081)
