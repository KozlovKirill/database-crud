from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    email: str
    username: str
    password: str
    subscription_id: Optional[int] = None

class User(CreateUser):
    id: int

    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    email: Optional[str]
    username: Optional[str]
    password: Optional[str]
    subscription_id: Optional[int]

class UserInDB(User):
    hashed_password: str

# create separate rotue for update subscription
# class UpdateUserSubscription(BaseModel):
#     subscription_id: int
