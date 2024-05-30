from __future__ import annotations
from datetime import datetime
from typing import Any
from db import execute_query

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id: str, name: str, email: str, profile_pic: str):
        """
        Initialize a User object.

        Args:
            id (str): The unique identifier for the user.
            name (str): The name of the user.
            email (str): The email address of the user.
            profile_pic (str): The URL of the user's profile picture.
        """
        self.id:str = id
        self.name:str = name
        self.email:str = email
        self.profile_pic:str = profile_pic
        self.records = []

    @staticmethod
    def get(user_id: str) -> User | None:
        """
        Retrieve a user by their user ID.

        This method retrieves a user from the database using their user ID. It
        returns a `User` object if the user is found, otherwise `None`.

        Args:
            user_id (str): The ID of the user to be retrieved.

        Returns:
            User | None: A `User` object if the user is found, otherwise
            `None`.

        Example:
            >>> User.get("123")
            <User object at 0x...>

            >>> User.get("nonexistent_id")
            None
        """
        query = "select_user_by_id.sql"
        values = (user_id,)
        results = execute_query(query, values)

        if not results:
            return None

        user_data = results[0]
        user = User(
            id=user_data[0], name=user_data[1], email=user_data[2],
            profile_pic=user_data[3]
        )
        return user

    @staticmethod
    def create(id: str, name: str, email: str, profile_pic: str) -> User:
        """
        Create a new user in the database.

        This method inserts a new user into the database with the provided
        details.

        Args:
            id (str): The unique identifier for the user.
            name (str): The name of the user.
            email (str): The email address of the user.
            profile_pic (str): The URL of the user's profile picture.

        Example:
            >>> User.create("123", "John Doe", "john@example.com", "http://example.com/john.jpg")
            <User object at 0x...>
        """
        query = "insert_user.sql"
        values = (id, name, email, profile_pic)
        execute_query(query, values)
        return User(id, name, email, profile_pic)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the User object to a dictionary.

        This method converts the User object to a dictionary representation.

        Returns:
            dict[str, Any]: A dictionary containing the user's details.

        Example:
            >>> user = User("123", "John Doe", "john@example.com", "http://example.com/john.jpg")
            >>> user.to_dict()
            {
                "id": "123",
                "username": "John Doe",
                "email": "john@example.com",
                "profile_pic": "http://example.com/john.jpg"
            }
        """
        return {
            "id": self.id,
            "username": self.name,
            "email": self.email,
            "profile_pic": self.profile_pic,
        }

    def gain(self, amount: float, description: str) -> Record:
        """
        Create a new gain record for the user.

        This method creates a new gain record in the database with the provided
        amount and description, associated with the current user. The amount is
        stored as a positive value.

        Args:
            amount (float): The amount of the gain. This value will be stored
                as a positive number.
            description (str): A description of the gain.

        Returns:
            Record | None: A `Record` object if the gain record is successfully
            created, otherwise `None`.

        Example:
            >>> user = User("123", "John Doe", "john@example.com", "http://example.com/john.jpg")
            >>> user.gain(100.0, "Salary payment")
            <Record object at 0x...>

            (In case of some error)
            >>> user.gain(100.0, "Salary payment")
            None
        """
        record = Record.create(self.id, amount, description)
        return record

    def expense(self, amount: float, description: str) -> Record:
        """
        Create a new expense record for the user.

        This method creates a new expense record in the database with the
        provided amount and description, associated with the current user. The
        amount is stored as a negative value.

        Args:
            amount (float): The amount of the expense. This value will be
                stored as a negative number.
            description (str): A description of the expense.

        Returns:
            Record | None: A `Record` object if the expense record is
                successfully created, otherwise `None`.

        Example:
            >>> user = User("123", "John Doe", "john@example.com", "http://example.com/john.jpg")
            >>> user.expense(50.0, "Grocery shopping")
            <Record object at 0x...>
        """
        negative_amount = amount * -1
        record = Record.create(self.id, negative_amount, description)
        return record

    def get_records(self) -> list[Record]:
        """
        Retrieve all records for the user.

        This method retrieves all records from the database associated with the
        current user.

        Returns:
            list[Record]: A list of `Record` objects associated with the user.

        Example:
            >>> user = User("123", "John Doe", "john@example.com", "http://example.com/john.jpg")
            >>> user.get_records()
            [<Record object at 0x...>, <Record object at 0x...>, ...]

            (If no records are found)
            >>> user.get_records()
            []
        """
        records = Record.get_all(self.id)
        return records

class Record:
    """
    Represents a financial record.

    This class models a financial record, of gain or expense of money, with
    attributes including amount, description, and the creation time.

    Attributes:
        id (int): The ID of the record in the database.
        user_id (str): The ID of the user that registered the record.
        amount (float): The amount associated with the record.
        description (str): A description of the record.
        created_at (datetime): The datetime timestamp of the record.

    Static Methods:
        create: Create a new record in the database.
        get_all: Retrieve all records from the database.

    Methods:
        to_dict: Convert the record object to a dictionary.
    """

    def __init__(self, id: int, user_id: str, amount: float, description: str, created_at: datetime) -> None:
        """
        Initialize a Record object.

        Args:
            id (int): The ID of the record in the database.
            user_id (str): The ID of the user that registered the record.
            amount (float): The amount associated with the record.
            description (str): A description of the record.
            created_at (datetime): The datetime timestamp of the record.
        """
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.description = description
        self.created_at = created_at

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the record object to a dictionary.

        This method converts the record object to a dictionary representation.

        Returns:
            dict[str, Any]: A dictionary containing the record's details, with
            keys corresponding to the record's attributes.

        Example:
            >>> record = Record(1, "123", 50.0, "Found in my old pants", datetime.now())
            >>> record.to_dict()
            {
                'id': 1,
                'user_id': '123',
                'amount': 50.0,
                'description': 'Found in my old pants',
                'created_at': datetime.datetime(...)
            }
        """
        rec = vars(self).copy()
        return rec

    @staticmethod
    def create(user_id: str, amount: float, description: str) -> Record:
        """
        Create a new record in the database.

        This method inserts a new record into the database with the provided
        details and returns an equivalent Record object.

        Args:
            user_id (str): The ID of the user that registered the record.
            amount (float): The amount associated with the record.
            description (str): A description of the record.

        Returns:
            Record | None: The `Record` object created.

        Example:
            >>> Record.create("123", 50.0, "Found in my old pants")
            <Record object at 0x...>
        """
        query = "insert_record.sql"
        created_at = datetime.now()
        values = (user_id, amount, description, created_at)

        query_result:list[tuple[int,]] = execute_query(query, values) # type: ignore
        record_id = query_result[0][0]
        return Record(record_id, user_id, amount, description, created_at)

    @staticmethod
    def get_all(user_id: str) -> list[Record]:
        """
        Retrieve all records of a user from the database.

        This method retrieves all records from the database associated with the
        given user ID and returns them as a list of `Record` objects.

        Args:
            user_id (str): The ID of the user whose records are to be retrieved.

        Returns:
            list[Record]: A list of `Record` objects associated with the user.

        Example:
            >>> Record.get_all("123")
            [<Record object at 0x...>, <Record object at 0x...>, ...]

            (If no records are found)
            >>> Record.get_all("123")
            []
        """
        query = "get_records.sql"
        values = (user_id,)
        result = execute_query(query, values)

        if result is None:
            return []

        all_records = []
        for row in result:
            id, _, amount, description, created_at = row
            record = Record(id, user_id, amount, description, created_at)
            all_records.append(record)

        return all_records
