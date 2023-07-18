from flask import Flask, jsonify, request, make_response, abort, send_file

app = Flask(__name__)

balance = 0


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
    global balance
    return f"Saldo atual: R${balance:.2f}"


@app.route("/gain", methods=["POST"])
def register_gain():
    global balance

    data = request.get_json()

    _assert(data is not None, 400, "Faltou o body da requisição")
    _assert("amount" in data, 400, "Body sem amount")

    amount = data.get("amount")
    _assert(amount >= 0, 400, f"'amount' inválido: deve ser um valor positivo")

    balance += amount

    res = {
        "message": f"Ganho registrado! Agora você tem R${balance}",
        "registered_gain": amount,
        "balance": balance
    }
    return jsonify(res), 200


@app.route("/expense", methods=["POST"])
def register_expense():
    global balance

    data = request.get_json()

    _assert(data is not None, 400, "Faltou o body da requisição")
    _assert("amount" in data, 400, "Body sem amount")
    
    amount = data.get("amount")
    _assert(amount >= 0, 400, f"'amount' inválido: deve ser um valor positivo")
    
    balance -= amount
    
    res = {
        "message": f"Gasto registrado! Agora você tem R${balance}",
        "registered_expense": amount,
        "balance": balance
    }
    return jsonify(res), 200
  