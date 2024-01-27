from .postgres_connector import *
from db.models.models import db

def create_table(app, environ: str):
    assert environ in ['prod', 'test', 'dev'], f"{environ} not in {['prod', 'test', 'dev']}"
    # breakpoint()
    if environ == 'prod':

        db.create_engine(database_url)
    elif environ == 'dev':
        db.create_engine(dev_database_url)

    else:
        db.create_engine(test_database_url)

    # breakpoint()
    db.init_app(app)
    db.metadata.create_all(db.engine)