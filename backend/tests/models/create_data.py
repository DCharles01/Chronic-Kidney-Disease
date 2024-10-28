from db.models.models import CKDPatientData
from db.postgres_connector import create_session, database_url, dev_database_url, test_database_url
import pytest


@pytest.fixture()
def insert_data():
    patient_data = CKDPatientData(age=25, hypertension='yes', diabetes='yes', pedal_edema='yes', prediction='CKD')

    yield patient_data


