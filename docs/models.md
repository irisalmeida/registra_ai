<!-- markdownlint-disable -->

<a href="../registraai/models.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `models`






---

<a href="../registraai/models.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Record`
Represents a financial record. 

This class models a financial record, such as a transaction or event, with attributes including amount, description, and timestamp. 



**Attributes:**
 
 - <b>`amount`</b> (float):  The amount associated with the record. 
 - <b>`description`</b> (str):  A description of the record. 
 - <b>`ts`</b> (Optional[datetime]):  The timestamp of the record (default: current time). 

Methods: 
 - <b>`to_dict`</b> ():  Convert the record object to a dictionary. 
 - <b>`save`</b> ():  Save the record to the database. 
 - <b>`get_all`</b> ():  Retrieve all records from the database. 

<a href="../registraai/models.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(amount: float, description: str, ts: Optional[datetime] = None) → None
```

Initialize a Record object. 



**Args:**
 
 - <b>`amount`</b> (float):  The amount associated with the record. 
 - <b>`description`</b> (str):  A description of the record. 
 - <b>`ts`</b> (Optional[datetime]):  The timestamp of the record (default: current time). 




---

<a href="../registraai/models.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_all`

```python
get_all() → list[dict[str, str | float]]
```

Retrieve all records from the database. 



**Returns:**
 
 - <b>`list[dict[str, str | float]]`</b>:  A list of dictionaries, each representing a record with its details. 

---

<a href="../registraai/models.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `save`

```python
save() → bool
```

Save the record to the database. 



**Returns:**
 
 - <b>`bool`</b>:  True if the record was successfully saved, False otherwise. 

---

<a href="../registraai/models.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dict`

```python
to_dict() → dict
```

Convert the record object to a dictionary. 



**Returns:**
 
 - <b>`dict`</b>:  A dictionary representation of the record. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
