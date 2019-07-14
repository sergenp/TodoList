from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@cross_origin()
@app.route("/register", methods=['POST'])
def register():
    return jsonify({
        'message' : "Succesfully recieved",
        'content' : request.get_json()
    })

if __name__ == "__main__":
	app.run(port=8081)
