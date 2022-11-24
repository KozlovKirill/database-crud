import typing

from passlib.context import CryptContext
from schemas.user_schema import User

from sqlalchemy.orm import Session

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_hashed_password(password):
    return password_context.hash(password)

def get_user(database, username: str):
    for user in database:
        if user["username"] == username:
            return User(**user)

def get_user_by_id(database, id: int):
    for user in database:
        if user["id"] == id:
            return User(**user)

def authenticate_user(database, username: str, password: str):
    user = get_user(database, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user