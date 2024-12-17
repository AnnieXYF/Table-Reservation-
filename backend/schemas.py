from pydantic import BaseModel
from datetime import time,date

class Reservation (BaseModel):
    id: int
    table_name: str
    book_time: time
    book_date: date

    class Config:
        orm_mode = True
