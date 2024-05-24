from datetime import datetime
from typing import Optional
from db import load_query, execute_query


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

    def __init__(self, amount:float, description:str, ts:Optional[datetime]=None) -> None:
        """
        Initialize a Record object.

        Args:
            amount (float): The amount associated with the record.
            description (str): A description of the record.
            ts (Optional[datetime]): The timestamp of the record (default: current time).
        """
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
        insert_record_query = "insert_table_records.sql"
        query = load_query(insert_record_query)

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
        query = load_query("select_all_records.sql")
        result = execute_query(query)

        if result is None:
            return []

        all_records = []
        for row in result:
            _, amount, description, ts = row
            record = Record(amount, description, ts)
            all_records.append(record.to_dict())

        return all_records
