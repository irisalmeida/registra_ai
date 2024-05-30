from models import Record, User

def get_user(user_id: str) -> User:
    """
    Retrieve a user by their user ID.

    This function retrieves a user from the database using their user ID. It
    returns a `User` object if the user is found, otherwise `None`.

    Args:
        user_id (str): The ID of the user to be retrieved.

    Returns:
        User: A `User` object if the user is found, otherwise `None`.

    Raises:
        Exception: If the user_id is not found, raises an Exception.

    Example:
        >>> get_user("123")
        <User object at 0x...>

        >>> get_user("nonexistent_id")
        Exception: User id not found: nonexistent_id
    """
    user = User.get(user_id)
    if user is None:
        raise Exception(f"User id not found: {user_id}")
    return user


def get_or_create_user(google_id: str, name: str, email: str, picture: str) -> User | None:
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
        User | None: A `User` object representing the user, either retrieved or newly
        created.

    Example:
        >>> get_or_create_user("123456789", "John Doe", "john@example.com",
                               "http://example.com/john.jpg")
        <User object at 0x...>
    """
    try:
        user = get_user(google_id)
    except Exception:
        user = User.create(google_id, name, email, picture)

    return user


def get_records(user_id: str) -> list[Record]:
    """
    Retrieve all records for a user.

    This function fetches all records that belong to the user with the
    specified user ID from the database using the `Record` model.

    Args:
        user_id (str): The ID of the user to get the records.

    Returns:
        list[Record] | None: A list of `Record` objects if records are found,
                             otherwise `None`.

    Raises:
        Exception: If the user_id is not found, raises an Exception.

    Example:
        >>> get_records("1234")
        [<Record object at 0x...>, <Record object at 0x...>]

        >>> get_records("nonexistent_id")
        Exception: User id not found: nonexistent_id
    """
    user = get_user(user_id)
    records = user.get_records()
    return records


def get_balance(user_id: str) -> float:
    """
    Calculate the total balance of a user.

    This function calculates the total balance by summing up the amounts of all
    registered gains and expenses for the user with the specified user ID.

    Args:
        user_id (str): The ID of the user to get the balance.

    Returns:
        float | None: The total balance after all registered gains and expenses,
                      or `None` if the user is not found.

    Raises:
        Exception: If the user_id is not found, raises an Exception.

    Example:
        If there are records with amounts [100.50, -50.00], the function will
        return 50.50.

        >>> get_balance("123")
        50.50

        >>> get_balance("nonexistent_id")
        Exception: User id not found: nonexistent_id
    """
    user = get_user(user_id)

    user_records = user.get_records()
    balance = sum([float(rec.amount) for rec in user_records])

    return round(balance, 2)


def register_gain(user_id: str, amount: float, description: str) -> Record:
    """
    Register a money gain.

    This function registers a money gain by creating a new record with the
    specified amount and description for the user with the specified user ID.
    The amount is stored as a positive value.

    Args:
        user_id (str): The ID of the user registering the gain.
        amount (float): The amount of the gain.
        description (str): A description of the gain.

    Returns:
        Record | None: A `Record` object representing the newly created gain.

    Raises:
        Exception: If the user_id is not found, raises an Exception.

    Example:
        >>> register_gain("123", 150.00, "Freelance work")
        <Record object at 0x...>

        >>> register_gain("nonexistent_id", 150.00, "Freelance work")
        Exception: User id not found: nonexistent_id
    """
    user = get_user(user_id)

    record = user.gain(amount, description)

    return record


def register_expense(user_id: str, amount: float, description: str) -> Record:
    """
    Register a money expense.

    This function registers a money expense by creating a new record with the
    specified amount and description for the user with the specified user ID.
    The amount is stored as a negative value.

    Args:
        user_id (str): The ID of the user registering the expense.
        amount (float): The amount of the expense.
        description (str): A description of the expense.

    Returns:
        Record | None: A `Record` object representing the newly created
                       expense, or `None` if the user is not found.

    Raises:
        Exception: If the user_id is not found, raises an Exception.

    Example:
        >>> register_expense("123", 75.00, "Grocery shopping")
        <Record object at 0x...>

        >>> register_expense("nonexistent_id", 75.00, "Grocery shopping")
        Exception: User id not found: nonexistent_id
    """
    user = get_user(user_id)

    record = user.expense(amount, description)

    return record
