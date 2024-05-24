from typing import Any
from flask import Flask, g, jsonify, request, make_response, abort, Response

import controller
import db

app = Flask(__name__)

def _assert(
        condition: bool,
        status_code: int,
        reason: str,
        additional_info: dict[str, Any] | None = None
    ) -> None:
    """
    Check if condition is true. If it is not, abort request and make an error
    response with the provided status code, message, and additional
    information.

    Args:
        condition (bool): The condition that, if false, will cause the request
            to abort and receive an error response.
        status_code (int): The response's status code if the condition is
            false.
        message (str): The response's message if the condition is false.
        additional_info (dict[str, Any] | None, optional): Additional
            information to include in the error response if the condition is
            false. Default is None.

    Returns:
        This function does not return, but the error response will have the
        status code defined in the param and a JSON with 'status', 'reason',
        and optionally 'additional_info' fields. Example:

    Response JSON Structure:
        {
            "status": str                # Status text. In this case, "error"
            "reason": str                # The reason the request failed
            "additional_info": dict {    # Additional information about the
                ...                      # error reason
            }
        }

    Example error response:
        http/1.1 400 bad request
        content-type: application/json
        {
            "status": "error",
            "reason": "missing body fields",
            "additional_info": {
                "missing_fields": ["amount", "description"]
            }
        }
    """
    if condition:
        return
    _abort(status_code, reason, additional_info)


def _abort(
        status_code: int,
        reason: str,
        aditional_info: dict[str, Any] | None = None
    ) -> None:
    """
    Abort request and make an error response with the provided status code,
    reason, and additional information.

    Args:
        status_code (int): The response's status code.
        reason (str): The response's reason message.
        additional_info (dict[str, Any] | None, optional): Additional
            information to include in the response. Default is None.

    Returns:
        This function does not return, but the error response will have the
        status code defined in the param and a JSON with 'status', 'reason',
        and optionally 'additional_info' fields. Example:

    Response JSON Structure:
        {
            "status": str                # Status text. In this case, "error"
            "reason": str                # The reason the request failed
            "additional_info": dict {    # Additional information about the
                ...                      # error reason
            }
        }

    Example error response:
        http/1.1 400 bad request
        content-type: application/json
        {
            "status": "error",
            "reason": "missing body fields",
            "additional_info": {
                "missing_fields": ["amount", "description"]
            }
        }
    """
    res:dict[str,str|dict[str,Any]] = {
        "status": "error",
        "reason": reason,
    }
    if aditional_info is not None:
        res["aditional_info"] = aditional_info

    response = make_response(jsonify(res), status_code)
    abort(response)


@app.route("/balance")
def get_balance() -> tuple[Response,int]:
    """
    Retrieve the current balance.

    This endpoint returns the current balance of the user. The response is a
    JSON object containing the balance and additional metadata.

    Returns:
        tuple[Response, int]: A tuple where the first element is a Flask
        `Response` object containing the JSON payload and the second element is
        the HTTP status code.

    Response JSON Structure:
        {
            "balance": float   # The current balance amount
        }

    Example Response:
        HTTP/1.1 200 OK
        Content-Type: application/json
        {
            "balance": 100.50
        }

    """
    balance = controller.get_balance()

    res = {
        "balance": balance,
    }
    return jsonify(res), 200


@app.route("/gain", methods=["POST"])
def post_gain() -> tuple[Response, int]:
    """
    Process and record a gain.

    This endpoint processes and records a gain from the request data. It
    expects a JSON payload with the required fields. If the request body is
    incomplete, it returns a 400 error with an appropriate message.

    Returns: tuple[Response, int]: A tuple where the first element is a Flask
    `Response` object containing the JSON payload and the second element is the
    HTTP status code.

    Request JSON Structure:
        {
            "amount": float,     # The amount of the gain
            "description": str   # A description of the gain
        }

    Response JSON Structure (200):
        {
            "record": dict,    # A dictionary with the registered record
            "balance": float   # The new balance after the registered record
        }

    Error Response JSON Structure (400):
        {
            "status": str          # An error status
            "reason": str          # The reason of the error
            "additional_info": {   # Aditional information about the error
                ...
            }
        }
        {
            "status": str          # An error status
            "reason": str          # The reason of the error
        }

    Example Success Response:
        HTTP/1.1 200 OK
        Content-Type: application/json
        {
            "record": {
                "amount": 100.50,
                "description": "Found in my old pants"
            },
            "balance": 100.50
        }

    example error response:
        http/1.1 400 bad request
        content-type: application/json
        {
            "status": "error",
            "reason": "missing body fields",
            "additional_info": {
                "missing_fields": ["amount", "description"]
            }
        }
    """
    try:
        data = request.get_json()
    except Exception:
        data = {}

    required_fields = ["amount", "description"]
    missing_fields = []

    _assert(data is not None, 400, "Missing request body")

    for field in required_fields:
        if field not in data:
            missing_fields.append(field)

    _assert(not bool(missing_fields), 400, "Missing body fields", {
        "missing_fields": missing_fields })

    amount: int | float = data.get("amount") # type: ignore

    aditional_info = {
        "invalid_field": "amount",
        "reason": f"Must be a number. Got: {type(amount).__name__}"
    }
    _assert(isinstance(amount, int) or isinstance(amount, float),
            400, "Invalid field", aditional_info)

    aditional_info = {
        "invalid_field": "amount",
        "reason": f"Must be a positive number. Got: {amount}"
    }
    _assert(amount >= 0, 400, "Invalid field", aditional_info)

    description: str = data.get("description") # type: ignore

    aditional_info = {
        "invalid_field": "description",
        "reason": f"Must be a string. Got: {type(description).__name__}"
    }
    _assert(isinstance(description, str), 400, "Invalid field", aditional_info)

    aditional_info = {
        "invalid_field": "description",
        "reason": f"Can't be empty"
    }
    _assert(bool(description), 400, "Invalid field", aditional_info)

    rec = controller.register_gain(amount, description)
    balance = controller.get_balance()

    res = {
        "record": rec,
        "balance": balance
    }
    return jsonify(res), 200


