<!-- markdownlint-disable -->

<a href="../registraai/rest.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `rest`




**Global Variables**
---------------
- **FRONTEND_URL**
- **GOOGLE_CLIENT_ID**
- **GOOGLE_CLIENT_SECRET**
- **GOOGLE_DISCOVERY_URL**

---

<a href="../registraai/rest.py#L151"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `load_user`

```python
load_user(user_id: str) → UserMixin | None
```

Load a user by their user ID. 

This function is used by Flask-Login to load a user from the user ID stored in the session. It expects a user ID as a string and returns a `UserMixin` object if the user is found, otherwise `None`. 



**Args:**
 
 - <b>`user_id`</b> (str):  The ID of the user to be loaded. 



**Returns:**
 
 - <b>`UserMixin | None`</b>:  A `UserMixin` object if the user is found, otherwise `None`. 



**Example:**
 ``` load_user("123")```
    <UserMixin object at 0x...>

    >>> load_user("nonexistent_id")
    None



---

<a href="../registraai/rest.py#L177"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_google_provider_cfg`

```python
get_google_provider_cfg() → dict[str, Any]
```

Get the Google OAuth2 provider configuration. 

This function makes a GET request to the Google Discovery URL to fetch the OAuth2 provider configuration, including details like the authorization endpoint, token endpoint, etc. 



**Returns:**
 
 - <b>`Dict[str, Any]`</b>:  A dictionary containing the Google OAuth2 provider configuration. 



**Example:**
 ``` get_google_provider_cfg()```
    {
         "issuer": "https://accounts.google.com",
         "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
         "token_endpoint": "https://oauth2.googleapis.com/token",
         ...
    }



---

<a href="../registraai/rest.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `login`

```python
login()
```

Initiate the Google OAuth2 login process. 

This endpoint retrieves the Google OAuth2 provider configuration, prepares the request URI for OAuth2 authorization, and redirects the user to the Google authorization page for login. 



**Returns:**
 
 - <b>`redirect`</b>:  Redirects the user to the Google authorization page for login. 


---

<a href="../registraai/rest.py#L225"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `callback`

```python
callback()
```

Callback endpoint for handling the OAuth2 authorization code and logging in the user. 

This endpoint receives the authorization code from Google, exchanges it for an access token, retrieves user information, creates or retrieves the user from the database, logs the user in, and redirects them to the frontend URL. 



**Returns:**
 
 - <b>`redirect`</b>:  Redirects the user to the frontend URL after successful login. 
 - <b>`jsonify`</b>:  Returns a JSON response with an error message if the user email is not available or verified. 


---

<a href="../rest/logout#L292"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `logout`

```python
logout()
```

Logout the currently authenticated user. 

This endpoint logs out the currently authenticated user and returns a JSON response confirming the logout. 



**Returns:**
 
 - <b>`jsonify`</b>:  A JSON response indicating successful logout. 



**Example:**
 ``` logout()```
    {"status": "ok", "message": "Logout success"}



---

<a href="../rest/get_user#L314"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_user`

```python
get_user()
```

Get user data for the currently authenticated user. 

This endpoint retrieves user data for the currently authenticated user and returns it as a JSON response. 



**Returns:**
 
 - <b>`tuple[Response, int]`</b>:  A tuple where the first element is a Flask `Response` object containing the JSON payload and the second element is the HTTP status code. 

Request JSON Structure: N/A (GET request) 

