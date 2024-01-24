#!/usr/bin/env python3
"""Implement flask app"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index() -> str:
    """
    Route decorator for the index endpoint.
    No parameters.
    Returns a JSON response containing the form data as a string.
    """
    form = {"message": "Bienvenue"}
    return jsonify(form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
