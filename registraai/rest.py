import json
import os
from typing import Any

from flask import (
    Flask,
    g,
    jsonify,
    request,
    make_response,
    abort,
    Response,
    redirect,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)
from flask_cors import CORS
from oauthlib.oauth2 import WebApplicationClient

import requests
import controller
import db
from models import User

FRONTEND_URL = os.environ.get("FRONTEND_URL", "")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")

CORS(app, resources={r"/*": {"origins": FRONTEND_URL}}, supports_credentials=True)

login_manager = LoginManager()
login_manager.init_app(app)

client = WebApplicationClient(GOOGLE_CLIENT_ID)


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


@login_manager.user_loader
def load_user(user_id: str) -> UserMixin | None:
    """
    Load a user by their user ID.

    This function is used by Flask-Login to load a user from the user ID stored
    in the session. It expects a user ID as a string and returns a `UserMixin`
    object if the user is found, otherwise `None`.

    Args:
        user_id (str): The ID of the user to be loaded.

    Returns:
        UserMixin | None: A `UserMixin` object if the user is found,
        otherwise `None`.

    Example:
        >>> load_user("123")
        <UserMixin object at 0x...>

        >>> load_user("nonexistent_id")
        None
    """
    return controller.get_user(user_id)


def get_google_provider_cfg() -> dict[str, Any]:
    """
    Get the Google OAuth2 provider configuration.

    This function makes a GET request to the Google Discovery URL to fetch the
    OAuth2 provider configuration, including details like the authorization
    endpoint, token endpoint, etc.

    Returns:
        Dict[str, Any]: A dictionary containing the Google OAuth2 provider
        configuration.

    Example:
        >>> get_google_provider_cfg()
        {
            "issuer": "https://accounts.google.com",
            "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_endpoint": "https://oauth2.googleapis.com/token",
            ...
        }
    """
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    """
    Initiate the Google OAuth2 login process.

    This endpoint retrieves the Google OAuth2 provider configuration, prepares
    the request URI for OAuth2 authorization, and redirects the user to the
    Google authorization page for login.

    Returns:
        redirect: Redirects the user to the Google authorization page for
        login.
    """
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=f"{request.base_url}/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    """
    Callback endpoint for handling the OAuth2 authorization code and logging in
    the user.

    This endpoint receives the authorization code from Google, exchanges it for
    an access token, retrieves user information, creates or retrieves the user
    from the database, logs the user in, and redirects them to the frontend
    URL.

    Returns:
        redirect: Redirects the user to the frontend URL after successful
        login.
        jsonify: Returns a JSON response with an error message if the user
        email is not available or verified.
    """
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()

    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET), # type: ignore
    )
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return jsonify(
            {
                "error": "User email not available or not verified by Google"
            }
        ), 400

    try:
        user = controller.get_or_create_user(unique_id, users_name, users_email, picture)
    except Exception as e:
        return jsonify(
            {
                "error": str(e)
            }
        ), 500

    login_user(user)
    callback_url = f"{FRONTEND_URL}/#login-callback"
    response = make_response(redirect(callback_url))
    response.set_cookie("logged", "true")
    return response


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Logout the currently authenticated user.

    This endpoint logs out the currently authenticated user and returns a JSON
    response confirming the logout.

    Returns:
        jsonify: A JSON response indicating successful logout.

    Example:
        >>> logout()
        {"status": "ok", "message": "Logout success"}
    """
    logout_user()
    response = make_response({"status": "ok", "message": "Logout success"}, 200)
    response.set_cookie("logged", "false")
    return response


@app.route("/user_data", methods=["GET"])
@login_required
def get_user():
    """
    Get user data for the currently authenticated user.

    This endpoint retrieves user data for the currently authenticated user and returns it as a JSON response.

    Returns:
        tuple[Response, int]: A tuple where the first element is a Flask `Response` object containing the JSON payload
        and the second element is the HTTP status code.

    Request JSON Structure:
        N/A (GET request)

    Response JSON Structure (200):
        {
            "id": str,          # The user's ID
            "username": str,    # The user's username
            "email": str,       # The user's email address
            "profile_pic": str  # The URL of the user's profile picture
        }

    Error Response JSON Structure (401):
        {
            "error": str        # Error message indicating unauthorized access
        }

    Error Response JSON Structure (400):
        {
            "error": str        # Error message indicating user not found
        }

    Example Success Response:
        HTTP/1.1 200 OK
        Content-Type: application/json
        {
            "id": "123",
            "username": "John Doe",
            "email": "john@example.com",
            "profile_pic": "http://example.com/john.jpg"
        }

    Example Unauthorized Access Response:
        HTTP/1.1 401 Unauthorized
        Content-Type: application/json
        {
            "status": "error",
            "reason": "Unauthorized access"
        }

    Example User Not Found Response:
        HTTP/1.1 400 Bad Request
        Content-Type: application/json
        {
            "status": "error",
            "reason": "User not found"
        }
    """
    user_id = current_user.id # type: ignore
    _assert(bool(current_user.is_authenticated and # type: ignore
            str(current_user.id == user_id)), # type: ignore
            401, "Unathorized access")

    user = User.get(user_id)
    _assert(user is not None, 400, "User not found")

    return jsonify(user.to_dict()), 200 # type: ignore


@app.route("/balance")
@login_required
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
    status_code = 200
    user_id = current_user.id # type: ignore

    try:
        balance = controller.get_balance(user_id)

        res = {
            "balance": balance
        }
    except Exception as e:
        res = {
            "status": "error",
            "reason": f"Erro during gain registration for user {user_id}",
            "adicional_info": {
                "exception": str(e),
                }
        }
        status_code = 500

    return jsonify(res), status_code


@app.route("/gain", methods=["POST"])
@login_required
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

    status_code = 200
    user_id = current_user.id # type: ignore

    try:
        rec = controller.register_gain(user_id, amount, description)
        balance = controller.get_balance(user_id)

        res = {
            "record": rec.to_dict(),
            "balance": balance
        }
    except Exception as e:
        res = {
            "status": "error",
            "reason": f"Erro during gain registration for user {user_id}",
            "adicional_info": {
                "exception": str(e),
                }
        }
        status_code = 500

    return jsonify(res), status_code


@app.route("/expense", methods=["POST"])
@login_required
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

    status_code = 200
    user_id = current_user.id # type: ignore
    try:
        rec = controller.register_expense(user_id, amount, description)
        balance = controller.get_balance(user_id)

        res = {
            "record": rec.to_dict(),
            "balance": balance
        }
    except Exception as e:
        res = {
            "status": "error",
            "reason": f"Erro during expense registration for user {user_id}",
            "adicional_info": {
                "exception": str(e),
                }
        }
        status_code = 500

    return jsonify(res), status_code


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
    status_code = 200
    user_id = current_user.id # type: ignore

    try:
        user = controller.get_user(user_id)
        records = user.get_records()
        history = [rec.to_dict() for rec in records]
        balance = sum([rec.amount for rec in records])

        res = {
            "history": history,
            "balance": balance,
        }
    except Exception as e:
        res = {
            "status": "error",
            "reason": f"Erro during get history for user {user_id}",
            "adicional_info": {
                "exception": str(e),
                }
        }
        status_code = 500

    return jsonify(res), status_code


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
