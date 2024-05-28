from models import Record, User


def get_user(user_id: str) -> User | None:
    """
    Retrieve a user by their user ID.

    This function retrieves a user from the database using their user ID. It
    returns a `UserMixin` object if the user is found, otherwise `None`.

    Args:
        user_id (str): The ID of the user to be retrieved.

    Returns:
        UserMixin | None: A `UserMixin` object if the user is found,
        otherwise `None`.

    Example:
        >>> get_user("123")
        <UserMixin object at 0x...>

        >>> get_user("nonexistent_id")
        None
    """
    return User.get(user_id)


def get_or_create_user(google_id: str, name: str, email: str, picture: str) -> User:
    """
    Get or create a user in the system.

    This function attempts to retrieve a user with the provided Google ID from
    the system. If the user doesn't exist, a new user is created and returned.

    Args:
        google_id (str): The Google ID of the user.
        name (str): The name of the user.
        email (str): The email address of the user.
        picture (str): The URL of the user's profile picture.

    Returns:
        User: A `User` object representing the user, either retrieved or newly
        created.

    Example:
        >>> get_or_create_user("123456789", "John Doe", "john@example.com",
                               "http://example.com/john.jpg")
        <User object at 0x...>
    """
    user = User(
        id_=google_id, name=name, email=email, profile_pic=picture
    )

    if not User.get(google_id):
        User.create(google_id, name, email, picture)

    return user


def get_records(user_id: str) -> list[dict[str,str|float]]:
    """
    Retrieve all records from a user.

    This function fetches all records that belongs to the user_id from the
    database using the `Record` model.

    Args:
        user_id (str): The id of the user to get the records.

    Returns:
        list[dict]: A list of dictionaries, each representing a record with its
                    details.

    Example:
        [
            {
                "user_id": "1234",
                "amount": 100.50,
                "description": "Found in my old pants",
                "ts": "2024-05-23T10:00:00Z"
            },
            {
                "user_id": "1234",
                "amount": -50.00,
                "description": "Buy new pants",
                "ts": "2024-05-24T15:30:00Z"
            }
        ]
    """
    user = get_user(user_id)
    if user is None:
        return []
    records = user.get_records()
    return records


def get_balance(user_id: str) -> float:
    """
    Calculate the total balance of a user.

    This function calculates the total balance by summing up the amounts of all
    registered gains and expenses from a user based on its user_id.

    Args:
        user_id (str): The id of the user to get the balence.

    Returns:
        float: The total balance after all registered gains and expenses.

    Example:
        If there are records with amounts [100.50, -50.00], the function will
        return 50.50.
    """
    user = get_user(user_id)
    if user is None:
        return 0

    all_records = user.get_records()
    balance = sum([float(rec['amount']) for rec in all_records])
    return round(balance, 2)


def register_gain(user_id: str, amount:float, description:str) -> dict:
    """
    Register a money gain.

    This function registers a money gain by creating a new record with the
    specified amount and description for the user_id. The amount is stored as a
    positive value.

    Args:
        user_id (str): The id of the user registering the gain.
        amount (float): The amount of the gain.
        description (str): A description of the gain.

    Returns:
        dict: A dictionary representing the newly created record.

    Example:
        {
            "user_id": "123",
            "record_id": 3,
            "amount": 150.00,
            "description": "Freelance work",
            "ts": "2024-05-25T08:45:00Z"
        }
    """
    rec = Record(user_id, amount, description)
    rec.save()
    return rec.to_dict()


def register_expense(user_id: str, amount:float, description:str) -> dict:
    """
    Register a money expense.

    This function registers a money expense by creating a new record with the
    specified amount and description for the user_id. The amount is stored as a
    negative value.

    Args:
        user_id (str): The id of the user registering the expense.
        amount (float): The amount of the expense.
        description (str): A description of the expense.

    Returns:
        dict: A dictionary representing the newly created record.

    Example:
        {
            "user_id": "123",
            "record_id": 4,
            "amount": -75.00,
            "description": "Grocery shopping",
            "ts": "2024-05-26T14:20:00Z"
        }
    """
    negative_amount = amount * -1
    rec = Record(user_id, negative_amount, description)
    rec.save()
    return rec.to_dict()
