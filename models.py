from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    subscription_id = Column(Integer, ForeignKey("subscription.id"), nullable=True)

    def toDict(self):
        user_dict = {"id": self.id,
                     "email": self.email,
                     "username": self.username,
                     "password": self.password,
                     "subscription_id": self.subscription_id}
        return user_dict

class TransactionModel(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    subscription_id = Column(Integer, ForeignKey("subscription.id"))
    date = Column(DateTime)

class SubscriptionModel(Base):
    __tablename__ = "subscription"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True) #in USD
    period = Column(Integer) #in days
    previlegis = Column(ARRAY(String(255)))
