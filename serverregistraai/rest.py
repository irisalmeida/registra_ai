from flask import Flask, jsonify, request, make_response, abort, send_file

app = Flask(__name__)


balance = 10

@app.route("/balance")
def get_balance():
    global balance
    return f"Saldo atual: R${balance:.2f}"


@app.route("/gain", methods=["POST"])
def register_gain():
    global balance
    data = request.get_json()
    amount = data.get("amount")
    balance += amount
    return f"Ganho registrado! Agora você tem R${balance:.2f}"


@app.route("/expense", methods=["POST"])
def register_expense():
    global balance
    data = request.get_json()
    amount = data.get("amount")
    balance -= amount
    return f"Gasto registrado! Agora você tem R${balance:.2f}"
