from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing import Any

from datetime import datetime, timedelta

from schemas.user_schema import CreateUser, User, UpdateUser
from schemas.transaction_schema import CreateTransaction, Transaction
from schemas.subscription_schema import CreateSubscription, Subscription
from schemas.token_schema import Token

from models import Base, UserModel, TransactionModel, SubscriptionModel
from utils.password_encryption import get_hashed_password, authenticate_user
from utils.jwt_handler import create_access_token, get_current_user, check_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, \
    credentials_exception
from utils.config_loader import get_database_url
from utils.database_loader import get_database

engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)
token_router = APIRouter()


class UserRouter(SQLAlchemyCRUDRouter):
    def _get_one(self, *args: Any, **kwargs: Any):
        def route(
                item_id: self._pk_type,
                db: Session = Depends(self.db_func),
                current_user: User = Depends(get_current_user)
        ):
            if current_user.id == item_id:
                model: Model = db.query(self.db_model).get(item_id)

                if model:
                    return model
                else:
                    raise NOT_FOUND from None
            else:
                raise credentials_exception

        return route

    def _get_all(self, *args: Any, **kwargs: Any):
        def route(
                db: Session = Depends(self.db_func),
                pagination=self.pagination,
                is_valid_token: bool = Depends(check_access_token)
        ):
            if is_valid_token:
                skip, limit = pagination.get("skip"), pagination.get("limit")

                db_models = (
                    db.query(self.db_model)
                    .order_by(getattr(self.db_model, self._pk))
                    .limit(limit)
                    .offset(skip)
                    .all()
                )
                return db_models
            else:
                raise credentials_exception

        return route

    def _create(self, *args: Any, **kwargs: Any):
        def route(
                model: self.create_schema,
                db: Session = Depends(self.db_func),
        ):
            try:
                model = model.dict()
                model["password"] = get_hashed_password(model["password"])
                db_model: Model = self.db_model(**model)
                db.add(db_model)
                db.commit()
                db.refresh(db_model)
                return db_model
            except IntegrityError:
                db.rollback()
                raise HTTPException(422, "Key already exists") from None

        return route

    def _update(self, *args: Any, **kwargs: Any):
        def route(
                item_id: self._pk_type,
                model: self.update_schema,
                db: Session = Depends(self.db_func),
                current_user: User = Depends(get_current_user)
        ):
            if current_user.id == item_id:
                try:
                    model = model.dict()
                    model["password"] = get_hashed_password(model["password"])
                    db_model: Model = db.query(self.db_model).get(item_id)
                    print(db_model)

                    for key, value in model.items():
                        if hasattr(db_model, key):
                            setattr(db_model, key, value)

                    db.commit()
                    db.refresh(db_model)

                    return db_model
                except IntegrityError as e:
                    db.rollback()
                    self._raise(e)
            else:
                raise credentials_exception

        return route

    def _delete_one(self, *args: Any, **kwargs: Any):
        def route(item_id: self._pk_type,
                  db: Session = Depends(self.db_func),
                  current_user: User = Depends(get_current_user)
                  ):
            if current_user.id == item_id:
                db_model: Model = db.query(self.db_model).get(item_id)
                db.delete(db_model)
                db.commit()

                return db_model
            else:
                raise credentials_exception

        return route

    def _delete_all(self, *args: Any, **kwargs: Any):
        def route(db: Session = Depends(self.db_func),
                  is_valid_token: bool = Depends(check_access_token)):
            if is_valid_token:
                db.query(self.db_model).delete()
                db.commit()

                return self._get_all()(db=db, pagination={"skip": 0, "limit": None})
            else:
                raise credentials_exception

        return route


def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


user_router = UserRouter(
    schema=User,
    create_schema=CreateUser,
    update_schema=UpdateUser,
    db_model=UserModel,
    db=get_session,
    prefix="/user",
)

transaction_router = SQLAlchemyCRUDRouter(
    schema=Transaction,
    # dependencies=[Depends(token_authorize)],
    create_schema=CreateTransaction,

    # routes (only read and create)
    get_all_route=False,
    update_route=False,
    delete_one_route=False,
    delete_all_route=False,

    db_model=TransactionModel,
    db=get_session,
    prefix="/transaction",
)

subscription_router = SQLAlchemyCRUDRouter(
    schema=Subscription,
    create_schema=CreateSubscription,
    db_model=SubscriptionModel,
    db=get_session,
    prefix="/subscription",
)


@token_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(get_database(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
