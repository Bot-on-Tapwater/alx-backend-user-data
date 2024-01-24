#!/usr/bin/env python3
"""Implement flask app"""
from flask import Flask, jsonify, request, abort, redirect, url_for
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


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    Route for logging in, takes email and password from
    form data and validates the login.
    If valid, creates a session and returns a JSON response with
    the email and a success message,
    also setting a session ID cookie. If not
    valid, aborts with a 401 status code.
    Returns a JSON response.
    """
    email = request.form['email']
    password = request.form['password']

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)

        response = jsonify({"email": f"{email}", "message": "logged in"})

        response.set_cookie('session_id', session_id)

        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect(url_for('index'))
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
