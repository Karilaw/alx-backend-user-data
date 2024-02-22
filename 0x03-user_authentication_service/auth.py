#!/usr/bin/env python3
"""
Auth module
"""
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password with bcrypt.

        Parameters:
            password (str): The password to hash.

        Returns:
            bytes: The hashed password.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user.

        Parameters:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user already exists with the passed email.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login.

        Parameters:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """
        Generate a new UUID.

        Returns:
            str: The string representation of the new UUID.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        Create a new session.

        Parameters:
            email (str): The user's email.

        Returns:
            str: The new session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
