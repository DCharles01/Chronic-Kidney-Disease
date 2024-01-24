from .settings import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
dev_database_url: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DEV_DB_NAME}"
test_database_url: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"


def create_session(db_url: str):
    # breakpoint()
    engine = create_engine(db_url)  # create database engine

    Session = sessionmaker(bind=engine)  # create session factory

    session = Session()

    return session

