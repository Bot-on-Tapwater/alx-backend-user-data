#!/usr/bin/env python3
"""Implement _hash_password"""
import bcrypt


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
