from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/register", methods=['POST'])
def register():
    return jsonify({
        'message' : "Succesfully recieved",
        'content' : request.get_json()
    })

if __name__ == "__main__":
	app.run(port=8081)
