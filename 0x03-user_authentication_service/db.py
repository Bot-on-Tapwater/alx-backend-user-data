#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base
from user import User
import logging

logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Creates and adds a new user to the database.

        Args:
            email (str): The email of the new user.
            hashed_password (str): The hashed password of the new user.

        Returns:
            User: The newly created user object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """
        Find a user by the provided keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            User: The first user found based on the provided keyword arguments.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If the request is invalid.
        """
        for keyword, value in kwargs.items():
            # print(f"KEYWORD: {keyword} VALUE: {value}")
            if hasattr(User, keyword):
                # print(f"REQUEST IS VALID")
                first_user = self._session.query(User).filter_by(
                    **{keyword: value}).first()
                # print(f"FIRST USER: {first_user}")
                if first_user is not None:
                    # print(f"FIRST USER IS NOT NONE")
                    return first_user
                else:
                    # print(f"FIRST USER IS NONE")
                    raise NoResultFound()
            else:
                # print("REQUEST IS INVALID")
                raise InvalidRequestError()
