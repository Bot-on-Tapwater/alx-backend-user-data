#!/usr/bin/env python3
"""Implement BasicAuth class"""

from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the base64 authorization header
        from the given authorization_header string.

        Args:
            self: The instance of the class.
            authorization_header (str): The authorization header string.

        Returns:
            str: The extracted base64 authorization header.

        Raises:
            None.

        Examples:
            extract_base64_authorization_header(None, "") -> None
            extract_base64_authorization_header(None, "Invalid Header") -> None
            extract_base64_authorization_header
            (None, "Basic ABC123") -> "ABC123"
        """
        if authorization_header is None:
            return None
        elif not isinstance(authorization_header, str):
            return None
        elif not authorization_header.startswith("Basic "):
            return None
        else:
            return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Decodes a base64-encoded authorization header.

        Args:
            base64_authorization_header (str): The
            base64-encoded authorization header.

        Returns:
            str: The decoded authorization header.
            Returns None if the input is invalid.
        """
        if base64_authorization_header is None:
            return None
        elif not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_string = base64.b64decode(base64_authorization_header)
            return decoded_string.decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Extracts user credentials from a decoded base64 authorization header.

        Parameters:
            decoded_base64_authorization_header
            (str): The decoded base64 authorization header.

        Returns:
            tuple: A tuple containing two elements: the username and password
            extracted from the authorization header.
            If the authorization header is None,
            not a string, or does not contain a
            colon (':'), it returns (None, None).
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        elif not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        elif ':' not in decoded_base64_authorization_header:
            return (None, None)
        else:
            return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Generate a User object from the given credentials.

        Args:
            user_email (str): The email address of the user.
            user_pwd (str): The password of the user.

        Returns:
            User: The User object if the credentials are valid, None otherwise.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        elif user_pwd is None or not isinstance(user_pwd, str):
            return None

        current_user = User.search({'email': user_email})

        if not current_user:
            return None

        elif not current_user[0].is_valid_password(user_pwd):
            return None
        else:
            return current_user[0]
