#!/usr/bin/env python3
"""Implement Auth Class"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Implement class Auth"""
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """require auth method"""
        if path is not None and path[-1] != "/":
            path += "/"

        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if (path not in excluded_paths or path is None):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        Generates the authorization header for a given request.

        Args:
            request (optional): The request object
            for which to generate the authorization header.

        Returns:
            str: The generated authorization header string.
        """
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user.

        Args:
            request (Optional[Request]): The request object (default: None).

        Returns:
            User: The current user.

        """
        return None