Response JSON Structure (200): { 
 - <b>`"id"`</b>:  str,          # The user's ID 
 - <b>`"username"`</b>:  str,    # The user's username 
 - <b>`"email"`</b>:  str,       # The user's email address 
 - <b>`"profile_pic"`</b>:  str  # The URL of the user's profile picture } 

Error Response JSON Structure (401): { 
 - <b>`"error"`</b>:  str        # Error message indicating unauthorized access } 

Error Response JSON Structure (400): { 
 - <b>`"error"`</b>:  str        # Error message indicating user not found } 

Example Success Response: HTTP/1.1 200 OK 
 - <b>`Content-Type`</b>:  application/json { 
 - <b>`"id"`</b>:  "123", 
 - <b>`"username"`</b>:  "John Doe", 
 - <b>`"email"`</b>:  "john@example.com", 
 - <b>`"profile_pic"`</b>:  "http://example.com/john.jpg" } 

Example Unauthorized Access Response: HTTP/1.1 401 Unauthorized 
 - <b>`Content-Type`</b>:  application/json { 
 - <b>`"status"`</b>:  "error", 
 - <b>`"reason"`</b>:  "Unauthorized access" } 

Example User Not Found Response: HTTP/1.1 400 Bad Request 
 - <b>`Content-Type`</b>:  application/json { 
 - <b>`"status"`</b>:  "error", 
 - <b>`"reason"`</b>:  "User not found" } 


---

<a href="../rest/get_balance#L384"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_balance`

```python
get_balance() → tuple[Response, int]
```

Retrieve the current balance. 

This endpoint returns the current balance of the user. The response is a JSON object containing the balance and additional metadata. 



**Returns:**
 
 - <b>`tuple[Response, int]`</b>:  A tuple where the first element is a Flask `Response` object containing the JSON payload and the second element is the HTTP status code. 

Response JSON Structure: { 
 - <b>`"balance"`</b>:  float   # The current balance amount } 

Example Response: HTTP/1.1 200 OK 
 - <b>`Content-Type`</b>:  application/json { 
 - <b>`"balance"`</b>:  100.50 } 


---

<a href="../rest/post_gain#L433"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `post_gain`

```python
post_gain() → tuple[Response, int]
```

Process and record a gain. 

This endpoint processes and records a gain from the request data. It expects a JSON payload with the required fields. If the request body is incomplete, it returns a 400 error with an appropriate message. 

Returns: tuple[Response, int]: A tuple where the first element is a Flask `Response` object containing the JSON payload and the second element is the HTTP status code. 

Request JSON Structure:  {  "amount": float,     # The amount of the gain  "description": str   # A description of the gain  } 

Response JSON Structure (200):  {  "record": dict,    # A dictionary with the registered record  "balance": float   # The new balance after the registered record  } 

Error Response JSON Structure (400):  {  "status": str          # An error status  "reason": str          # The reason of the error  "additional_info": {   # Aditional information about the error  ...  }  }  {  "status": str          # An error status  "reason": str          # The reason of the error  } 

Example Success Response:  HTTP/1.1 200 OK  Content-Type: application/json  {  "record": {  "amount": 100.50,  "description": "Found in my old pants"  },  "balance": 100.50  } 

example error response:  http/1.1 400 bad request  content-type: application/json  {  "status": "error",  "reason": "missing body fields",  "additional_info": {  "missing_fields": ["amount", "description"]  }  } 


---

<a href="../rest/post_expense#L564"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `post_expense`

```python
post_expense()
```

Process and record an expense. 

This endpoint processes and records an expense from the request data. It expects a JSON payload with the required fields. If the request body is incomplete, it returns a 400 error with an appropriate message. 

Returns: tuple[Response, int]: A tuple where the first element is a Flask `Response` object containing the JSON payload and the second element is the HTTP status code. 

Request JSON Structure:  {  "amount": float,     # The amount of the expense  "description": str   # A description of the expense  } 

Response JSON Structure (200):  {  "record": dict,    # A dictionary with the registered record  "balance": float   # The new balance after the registered record  } 

Error Response JSON Structure (400):  {  "status": str          # An error status  "reason": str          # The reason of the error  "additional_info": {   # Aditional information about the error  ...  }  }  {  "status": str          # An error status  "reason": str          # The reason of the error  } 

Example Success Response:  HTTP/1.1 200 OK  Content-Type: application/json  {  "record": {  "amount": -50.25,  "description": "Buy new pants"  },  "balance": 50.25  } 

Example Error Response:  HTTP/1.1 400 Bad Request  Content-Type: application/json  {  "status": "error",  "reason": "Missing body fields",  "additional_info": {  "missing_fields": ["amount", "description"]  }  } 


---

<a href="../registraai/rest.py#L694"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../registraai/rest.py#L761"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `before_request`

```python
before_request()
```

Initialize the database connection pool before each request. 

This function is called before each request to initialize the connection pool, ensuring that database connections are ready to be used by the request handlers. It sets up necessary resources required for handling the request. 



**Returns:**
  None 


---

<a href="../registraai/rest.py#L777"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `teardown_appcontext`

```python
teardown_appcontext(exception)
```

Release the connection pool after each request. 

This function is called after each request to release the database connection pool, ensuring that all connections are properly closed and resources are cleaned up. It helps maintain the stability and performance of the application by managing the connection lifecycle. 

Args: exception (Exception): The exception that was raised during the request, if any. 



**Returns:**
  None 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
