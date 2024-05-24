<!-- markdownlint-disable -->

<a href="../registraai/controller.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `controller`





---

<a href="../registraai/controller.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_all_records`

```python
get_all_records() → list[dict[str, str | float]]
```

Retrieve all records. 

This function fetches all records from the database using the `Record` model. 



**Returns:**
 
 - <b>`list[dict]`</b>:  A list of dictionaries, each representing a record with its details. 



**Example:**
 [  {  "amount": 100.50,  "description": "Found in my old pants",  "ts": "2024-05-23T10:00:00Z"  },  {  "amount": -50.00,  "description": "Buy new pants",  "ts": "2024-05-24T15:30:00Z"  } ] 


---

<a href="../registraai/controller.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_balance`

```python
get_balance() → float
```

Calculate the total balance. 

This function calculates the total balance by summing up the amounts of all registered gains and expenses. 



**Returns:**
 
 - <b>`float`</b>:  The total balance after all registered gains and expenses. 



**Example:**
 If there are records with amounts [100.50, -50.00], the function will return 50.50. 


---

<a href="../registraai/controller.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `register_gain`

```python
register_gain(amount: float, description: str) → dict
```

Register a money gain. 

This function registers a money gain by creating a new record with the specified amount and description. The amount is stored as a positive value. 



**Args:**
 
 - <b>`amount`</b> (float):  The amount of the gain. 
 - <b>`description`</b> (str):  A description of the gain. 



**Returns:**
 
 - <b>`dict`</b>:  A dictionary representing the newly created record. 



**Example:**
 {  "record_id": 3,  "amount": 150.00,  "description": "Freelance work",  "timestamp": "2024-05-25T08:45:00Z" } 


---

<a href="../registraai/controller.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `register_expense`

```python
register_expense(amount: float, description: str) → dict
```

Register a money expense. 

This function registers a money expense by creating a new record with the specified amount and description. The amount is stored as a negative value. 



**Args:**
 
 - <b>`amount`</b> (float):  The amount of the expense. 
 - <b>`description`</b> (str):  A description of the expense. 



**Returns:**
 
 - <b>`dict`</b>:  A dictionary representing the newly created record. 



**Example:**
 {  "amount": -75.00,  "description": "Grocery shopping",  "timestamp": "2024-05-26T14:20:00Z" } 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
