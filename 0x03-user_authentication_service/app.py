#!/usr/bin/env python3
"""Implement flask app"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
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


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    Handle POST requests to create new users.

    Retrieves email and password from the request form and attempts to
    register a new user with the provided credentials.

    Returns:
        - If successful, it returns a JSON
        response with the new user's email and a success message.
        - If the email is already registered,
        it returns a JSON response with an
        error message and status code 400.
    """
    email = request.form['email']  # retrieve email from the request form
    password = request.form['password']

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
