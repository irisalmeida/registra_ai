from datetime import datetime
from typing import Optional
from db import load_query, execute_query


class Record():
    def __init__(self, amount:float, description:str, ts:Optional[datetime]=None) -> None:
        self.amount = amount
        self.description = description
        self.ts = datetime.now() if ts is None else ts

    def to_dict(self) -> dict:
        rec = vars(self).copy()
        return rec

    def save(self):
        create_record_query = "create_table_records.sql"
        query = load_query(create_record_query)

        values = (self.amount, self.description, self.ts)

        try:
            execute_query(query)
            return True
        except Exception as e:
            print(e)
            return False
            
    @staticmethod
    def get_all():
        query = load_query("select_all_records.sql") 
        result = execute_query(query)


        all_records = []
        for row in result:
            amount, description, ts = row
            record = Record(amount, description, ts)
            all_records.append(record.to_dict())

        return all_records