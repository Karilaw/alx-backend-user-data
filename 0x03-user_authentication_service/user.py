#!/usr/bin/env python3
"""
This module defines a User class that interacts
with the 'users' table in the database.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    The User class represents a 'users' table in a database.

    Attributes:
        id (Integer): The primary key.
        email (String): The user's email. It is non-nullable.
        hashed_password (String): The user's hashed password.
        session_id (String): The user's session ID. It is nullable.
        reset_token (String): The user's reset token. It is nullable.
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: str = Column(String(250), nullable=True)
    reset_token: str = Column(String(250), nullable=True)
