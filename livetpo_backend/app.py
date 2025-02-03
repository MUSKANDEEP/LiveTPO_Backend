from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Live TPO Placement System API!"})

if __name__ == '__main__':
    app.run(debug=True)
