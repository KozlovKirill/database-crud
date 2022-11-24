from models import UserModel

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import load_dotenv, Path

from utils.config_loader import get_database_url

load_dotenv(Path('..') / '.env')
engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database():
    session = SessionLocal()
    database = [user.toDict() for user in session.query(UserModel).all()]
    session.close()
    return database
