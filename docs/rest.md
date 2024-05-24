<!-- markdownlint-disable -->

<a href="../registraai/rest.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `rest`





---

<a href="../registraai/rest.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_balance`

```python
get_balance() → tuple[Response, int]
```

Retrieve the current balance. 

This endpoint returns the current balance of the user. The response is a JSON object containing the balance and additional metadata. 



**Returns:**
 
 - <b>`tuple[Response, int]`</b>:  A tuple where the first element is a Flask `Response` object containing the JSON payload and the second element is the HTTP status code. 

Response JSON Structure: { 
 - <b>`"balance"`</b>:  float,   # The current balance amount 
 - <b>`"message"`</b>:  str,     # A message containing the current balance } 

Example Response: HTTP/1.1 200 OK 
 - <b>`Content-Type`</b>:  application/json { 
 - <b>`"balance"`</b>:  100.50, 
 - <b>`"message"`</b>:  "Saldo atual: R$100.50" } 


---

<a href="../registraai/rest.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `post_gain`

```python
post_gain() → tuple[Response, int]
```

Process and record a gain. 

This endpoint processes and records a gain from the request data. It expects a JSON payload with the required fields. If the request body is incomplete, it returns a 400 error with an appropriate message. 

Returns: tuple[Response, int]: A tuple where the first element is a Flask `Response` object containing the JSON payload and the second element is the HTTP status code. 

Request JSON Structure:  {  "amount": float,     # The amount of the gain  "description": str   # A description of the gain  } 

Response JSON Structure (200):  {  "message": str,            # A message of success with the new  # balance  "registered_gain": dict,   # A dictionary with the fields "amount"  # and "description" from the gain record  "balance": float           # The new balance after the registered  # gain  } 

Error Response JSON Structure (400):  {  "message": str,       # A message with the error reason  "status_code": int    # The status code of the response  } 

Example Success Response:  HTTP/1.1 200 OK  Content-Type: application/json  {  "message": "Ganho registrado! Agora você tem R$100.50"  "registered_gain": {  "amount": 100.50,  "description": "Found in my old pants"  },  "balance": 100.50  } 

Example Error Response:  HTTP/1.1 400 Bad Request  Content-Type: application/json  {  "status_code": 400,  "message": "Body sem campo 'amount'"  } 


---

<a href="../registraai/rest.py#L174"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `post_expense`

```python
post_expense()
```

Process and record an expense. 

This endpoint processes and records an expense from the request data. It expects a JSON payload with the required fields. If the request body is incomplete, it returns a 400 error with an appropriate message. 

Returns: tuple[Response, int]: A tuple where the first element is a Flask `Response` object containing the JSON payload and the second element is the HTTP status code. 

Request JSON Structure:  {  "amount": float,     # The amount of the gain  "description": str   # A description of the gain  } 

Response JSON Structure (200):  {  "message": str,               # A message of success with the new  # balance  "registered_expense": dict,   # A dictionary with the fields  # "amount" and "description" from the  # expense record  "balance": float              # The new balance after the registered  # expense  } 

Error Response JSON Structure (400):  {  "message": str,       # A message with the error reason  "status_code": int    # The status code of the response  } 

Example Success Response:  HTTP/1.1 200 OK  Content-Type: application/json  {  "message": "Gasto registrado! Agora você tem R$50.50"  "registered_expense": {  "amount": 50.00  "description": "Buy new pants"  },  "balance": 50.50  } 

Example Error Response:  HTTP/1.1 400 Bad Request  Content-Type: application/json  {  "status_code": 400,  "message": "Body sem campo 'amount'"  } 


---

<a href="../registraai/rest.py#L251"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_history`

```python
get_history() → tuple[Response, int]
```

Retrieve the history of all records. 

This endpoint returns a list of all records. Each record contains information about individual transactions or events. 



**Returns:**
 
 - <b>`tuple[Response, int]`</b>:  A tuple where the first element is a Flask `Response` object containing the JSON payload and the second element is the HTTP status code. 

Response JSON Structure (200): [  { 
 - <b>`"amount"`</b>:  float,      # The amount associated with the record 
 - <b>`"description"`</b>:  str,   # A description of the record 
 - <b>`"ts"`</b>:  str             # The timestamp of when the record was  # created }, ... ] 

Example Success Response: HTTP/1.1 200 OK 
 - <b>`Content-Type`</b>:  application/json [  { 
 - <b>`"amount"`</b>:  100.50, 
 - <b>`"description"`</b>:  "Found in my old pants", 
 - <b>`"ts"`</b>:  "2024-05-23T10:00:00Z" }, { 
 - <b>`"amount"`</b>:  -50.00, 
 - <b>`"description"`</b>:  "Buy new pants", 
 - <b>`"ts"`</b>:  "2024-05-24T15:30:00Z" } ] 


---

<a href="../registraai/rest.py#L296"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `add_cors_headers`

```python
add_cors_headers(response)
```

Add CORS headers to the response. 

This function is called after each request to add Cross-Origin Resource Sharing (CORS) headers to the response, allowing cross-origin requests from any origin. It enables the client to send requests with the specified headers and methods. 

Args: response (Response): The Flask response object to which CORS headers will be added. 

Returns: Response: The modified response object with added CORS headers. 

Added Headers: 
    - Access-Control-Allow-Origin: Allows requests from any origin (`*`). 
    - Access-Control-Allow-Headers: Allows `Content-Type` and  `Authorization` headers. 
    - Access-Control-Allow-Methods: Allows `GET`, `PUT`, `POST`, and  `DELETE` methods. 


---

<a href="../registraai/rest.py#L325"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `before_request`

```python
before_request()
```

Initialize the database connection pool before each request. 

This function is called before each request to initialize the connection pool, ensuring that database connections are ready to be used by the request handlers. It sets up necessary resources required for handling the request. 



**Returns:**
  None 


---

<a href="../registraai/rest.py#L340"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `teardown_appcontext`

```python
teardown_appcontext(exception)
```

Release the connection pool after each request. 

This function is called after each request to release the database connection pool, ensuring that all connections are properly closed and resources are cleaned up. It helps maintain the stability and performance of the application by managing the connection lifecycle. 



**Args:**
 
 - <b>`exception`</b> (Exception):  The exception that was raised during the request, if any. 



**Returns:**
 None 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
