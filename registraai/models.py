from __future__ import annotations
from datetime import datetime
from typing import Any
from db import execute_query

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id_: str, name: str, email: str, profile_pic: str):
        """
        Initialize a User object.

        Args:
            id_ (str): The unique identifier for the user.
            name (str): The name of the user.
            email (str): The email address of the user.
            profile_pic (str): The URL of the user's profile picture.
        """
        self.id:str = id_
        self.name:str = name
        self.email:str = email
        self.profile_pic:str = profile_pic

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
            id_=user_data[0], name=user_data[1], email=user_data[2], profile_pic=user_data[3]
        )
        return user


    @staticmethod
    def create(id_: str, name: str, email: str, profile_pic: str) -> None:
        """
        Create a new user in the database.

        This method inserts a new user into the database with the provided
        details.

        Args:
            id_ (str): The unique identifier for the user.
            name (str): The name of the user.
            email (str): The email address of the user.
            profile_pic (str): The URL of the user's profile picture.

        Example:
            >>> User.create("123", "John Doe", "john@example.com",
                            "http://example.com/john.jpg")
        """
        query = "insert_user.sql"
        values = (id_, name, email, profile_pic)
        execute_query(query, values)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the User object to a dictionary.

        This method converts the User object to a dictionary representation.

        Returns:
            dict[str, Any]: A dictionary containing the user's details.

        Example:
            >>> user = User("123", "John Doe", "john@example.com",
                            "http://example.com/john.jpg")
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

    def get_records(self) -> list[dict[str, str | float]]:
        query = "get_user_records.sql"
        values = (self.id,)
        results = execute_query(query, values)

        if results is None:
            return []

        records = []
        for rec in results:
            record = {
                "id": rec[0],
                "user_id": rec[1],
                "amount": rec[2],
                "description": rec[3],
                "ts": rec[4],
            }
            records.append(record)

        return records


class Record():
    """
    Represents a financial record.

    This class models a financial record, such as a transaction or event,
    with attributes including amount, description, and timestamp.

    Attributes:
        amount (float): The amount associated with the record.
        description (str): A description of the record.
        ts (Optional[datetime]): The timestamp of the record (default: current time).

    Methods:
        to_dict(): Convert the record object to a dictionary.
        save(): Save the record to the database.
        get_all(): Retrieve all records from the database.
    """

    def __init__(self, user_id: str, amount: float, description: str, ts: datetime | None = None) -> None:
        """
        Initialize a Record object.

        Args:
            amount (float): The amount associated with the record.
            description (str): A description of the record.
            ts (Optional[datetime]): The timestamp of the record (default: current time).
        """
        self.user_id = user_id
        self.amount = amount
        self.description = description
        self.ts = datetime.now() if ts is None else ts

    def to_dict(self) -> dict:
        """
        Convert the record object to a dictionary.

        Returns:
            dict: A dictionary representation of the record.
        """
        rec = vars(self).copy()
        return rec

    def save(self) -> bool:
        """
        Save the record to the database.

        Returns:
            bool: True if the record was successfully saved, False otherwise.
        """
        query = "insert_table_records.sql"

        values = (self.amount, self.description, self.ts)

        try:
            execute_query(query, values)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_all() -> list[dict[str,str|float]]:
        """
        Retrieve all records from the database.

        Returns:
            list[dict[str, str | float]]: A list of dictionaries, each representing a record with its details.
        """
        query = "select_all_records.sql"
        result = execute_query(query)

        if result is None:
            return []

        all_records = []
        for row in result:
            _, amount, description, ts = row
            record = Record(amount, description, ts)
            all_records.append(record.to_dict())

        return all_records
