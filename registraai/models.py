from datetime import datetime


class Record():
    def __init__(self, amount:float, description:str) -> None:
        self.amount = amount
        self.description = description
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        rec = vars(self).copy()
        return rec
