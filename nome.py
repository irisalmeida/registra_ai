balance = 0

def register_gain(amount):
    global balance
    balance += amount
    return f"Ganho registrado! Agora você tem R${balance:.2f}"

def register_expense(amount):
    global balance
    balance -= amount
    return f"Gasto registrado! Agora você tem R${balance:.2f}"

def get_balance():
    global balance
    return f"Saldo atual: R${balance:.2f}"

while True:
    print("Escolha uma das opções abaixo:")
    print("1 - Ganho")
    print("2 - Gasto")
    print("3 - Saldo")
    print("4 - Sair")

    choice = input("Opção escolhida: ")

    if choice == "1":
        value = float(input("Digite seu ganho: "))
        output = register_gain(value)
    elif choice == "2":
        value = float(input("Digite seu gasto: "))
        output = register_expense(value)
    elif choice == "3":
        output = get_balance()
    elif choice == "4":
        output = "Até mais!!!"
        break
    else:
        output = "Opção inválida!"

    print(output)

print(output)
