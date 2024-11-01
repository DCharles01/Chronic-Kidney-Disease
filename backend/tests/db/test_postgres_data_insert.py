import pytest
from api.create_app import create_app
from db.models.models import db, CKDPatientData
from db import create_table



@pytest.fixture()
def dev_app():
    app = create_app(environ='dev')
    with app.app_context():
        # build up
        create_table(app=app, environ='dev')
        patient_data = CKDPatientData(age=56, diabetes='yes', anemia='yes', prediction='yes', is_correct='yes')
        db.session.add(patient_data)
        db.session.commit()
        yield app

        # tear down
        db.session.remove()
        db.drop_all()


def test_ckd_patient_data_exists(dev_app):
    assert CKDPatientData.query.count()==1





