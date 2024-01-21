import pytest
from model_api.create_app import create_app, create_table
from model_api.models.models import db, CKDPatientData


@pytest.fixture()
def dev_app():
    app = create_app(environ='dev')
    with app.app_context():
        # build up
        create_table(app=app, environ='dev')
        patient_data = CKDPatientData(session_id='123', age=56, diabetes='yes', anemia='yes', prediction='yes', is_correct='yes')
        db.session.add(patient_data)
        db.session.commit()
        yield app

        # tear down
        db.session.remove()
        db.drop_all()


def test_ckd_patient_data_exists(dev_app):
    assert CKDPatientData.query.count()==1

def test_ckd_patient_data_has_session_id(dev_app):
    assert CKDPatientData.query.first().session_id == '123'




