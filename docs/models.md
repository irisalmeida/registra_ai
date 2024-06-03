<!-- markdownlint-disable -->

<a href="../registraai/models.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `models`






---

<a href="../registraai/models.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `User`




<a href="../registraai/models.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: 'str', name: 'str', email: 'str', profile_pic: 'str')
```

Initialize a User object. 



**Args:**
 
 - <b>`id`</b> (str):  The unique identifier for the user. 
 - <b>`name`</b> (str):  The name of the user. 
 - <b>`email`</b> (str):  The email address of the user. 
 - <b>`profile_pic`</b> (str):  The URL of the user's profile picture. 


---

#### <kbd>property</kbd> is_active





---

#### <kbd>property</kbd> is_anonymous





---

#### <kbd>property</kbd> is_authenticated







---

<a href="../registraai/models.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create(id: 'str', name: 'str', email: 'str', profile_pic: 'str') → User
```

Create a new user in the database. 

This method inserts a new user into the database with the provided details. 



**Args:**
 
 - <b>`id`</b> (str):  The unique identifier for the user. 
 - <b>`name`</b> (str):  The name of the user. 
 - <b>`email`</b> (str):  The email address of the user. 
 - <b>`profile_pic`</b> (str):  The URL of the user's profile picture. 



**Example:**
 ``` User.create("123", "John Doe", "john@example.com", "http://example.com/john.jpg")```
    <User object at 0x...>


---

<a href="../registraai/models.py#L140"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expense`

```python
expense(amount: 'float', description: 'str') → Record
```

Create a new expense record for the user. 

This method creates a new expense record in the database with the provided amount and description, associated with the current user. The amount is stored as a negative value. 



**Args:**
 
 - <b>`amount`</b> (float):  The amount of the expense. This value will be  stored as a negative number. 
 - <b>`description`</b> (str):  A description of the expense. 



**Returns:**
 
 - <b>`Record | None`</b>:  A `Record` object if the expense record is  successfully created, otherwise `None`. 



**Example:**
 ``` user = User("123", "John Doe", "john@example.com", "http://example.com/john.jpg")```
    >>> user.expense(50.0, "Grocery shopping")
    <Record object at 0x...>


---

<a href="../registraai/models.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `gain`

```python
gain(amount: 'float', description: 'str') → Record
```

Create a new gain record for the user. 

This method creates a new gain record in the database with the provided amount and description, associated with the current user. The amount is stored as a positive value. 



**Args:**
 
 - <b>`amount`</b> (float):  The amount of the gain. This value will be stored  as a positive number. 
 - <b>`description`</b> (str):  A description of the gain. 



**Returns:**
 
 - <b>`Record | None`</b>:  A `Record` object if the gain record is successfully created, otherwise `None`. 



**Example:**
 ``` user = User("123", "John Doe", "john@example.com", "http://example.com/john.jpg")```
    >>> user.gain(100.0, "Salary payment")
    <Record object at 0x...>

    (In case of some error)
    >>> user.gain(100.0, "Salary payment")
    None


---

<a href="../registraai/models.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(user_id: 'str') → User | None
```

Retrieve a user by their user ID. 

This method retrieves a user from the database using their user ID. It returns a `User` object if the user is found, otherwise `None`. 



**Args:**
 
 - <b>`user_id`</b> (str):  The ID of the user to be retrieved. 



**Returns:**
 
 - <b>`User | None`</b>:  A `User` object if the user is found, otherwise `None`. 



**Example:**
 ``` User.get("123")```
    <User object at 0x...>

    >>> User.get("nonexistent_id")
    None


---

<a href="../registraai/models.py#L166"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_records`

```python
get_records() → list[Record]
```

Retrieve all records for the user. 

This method retrieves all records from the database associated with the current user. 



**Returns:**
 
 - <b>`list[Record]`</b>:  A list of `Record` objects associated with the user. 



**Example:**
 ``` user = User("123", "John Doe", "john@example.com", "http://example.com/john.jpg")```
    >>> user.get_records()
    [<Record object at 0x...>, <Record object at 0x...>, ...]

    (If no records are found)
    >>> user.get_records()
    []


---

<a href="../registraai/models.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → dict[str, Any]
```

