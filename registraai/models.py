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
        create_record_query = "registraai/sql/create_table_records.sql"
        query = load_query(create_record_query)

        query = query.replace("@MyCounter", str(self.amount))
        query = query.replace("@MyDescription", self.description)
        query = query.replace("@MyTimestamp", str(self.ts))

       
        execute_query(query)


        try:
            execute_query(query)
            return True 
        except Exception as e:
            return False


    def get_all():
        
       
        query = load_query("caminho/do/arquivo/select_all_records.sql")  # 
        result = execute_query(query)

        all_records = []
        for row in result:
            amount, description, ts = row
            record = Record(amount, description, ts)
            all_records.append(record.to_dict())

        return all_records