@app.route("/expense", methods=["POST"])
def post_expense():
    """
    Process and record an expense.

    This endpoint processes and records an expense from the request data. It
    expects a JSON payload with the required fields. If the request body is
    incomplete, it returns a 400 error with an appropriate message.

    Returns: tuple[Response, int]: A tuple where the first element is a Flask
    `Response` object containing the JSON payload and the second element is the
    HTTP status code.

    Request JSON Structure:
        {
            "amount": float,     # The amount of the expense
            "description": str   # A description of the expense
        }

    Response JSON Structure (200):
        {
            "record": dict,    # A dictionary with the registered record
            "balance": float   # The new balance after the registered record
        }

    Error Response JSON Structure (400):
        {
            "status": str          # An error status
            "reason": str          # The reason of the error
            "additional_info": {   # Aditional information about the error
                ...
            }
        }
        {
            "status": str          # An error status
            "reason": str          # The reason of the error
        }

    Example Success Response:
        HTTP/1.1 200 OK
        Content-Type: application/json
        {
            "record": {
                "amount": -50.25,
                "description": "Buy new pants"
            },
            "balance": 50.25
        }

    Example Error Response:
        HTTP/1.1 400 Bad Request
        Content-Type: application/json
        {
            "status": "error",
            "reason": "Missing body fields",
            "additional_info": {
                "missing_fields": ["amount", "description"]
            }
        }
    """
    try:
        data = request.get_json()
    except Exception:
        data = {}

    required_fields = ["amount", "description"]
    missing_fields = []

    _assert(data is not None, 400, "Missing request body")

    for field in required_fields:
        if field not in data:
            missing_fields.append(field)

    _assert(not bool(missing_fields), 400, "Missing body fields", {
        "missing_fields": missing_fields })

    amount: int | float = data.get("amount") # type: ignore

    aditional_info = {
        "invalid_field": "amount",
        "reason": f"Must be a number. Got: {type(amount).__name__}"
    }
    _assert(isinstance(amount, int) or isinstance(amount, float),
            400, "Invalid field", aditional_info)

    aditional_info = {
        "invalid_field": "amount",
        "reason": f"Must be a positive number. Got: {amount}"
    }
    _assert(amount >= 0, 400, "Invalid field", aditional_info)

    description: str = data.get("description") # type: ignore

    aditional_info = {
        "invalid_field": "description",
        "reason": f"Must be a string. Got: {type(description).__name__}"
    }
    _assert(isinstance(description, str), 400, "Invalid field", aditional_info)

    aditional_info = {
        "invalid_field": "description",
        "reason": f"Can't be empty"
    }
    _assert(bool(description), 400, "Invalid field", aditional_info)

    rec = controller.register_expense(amount, description)
    balance = controller.get_balance()

    res = {
        "record": rec,
        "balance": balance
    }
    return jsonify(res), 200


@app.route("/history", methods=["GET"])
def get_history() -> tuple[Response,int]:
    """
    Retrieve the history of all records.

    This endpoint returns a list of all records. Each record contains
    information about individual transactions or events.

    Returns:
        tuple[Response, int]: A tuple where the first element is a Flask
        `Response` object containing the JSON payload and the second element is
        the HTTP status code.

    Response JSON Structure (200):
        [
            {
                "amount": float,      # The amount associated with the record
                "description": str,   # A description of the record
                "ts": str             # The timestamp of when the record was
                                      # created
            },
            ...
        ]

    Example Success Response:
        HTTP/1.1 200 OK
        Content-Type: application/json
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
    all_records = controller.get_all_records()
    return jsonify(all_records), 200


@app.after_request
def add_cors_headers(response):
    """
    Add CORS headers to the response.

    This function is called after each request to add Cross-Origin Resource
    Sharing (CORS) headers to the response, allowing cross-origin requests from
    any origin. It enables the client to send requests with the specified
    headers and methods.

    Args: response (Response): The Flask response object to which CORS headers
    will be added.

    Returns: Response: The modified response object with added CORS headers.

    Added Headers:
        - Access-Control-Allow-Origin: Allows requests from any origin (`*`).
        - Access-Control-Allow-Headers: Allows `Content-Type` and
          `Authorization` headers.
        - Access-Control-Allow-Methods: Allows `GET`, `PUT`, `POST`, and
          `DELETE` methods.
    """
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response


@app.before_request
def before_request():
    """
    Initialize the database connection pool before each request.

    This function is called before each request to initialize the connection
    pool, ensuring that database connections are ready to be used by the
    request handlers. It sets up necessary resources required for handling the
    request.

    Returns:
        None
    """
    db.init_pool()


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Release the connection pool after each request.

    This function is called after each request to release the database
    connection pool, ensuring that all connections are properly closed and
    resources are cleaned up. It helps maintain the stability and performance
    of the application by managing the connection lifecycle.

    Args: exception (Exception): The exception that was raised during the
    request, if any.

    Returns:
        None
    """
    if "connection_pool" in g:
        g.connection_pool.closeall()
