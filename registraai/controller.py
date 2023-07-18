from models import Record

records = []


def get_balance():
    """Returns the total balance after all registered gains and expenses"""
    balance = sum([rec.amount for rec in records])
    return balance


def register_gain(amount:float, description:str) -> dict:
    """Register a money gain. The value is stored as a positive value."""
    rec = Record(amount, description)
    records.append(rec)
    return rec.to_dict()


def register_expense(amount:float, description:str) -> dict:
    """Register a money expense. The value is stored as a negative value."""
    negative_amount = amount * -1
    rec = Record(negative_amount, description)
    records.append(rec)
    return rec.to_dict()
