from pydantic import BaseModel
from datetime import datetime

class CreateTransaction(BaseModel):
    user_id: int
    subscription_id: int
    date: datetime

class Transaction(CreateTransaction):
    id: int

    class Config:
        orm_mode = True