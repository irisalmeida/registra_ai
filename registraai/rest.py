from flask import Flask, g, jsonify, request, make_response, abort

import controller
import db

app = Flask(__name__)


def _assert(condition, status_code, message):
    if condition: return
    _abort(status_code, message)


def _abort(status_code, message):
    res = {
        "message": message,
        "status_code": status_code
    }
    response = make_response(jsonify(res), status_code)
    abort(response)


@app.route("/balance")
def get_balance():
    balance = controller.get_balance()

    res = {
        "message": f"Saldo atual: R${balance:.2f}",
        "balance": balance,
    }
    return jsonify(res), 200


@app.route("/gain", methods=["POST"])
def post_gain():
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
def get_history():
    all_records = controller.get_all_records()
    return jsonify(all_records)


@app.before_request
def before_request():
    # Initialize the connection pool before each request
    db.init_pool()


@app.teardown_appcontext
def teardown_appcontext(exception):
    # Release the connection pool after each request
    if "connection_pool" in g:
        g.connection_pool.closeall()
