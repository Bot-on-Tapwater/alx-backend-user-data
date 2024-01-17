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
            return decoded_string.decode()
        except Exception:
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
            return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns User instance based on their email and password"""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None

        try:
            all_users = User.search({"email": user_email})
            if all_users == [] or not all_users:
                return None
            for user in all_users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the provided request.

        Parameters:
            request (Optional[Request]): The request object that contains the
            authorization header. Defaults to None.

        Returns:
            User: An instance of the User class representing the current user.

        """
        auth_header = self.authorization_header(request)

        auth_header = self.extract_base64_authorization_header(auth_header)

        decoded_header = self.decode_base64_authorization_header(auth_header)

        credentials = self.extract_user_credentials(decoded_header)

        return self.user_object_from_credentials(*credentials)
