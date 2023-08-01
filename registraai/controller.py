from models import Record


def get_all_records():
    all_records =  Record.get_all()
    return all_records

def get_balance():
    """Returns the total balance after all registered gains and expenses"""
    all_records = get_all_records()  # Chamando a função para obter a lista de registros
    balance = sum([rec['amount'] for rec in all_records])
    return balance

def register_gain(amount:float, description:str) -> dict:
    """Register a money gain. The value is stored as a positive value."""
    rec = Record(amount, description)
    rec.save()
    return rec.to_dict()


def register_expense(amount:float, description:str) -> dict:
    """Register a money expense. The value is stored as a negative value."""
    negative_amount = amount * -1
    rec = Record(negative_amount, description)
    rec.save()
    return rec.to_dict()

