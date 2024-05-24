from models import Record


def get_all_records() -> list[dict[str,str|float]]:
    """
    Retrieve all records.

    This function fetches all records from the database using the `Record` model.

    Returns:
        list[dict]: A list of dictionaries, each representing a record with its details.

    Example:
        [
            {
                "amount": 100.50,
                "description": "Found in my old pants",
                "ts": "2024-05-23T10:00:00Z"
            },
            {
                "amount": -50.00,
                "description": "Buy new pants",
                "ts": "2024-05-24T15:30:00Z"
            }
        ]
    """
    all_records =  Record.get_all()
    return all_records


def get_balance() -> float:
    """
    Calculate the total balance.

    This function calculates the total balance by summing up the amounts of all
    registered gains and expenses.

    Returns:
        float: The total balance after all registered gains and expenses.

    Example:
        If there are records with amounts [100.50, -50.00], the function will return 50.50.
    """
    all_records = get_all_records()
    balance = sum([float(rec['amount']) for rec in all_records])
    return balance


def register_gain(amount:float, description:str) -> dict:
    """
    Register a money gain.

    This function registers a money gain by creating a new record with the specified
    amount and description. The amount is stored as a positive value.

    Args:
        amount (float): The amount of the gain.
        description (str): A description of the gain.

    Returns:
        dict: A dictionary representing the newly created record.

    Example:
        {
            "record_id": 3,
            "amount": 150.00,
            "description": "Freelance work",
            "timestamp": "2024-05-25T08:45:00Z"
        }
    """
    rec = Record(amount, description)
    rec.save()
    return rec.to_dict()


def register_expense(amount:float, description:str) -> dict:
    """
    Register a money expense.

    This function registers a money expense by creating a new record with the specified
    amount and description. The amount is stored as a negative value.

    Args:
        amount (float): The amount of the expense.
        description (str): A description of the expense.

    Returns:
        dict: A dictionary representing the newly created record.

    Example:
        {
            "amount": -75.00,
            "description": "Grocery shopping",
            "timestamp": "2024-05-26T14:20:00Z"
        }
    """
    """Register a money expense. The value is stored as a negative value."""
    negative_amount = amount * -1
    rec = Record(negative_amount, description)
    rec.save()
    return rec.to_dict()
