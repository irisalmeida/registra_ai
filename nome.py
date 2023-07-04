saldo = 0

while True:

    print("Escolha uma dos números abaixo:")
    print("1 - Ganho")
    print("2 - Gasto")
    print("3 - Saldo")
    print("4 - Sair")

    opcaoescolhida = input("Opção escolhida: ")


    if opcaoescolhida == "1":
        valor = float(input("Digite seu ganho: "))
        saldo += valor
        msg = (f"Ganho registrado! Agora você tem R${saldo:.2f}")
    elif opcaoescolhida == "2":
        valor = float(input("Digite seu gasto: "))
        saldo -= valor
        msg = (f"Gasto registrado! Agora você tem R${saldo:.2f}")
    elif opcaoescolhida == "3":
        msg = (f"Saldo atual: R${saldo:.2f}")
    elif opcaoescolhida == "4":
        msg = "Até mais!!!"
        break
    else:
        msg = "Opção inválida!"
    print(msg)
print(msg)
