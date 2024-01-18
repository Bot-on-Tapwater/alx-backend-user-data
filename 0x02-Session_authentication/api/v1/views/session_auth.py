#!/usr/bin/env python3
""" Module of session_auth views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_authentication():
    """
    Authenticates a user session by checking the provided email and password.

    Returns:
        - If the email is missing or empty: a
        JSON response with an error message and a status code of 400.
        - If the password is missing or empty: a
        JSON response with an error message and a status code of 400.
        - If no user is found with the provided
        email: a JSON response with an error message and a status code of 400.
        - If the password is incorrect: a JSON
        response with an error message and a status code of 401.
        - If the email and password are correct:a
        JSON response with the user information
        and a session ID, and a status code of 200.
    """
    try:
        email = request.form.get("email")

        if email == '' or email is None:
            return jsonify({"error": "email missing"}), 400
    except Exception:
        return jsonify({"error": "email missing"}), 400

    try:
        password = request.form.get("password")

        if password == '' or password is None:
            return jsonify({"error": "password missing"}), 400
    except Exception:
        return jsonify({"error": "password missing"}), 400

    all_users = User.search({"email": email})
    if all_users == [] or not all_users:
        return jsonify({"error": "no user found for this email"}), 400
    for user in all_users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())

            session_name = os.getenv('SESSION_NAME')
            response.set_cookie(session_name, session_id)
            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logout a user session.

    Returns:
        A JSON response with an empty dictionary
        and a status code of 200 if the session is successfully destroyed.
        Otherwise, it aborts the request with a status code of 404.
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
