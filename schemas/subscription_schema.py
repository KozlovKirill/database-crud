from pydantic import BaseModel, constr
from typing import Optional

class CreateSubscription(BaseModel):
    name: str
    description: Optional[str] = "Empty description"
    price: Optional[float] = 0 #in USD
    period: int #in days
    previlegis: list[constr(max_length=255)] #wtf? should work

class Subscription(CreateSubscription):
    id: int

    class Config:
        orm_mode = True