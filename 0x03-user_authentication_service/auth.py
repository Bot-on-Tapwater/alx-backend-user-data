#!/usr/bin/env python3
"""Implement _hash_password"""
import bcrypt
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from db import DB
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Generates a hash of the input password using bcrypt.

    Args:
        password (str): The input password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    Generate a UUID and return it as a string.

    :return: A string representing the UUID.
    :rtype: str
    """
    new_uuid = str(uuid.uuid4())
    # print(f"UUID: {new_uuid} TYPE: {type(new_uuid)}")
    return new_uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the provided email and password.

        Args:
            email (str): The email of the user to be registered.
            password (str): The password of the user to be registered.

        Returns:
            User: The newly registered user.
        """
        try:
            new_user = self._db.find_user_by(email=email)
            raise ValueError(f"Users {email} already exists")
        except NoResultFound:
            new_user = self._db.add_user(email, _hash_password(password))
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check if the login credentials are valid.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Create a session for the given email.

        Args:
            email (str): The email of the user.

        Returns:
            Union[str, None]: The session ID if successful,
            None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)

            session_id = _generate_uuid()

            user.session_id = session_id

            self._db._session.commit()

            return session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, str]:
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the user's session by
        setting the session_id to None in the database.

        Args:
            user_id (int): The id of the user whose session will be destroyed.

        Returns:
            None: If the user does not exist in the database.
        """
        user = self._db.find_user_by(id=user_id)

        user.session_id = None

        self._db._session.commit()

        return None
