# from db.postgres_connector import *

from db.postgres_connector import create_session, database_url, dev_database_url, test_database_url
from sqlalchemy.sql import text


def test_prod_connection():
    # breakpoint()
    session = create_session(database_url)  # create connection

    result = session.execute(text('select 1'))  # basic query to check connection

    assert result.scalar() == 1, "Connection failed"

    print('Connection to the database successful!')

def test_test_connection():
    # breakpoint()
    session = create_session(test_database_url)  # create connection

    result = session.execute(text('select 1'))  # basic query to check connection

    assert result.scalar() == 1, "Connection failed"

    print('Connection to the database successful!')

def test_dev_connection():
    # breakpoint()
    session = create_session(dev_database_url)  # create connection

    result = session.execute(text('select 1'))  # basic query to check connection

    assert result.scalar() == 1, "Connection failed"

    print('Connection to the database successful!')
