from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db.postgres_connector import create_session, database_url, test_database_url, dev_database_url
from db.models.models import db, CKDPatientData
from sqlalchemy import create_engine

def create_app(environ: str ='dev'):
    assert environ in ['prod', 'test', 'dev'], f"{environ} not in {['prod', 'test', 'dev']}"
    app = Flask(__name__)

    if environ == 'prod':
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    elif environ == 'dev':
        app.config['SQLALCHEMY_DATABASE_URI'] = dev_database_url

    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = test_database_url

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app


def create_table(app, environ: str = 'dev'):
    assert environ in ['prod', 'test', 'dev'], f"{environ} not in {['prod', 'test', 'dev']}"
    # breakpoint()
    if environ == 'prod':

        db.create_engine(database_url, engine_opts={})
    elif environ == 'dev':
        db.create_engine(dev_database_url, engine_opts={})

    else:
        db.create_engine(test_database_url, engine_opts={})

    # breakpoint()
    db.init_app(app)
    db.metadata.create_all(db.engine)



