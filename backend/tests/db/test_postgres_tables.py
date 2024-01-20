import pytest
from model_api.create_app import create_app, create_table
from models_api.models.models import db

@pytest.fixture()
def app():
    app = create_app('dev')
    with app.app_context():
        # build up
        create_table()
        yield app

        # tear down
        db.drop_all()


def test_table_exists_in_dev_env(app):
    inspector = db.inspect(db.engine)

    table_names = inspector.get_table_names()

    assert 'patient_data' in table_names