from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "KD Backend Running"

@app.route("/api/test")
def test():
    return jsonify({"status": "working"})
