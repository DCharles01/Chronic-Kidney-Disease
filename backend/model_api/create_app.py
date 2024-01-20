from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db.postgres_connector import create_session, database_url, test_database_url, dev_database_url
from model_api.models.models import db, CKDPatientData

def create_app(environ: str ='prod'):
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


def create_table(environ: str = 'prod'):
    assert environ in ['prod', 'test', 'dev'], f"{environ} not in {['prod', 'test', 'dev']}"
    if environ == 'prod':

        db.engine = db.create_engine(database_url)
    elif environ == 'dev':
        db.engine = db.create_engine(dev_database_url)

    else:
        db.engine = db.create_engine(test_database_url)

    db.metadata.create_all(db.engine)

