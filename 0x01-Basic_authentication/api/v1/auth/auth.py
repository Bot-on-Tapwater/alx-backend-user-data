#!/usr/bin/env python3
"""Implement Auth Class"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Implement class Auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for a given path.

        Args:
            path (str): The path to check for authentication.
            excluded_paths (List[str]): A list of
            paths that are excluded from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
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
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user.

        Args:
            request (Optional[Request]): The request object (default: None).

        Returns:
            User: The current user.

        """
        return None
