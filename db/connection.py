from configparser import ConfigParser
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = ConfigParser()
config.read('./db/db_config.ini')
database_url = config.get('auth', 'database_url')


def pg_db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        engine = create_engine(database_url)
        session = sessionmaker(bind=engine)()
        try:
            return func(session=session, *args, **kwargs)
        finally:
            session.close()
    return wrapper
