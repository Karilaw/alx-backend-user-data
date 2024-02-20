#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        Add a user to the database.

        Parameters:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by keyword arguments.

        Parameters:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            User: The first User object that matches the keyword arguments.

        Raises:
            NoResultFound: If no User object matches the keyword arguments.
            InvalidRequestError: If wrong query arguments are passed.
        """
        if not kwargs:
            raise InvalidRequestError("No keyword arguments provided.")

        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound("No user found with the provided arguments.")

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.

        Parameters:
            user_id (int): The id of the user to update.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None

        Raises:
            ValueError: If an argument that does
            not correspond to a user attribute is passed.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid arg: {key}")

        self._session.commit()
