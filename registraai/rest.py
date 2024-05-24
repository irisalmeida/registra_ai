from flask import Flask, g, jsonify, request, make_response, abort, Response

import controller
import db

app = Flask(__name__)


def _assert(condition:bool, status_code:int, message:str) -> None:
    """
    Check if condition is true. If it is not, abort request and make an Error
    response with the provided status code and message.

    Args:
        condition: the condition that if is false will cause the request to
          abort and receive a error response.
        status_code: the response's status code if the condition is false.
        message: the response's message if the condition is false.

    Returns:
        This function have no return, but the error response will have the
        status code defined in the param and a json with 'status_code' and
        'message' fields. Example:

        {
            "message": "Error during operation.",
            "status_code": "400"
        }
    """
    if condition: return
    _abort(status_code, message)


def _abort(status_code, message):
    """
    Abort request and make an Error response with the provided status code and
    message.

    Args:
        status_code: the response's status code.
        message: the response's message.

    Returns:
        This function have no return, but the error response will have the
        status code defined in the param and a json with 'status_code' and
        'message' fields. Example:

        {
            "message": "Error during operation.",
            "status_code": "400"
        }
    """
    res = {
        "message": message,
        "status_code": status_code
    }
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
            "balance": float,   # The current balance amount
            "message": str,     # A message containing the current balance
        }

    Example Response:
        HTTP/1.1 200 OK
        Content-Type: application/json
        {
            "balance": 100.50,
            "message": "Saldo atual: R$100.50"
        }

    """
    balance = controller.get_balance()

    res = {
        "message": f"Saldo atual: R${balance:.2f}",
        "balance": balance,
    }
    return jsonify(res), 200


@app.route("/gain", methods=["POST"])
def post_gain() -> tuple[Response,int]:
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
            "message": str,            # A message of success with the new
                                       # balance
            "registered_gain": dict,   # A dictionary with the fields "amount"
                                       # and "description" from the gain record
            "balance": float           # The new balance after the registered
                                       # gain
        }

    Error Response JSON Structure (400):
        {
            "message": str,       # A message with the error reason
            "status_code": int    # The status code of the response
        }

    Example Success Response:
        HTTP/1.1 200 OK
        Content-Type: application/json
        {
            "message": "Ganho registrado! Agora você tem R$100.50"
            "registered_gain": {
                "amount": 100.50,
                "description": "Found in my old pants"
            },
            "balance": 100.50
        }

    Example Error Response:
        HTTP/1.1 400 Bad Request
        Content-Type: application/json
        {
            "status_code": 400,
            "message": "Body sem campo 'amount'"
        }
    """
    data = request.get_json()

    _assert(data is not None, 400, "Faltou o body da requisição")
    _assert("amount" in data, 400, "Body sem campo 'amount'")
    _assert("description" in data, 400, "Body sem campo 'description'")

    amount = data.get("amount")
    _assert(amount >= 0, 400, f"'amount' inválido: deve ser um valor positivo")
    description = data.get("description")

    rec = controller.register_gain(amount, description)
    balance = controller.get_balance()

    res = {
        "message": f"Ganho registrado! Agora você tem R${balance}",
        "registered_gain": rec,
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
            "amount": float,     # The amount of the gain
            "description": str   # A description of the gain
        }

    Response JSON Structure (200):
        {
            "message": str,               # A message of success with the new
                                          # balance
            "registered_expense": dict,   # A dictionary with the fields
                                          # "amount" and "description" from the
                                          # expense record
            "balance": float              # The new balance after the registered
                                          # expense
        }

    Error Response JSON Structure (400):
        {
            "message": str,       # A message with the error reason
            "status_code": int    # The status code of the response
        }

    Example Success Response:
        HTTP/1.1 200 OK
        Content-Type: application/json
        {
            "message": "Gasto registrado! Agora você tem R$50.50"
            "registered_expense": {
                "amount": 50.00
                "description": "Buy new pants"
            },
            "balance": 50.50
        }

    Example Error Response:
        HTTP/1.1 400 Bad Request
        Content-Type: application/json
        {
            "status_code": 400,
            "message": "Body sem campo 'amount'"
        }
    """
    data = request.get_json()

    _assert(data is not None, 400, "Faltou o body da requisição")
    _assert("amount" in data, 400, "Body sem campo 'amount'")
    _assert("description" in data, 400, "Body sem campo 'description'")

    amount = data.get("amount")
    _assert(amount >= 0, 400, f"'amount' inválido: deve ser um valor positivo")
    description = data.get("description")

    rec = controller.register_expense(amount, description)
    balance = controller.get_balance()

    res = {
        "message": f"Gasto registrado! Agora você tem R${balance}",
        "registered_expense": rec,
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

    This function is called before each request to initialize the connection pool,
    ensuring that database connections are ready to be used by the request handlers.
    It sets up necessary resources required for handling the request.

    Returns:
        None
    """
    db.init_pool()


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Release the connection pool after each request.

    This function is called after each request to release the database connection pool,
    ensuring that all connections are properly closed and resources are cleaned up.
    It helps maintain the stability and performance of the application by managing
    the connection lifecycle.

    Args:
        exception (Exception): The exception that was raised during the request, if any.

    Returns:
        None
    """
    if "connection_pool" in g:
        g.connection_pool.closeall()
