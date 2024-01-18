#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if os.getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif os.getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif os.getenv('AUTH_TYPE') == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def filter_request():
    """
    Decorator function to filter requests before they are processed.

    This function is used as a decorator for the
    `before_request` method of the `app` object.
    It filters incoming requests based on the
    authentication status and the path of the request.

    Parameters:
        None

    Returns:
        None

    Raises:
        401: If the request requires
        authentication and the authorization header is missing.
        403: If the request requires
        authentication and the current user is not authorized.
    """

    if auth is not None:
        paths = ['/api/v1/status/',
                 '/api/v1/unauthorized/', '/api/v1/forbidden/',
                 '/api/v1/auth_session/login/']
        if auth.require_auth(request.path, paths):
            if (auth.authorization_header(request) is None
                    and auth.session_cookie(request) is None):
                abort(401)
            if auth.current_user(request) is None:
                abort(403)
        request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    A function that handles the 401 Unauthorized error.

    Parameters:
    - error: The error object that triggered the error handler.

    Returns:
    - str: A JSON response containing the error message.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handler function for 403 Forbidden error.

    Args:
        error: The error object.

    Returns:
        str: A JSON response with the error
        message and the HTTP status code 403.
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
