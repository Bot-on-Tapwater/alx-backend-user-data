#!/usr/bin/env python3
"""Implement BasicAuth class"""

from api.v1.auth.auth import Auth
import base64
import binascii


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