Convert the User object to a dictionary. 

This method converts the User object to a dictionary representation. 



**Returns:**
 
 - <b>`dict[str, Any]`</b>:  A dictionary containing the user's details. 



**Example:**
 ``` user = User("123", "John Doe", "john@example.com", "http://example.com/john.jpg")```
    >>> user.to_dict()
    {
         "id": "123",
         "username": "John Doe",
         "email": "john@example.com",
         "profile_pic": "http://example.com/john.jpg"
    }



---

<a href="../registraai/models.py#L188"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Record`
Represents a financial record. 

This class models a financial record, of gain or expense of money, with attributes including amount, description, and the creation time. 



**Attributes:**
 
 - <b>`id`</b> (int):  The ID of the record in the database. 
 - <b>`user_id`</b> (str):  The ID of the user that registered the record. 
 - <b>`amount`</b> (float):  The amount associated with the record. 
 - <b>`description`</b> (str):  A description of the record. 
 - <b>`created_at`</b> (datetime):  The datetime timestamp of the record. 

Static Methods: 
 - <b>`create`</b>:  Create a new record in the database. 
 - <b>`get_all`</b>:  Retrieve all records from the database. 

Methods: 
 - <b>`to_dict`</b>:  Convert the record object to a dictionary. 

<a href="../registraai/models.py#L210"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    id: 'int',
    user_id: 'str',
    amount: 'float',
    description: 'str',
    created_at: 'datetime'
) → None
```

Initialize a Record object. 



**Args:**
 
 - <b>`id`</b> (int):  The ID of the record in the database. 
 - <b>`user_id`</b> (str):  The ID of the user that registered the record. 
 - <b>`amount`</b> (float):  The amount associated with the record. 
 - <b>`description`</b> (str):  A description of the record. 
 - <b>`created_at`</b> (datetime):  The datetime timestamp of the record. 




---

<a href="../registraai/models.py#L251"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `create`

```python
create(user_id: 'str', amount: 'float', description: 'str') → Record
```

Create a new record in the database. 

This method inserts a new record into the database with the provided details and returns an equivalent Record object. 



**Args:**
 
 - <b>`user_id`</b> (str):  The ID of the user that registered the record. 
 - <b>`amount`</b> (float):  The amount associated with the record. 
 - <b>`description`</b> (str):  A description of the record. 



**Returns:**
 
 - <b>`Record | None`</b>:  The `Record` object created. 



**Example:**
 ``` Record.create("123", 50.0, "Found in my old pants")```
    <Record object at 0x...>


---

<a href="../registraai/models.py#L279"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all`

```python
get_all(user_id: 'str') → list[Record]
```

Retrieve all records of a user from the database. 

This method retrieves all records from the database associated with the given user ID and returns them as a list of `Record` objects. 



**Args:**
 
 - <b>`user_id`</b> (str):  The ID of the user whose records are to be retrieved. 



**Returns:**
 
 - <b>`list[Record]`</b>:  A list of `Record` objects associated with the user. 



**Example:**
 ``` Record.get_all("123")```
    [<Record object at 0x...>, <Record object at 0x...>, ...]

    (If no records are found)
    >>> Record.get_all("123")
    []


---

<a href="../registraai/models.py#L227"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → dict[str, Any]
```

Convert the record object to a dictionary. 

This method converts the record object to a dictionary representation. 



**Returns:**
 
 - <b>`dict[str, Any]`</b>:  A dictionary containing the record's details, with keys corresponding to the record's attributes. 



**Example:**
 ``` record = Record(1, "123", 50.0, "Found in my old pants", datetime.now())```
    >>> record.to_dict()
    {
         'id': 1,
         'user_id': '123',
         'amount': 50.0,
         'description': 'Found in my old pants',
         'created_at': datetime.datetime(...)
    }





---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
