"""Implement flask app"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    form = {"message": "Bienvenue"}
    return jsonify(form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
