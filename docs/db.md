<!-- markdownlint-disable -->

<a href="../registraai/db.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `db`




**Global Variables**
---------------
- **db_config**

---

<a href="../registraai/db.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `load_query`

```python
load_query(name: str) → str
```

Load an SQL query from a file. 

This function reads an SQL query from a file in the 'sql' directory based on the given name. 



**Args:**
 
 - <b>`name`</b> (str):  The name of the SQL query file (without the file extension). 



**Returns:**
 
 - <b>`str`</b>:  The contents of the SQL query as a string. 


---

<a href="../registraai/db.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `execute_query`

```python
execute_query(query: str, values: tuple = ()) → None | list[tuple]
```

Execute an SQL query with optional parameters. 

This function executes the given SQL query with optional parameter values. 



**Args:**
 
 - <b>`query`</b> (str):  The SQL query to execute. 
 - <b>`values`</b> (tuple, optional):  The parameter values for the query (default: ()). 



**Returns:**
 
 - <b>`None|list[tuple]`</b>:  The result of the query, either a list of tuples or None. 


---

<a href="../registraai/db.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `init_db`

```python
init_db(app)
```

Initialize the database. 

This function initializes the database by creating the connection pool and creating tables. 



**Args:**
 
 - <b>`app`</b>:  The Flask application object. 


---

<a href="../registraai/db.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `init_pool`

```python
init_pool()
```

Initialize the connection pool. 

This function initializes the connection pool for database connections. 



**Raises:**
 
 - <b>`RuntimeError`</b>:  If the connection to the database fails after multiple attempts. 


---

<a href="../registraai/db.py#L125"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_tables`

```python
create_tables()
```

Create database tables. 

This function creates the necessary tables in the database. 



**Note:**

> The SQL query for creating tables must be defined in a file named 'create_table_records.sql' and placed in the 'sql' directory. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
