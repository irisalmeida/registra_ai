<!-- markdownlint-disable -->

<a href="../registraai/controller.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `controller`





---

<a href="../registraai/controller.py#L3"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_user`

```python
get_user(user_id: str) → User
```

Retrieve a user by their user ID. 

This function retrieves a user from the database using their user ID. It returns a `User` object if the user is found, otherwise `None`. 



**Args:**
 
 - <b>`user_id`</b> (str):  The ID of the user to be retrieved. 



**Returns:**
 
 - <b>`User`</b>:  A `User` object if the user is found, otherwise `None`. 



**Raises:**
 
 - <b>`Exception`</b>:  If the user_id is not found, raises an Exception. 



**Example:**
 ``` get_user("123")```
    <User object at 0x...>

    >>> get_user("nonexistent_id")
    Exception: User id not found: nonexistent_id



---

<a href="../registraai/controller.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_or_create_user`

```python
get_or_create_user(
    google_id: str,
    name: str,
    email: str,
    picture: str
) → User | None
```

Get or create a user in the system. 

This function attempts to retrieve a user with the provided Google ID from the system. If the user doesn't exist, a new user is created and returned. 



**Args:**
 
 - <b>`google_id`</b> (str):  The Google ID of the user. 
 - <b>`name`</b> (str):  The name of the user. 
 - <b>`email`</b> (str):  The email address of the user. 
 - <b>`picture`</b> (str):  The URL of the user's profile picture. 



**Returns:**
 
 - <b>`User | None`</b>:  A `User` object representing the user, either retrieved or newly created. 



**Example:**
 ``` get_or_create_user("123456789", "John Doe", "john@example.com",```
                            "http://example.com/john.jpg")
    <User object at 0x...>



---

<a href="../registraai/controller.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_records`

```python
get_records(user_id: str) → list[Record]
```

Retrieve all records for a user. 

This function fetches all records that belong to the user with the specified user ID from the database using the `Record` model. 



**Args:**
 
 - <b>`user_id`</b> (str):  The ID of the user to get the records. 



**Returns:**
 
 - <b>`list[Record] | None`</b>:  A list of `Record` objects if records are found,  otherwise `None`. 



**Raises:**
 
 - <b>`Exception`</b>:  If the user_id is not found, raises an Exception. 



**Example:**
 ``` get_records("1234")```
    [<Record object at 0x...>, <Record object at 0x...>]

    >>> get_records("nonexistent_id")
    Exception: User id not found: nonexistent_id



---

<a href="../registraai/controller.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_balance`

```python
get_balance(user_id: str) → float
```

Calculate the total balance of a user. 

This function calculates the total balance by summing up the amounts of all registered gains and expenses for the user with the specified user ID. 



**Args:**
 
 - <b>`user_id`</b> (str):  The ID of the user to get the balance. 



**Returns:**
 
 - <b>`float | None`</b>:  The total balance after all registered gains and expenses,  or `None` if the user is not found. 



**Raises:**
 
 - <b>`Exception`</b>:  If the user_id is not found, raises an Exception. 



**Example:**
 If there are records with amounts [100.50, -50.00], the function will return 50.50. 

``` get_balance("123")```
    50.50

    >>> get_balance("nonexistent_id")
    Exception: User id not found: nonexistent_id



---

<a href="../registraai/controller.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `register_gain`

```python
register_gain(user_id: str, amount: float, description: str) → Record
```

Register a money gain. 

This function registers a money gain by creating a new record with the specified amount and description for the user with the specified user ID. The amount is stored as a positive value. 



**Args:**
 
 - <b>`user_id`</b> (str):  The ID of the user registering the gain. 
 - <b>`amount`</b> (float):  The amount of the gain. 
 - <b>`description`</b> (str):  A description of the gain. 



**Returns:**
 
 - <b>`Record | None`</b>:  A `Record` object representing the newly created gain. 



**Raises:**
 
 - <b>`Exception`</b>:  If the user_id is not found, raises an Exception. 



**Example:**
 ``` register_gain("123", 150.00, "Freelance work")```
    <Record object at 0x...>

    >>> register_gain("nonexistent_id", 150.00, "Freelance work")
    Exception: User id not found: nonexistent_id



---

<a href="../registraai/controller.py#L159"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `register_expense`

```python
register_expense(user_id: str, amount: float, description: str) → Record
```

Register a money expense. 

This function registers a money expense by creating a new record with the specified amount and description for the user with the specified user ID. The amount is stored as a negative value. 



**Args:**
 
 - <b>`user_id`</b> (str):  The ID of the user registering the expense. 
 - <b>`amount`</b> (float):  The amount of the expense. 
 - <b>`description`</b> (str):  A description of the expense. 



**Returns:**
 
 - <b>`Record | None`</b>:  A `Record` object representing the newly created  expense, or `None` if the user is not found. 



**Raises:**
 
 - <b>`Exception`</b>:  If the user_id is not found, raises an Exception. 



**Example:**
 ``` register_expense("123", 75.00, "Grocery shopping")```
    <Record object at 0x...>

    >>> register_expense("nonexistent_id", 75.00, "Grocery shopping")
    Exception: User id not found: nonexistent_id





---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
