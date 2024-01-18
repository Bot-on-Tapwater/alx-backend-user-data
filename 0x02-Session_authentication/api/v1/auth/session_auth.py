#!/usr/bin/env python3
"""Implement class SessionAuth"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Class SessionAuth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session for a user.

        Args:
            user_id (str): The ID of the user. Defaults to None.

        Returns:
            str: The session ID generated for the user.

        Raises:
            None

        Notes:
            - If the user_id is None, None is returned.
            - If the user_id is not a string, None is returned.
        """
        if user_id is None:
            return None
        elif not isinstance(user_id, str):
            return None
        else:
            session_id = uuid.uuid4()
            self.user_id_by_session_id[session_id] = user_id
            return session_id
