#!/usr/bin/env python3
""" Auth class """

from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """
    Class to manage the API authentic
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to require authentication.
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[-1] != "/":
            path += "/"

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to get the value of the header request 'Authorization'.
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Method to get the current user.
        """
        return None
