from datetime import datetime
from typing import Optional


class Record():
    def __init__(self, amount:float, description:str, ts:Optional[datetime]=None) -> None:
        self.amount = amount
        self.description = description
        self.ts = datetime.now() if ts is None else ts

    def to_dict(self) -> dict:
        rec = vars(self).copy()
        return rec
