#!/usr/bin/env python3
"""Implement class SessionAuth"""

from api.v1.auth.auth import Auth
from models.user import User
import uuid
import os


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
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns the user ID associated with the given session ID.

        :param session_id: The session ID for which to retrieve the user ID.
        :type session_id: str, optional
        :return: The user ID associated with the session ID, or None if the
        session ID is None or not a string.
        :rtype: str or None
        """
        if session_id is None:
            return None
        elif not isinstance(session_id, str):
            return None
        else:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieve the current user based on the provided request.

        Parameters:
            request (optional): The HTTP request object (default: None).

        Returns:
            The current User object associated with the provided request.
        """
        session_cookie = self.session_cookie(request)

        user_id_for_session = self.user_id_for_session_id(session_cookie)

        return User.get(user_id_for_session)

    def destroy_session(self, request=None):
        """
        Destroy the session.

        :param request: The request object. (default: None)
        :type request: object
        :return: True if the session was
        successfully destroyed, False otherwise.
        :rtype: bool
        """
        if request is None:
            return False
        elif not self.session_cookie(request):
            return False
        else:
            session_id = request.cookies.get(os.getenv("SESSION_NAME"))
            del self.user_id_by_session_id[session_id]
            return True
