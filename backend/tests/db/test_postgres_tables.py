import pytest
from model_api.create_app import create_app, create_table
from model_api.models.models import db


@pytest.fixture()
def dev_app():
    app = create_app(environ='dev')
    with app.app_context():
        # build up
        create_table(app=app, environ='dev')
        yield app

        # tear down
        db.drop_all()

@pytest.fixture()
def prod_app():
    app = create_app(environ='prod')
    with app.app_context():
        # build up
        create_table(app=app, environ='prod')
        yield app

        # tear down
        db.drop_all()

@pytest.fixture()
def test_app():
    app = create_app(environ='test')
    with app.app_context():
        # build up
        create_table(app=app, environ='test')
        yield app

        # tear down
        db.drop_all()


def test_table_exists_in_dev_db(dev_app):
    inspector = db.inspect(db.engine)

    table_names = inspector.get_table_names()

    assert 'patient_data' in table_names

def test_table_exists_in_prod_db(prod_app):
    inspector = db.inspect(db.engine)

    table_names = inspector.get_table_names()

    assert 'patient_data' in table_names

def test_table_exists_in_test_db(test_app):
    inspector = db.inspect(db.engine)

    table_names = inspector.get_table_names()

    assert 'patient_data' in table_names


