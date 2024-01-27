import pytest
from api.create_app import create_app
from db import create_table
from db.models.models import db, CKDPatientData
import json

@pytest.fixture()
def app():
    app = create_app(environ='dev')
    with app.app_context():
        # build up
        # create_table(app=app, environ='dev')
        # patient_data = CKDPatientData(session_id='123', age=56, diabetes='yes', anemia='yes', prediction='yes', is_correct='yes')
        # db.session.add(patient_data)
        # db.session.commit()
        yield app

        # tear down
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_predict_endpoint(app, client):
    patient_data = CKDPatientData(age=48, blood_pressure=80,
                                  red_blood_cell_count=5.2, white_blood_cell_count=7800,
                                  packed_cell_volume=44, serum_creatinine=1.2, sodium=0,
                                  potassium=0, hemoglobin=15.4, red_blood_cells='normal',
                                  coronary_artery_disease='no', appetite='good', hypertension='yes',
                                  diabetes='yes', anemia='yes', pedal_edema='no')

    prediction_columns = ['age','blood_pressure', 'red_blood_cell_count', 'white_blood_cell_count', 'packed_cell_volume',
                          'serum_creatinine', 'sodium', 'potassium', 'hemoglobin', 'red_blood_cells', 'coronary_artery_disease',
                          'appetite', 'hypertension', 'diabetes', 'anemia', 'pedal_edema']

    patient_data_dict = patient_data.to_dict()
    patient_prediction_data = {k: v for k, v in patient_data_dict.items() if k in prediction_columns}

    rbc_prediction_mapping = {'normal': 1, 'abnormal': 0}
    cad_prediction_mapping = {'yes': 1, 'no': 0}
    appetite_prediction_mapping = {'good': 1, 'poor': 0}
    hypertension_prediction_mapping = {'yes': 1, 'no': 0}
    diabetes_prediction_mapping = {'yes': 1, 'no': 0}
    anemia_prediction_mapping = {'yes': 1, 'no': 0}
    pedal_edema_prediction_mapping = {'yes': 1, 'no': 0}

    # feature engineer columns
    patient_prediction_data['coronary_artery_disease'] = cad_prediction_mapping[patient_prediction_data['coronary_artery_disease']]
    patient_prediction_data['red_blood_cells'] = rbc_prediction_mapping[patient_prediction_data['red_blood_cells']]
    patient_prediction_data['appetite'] = appetite_prediction_mapping[patient_prediction_data['appetite']]
    patient_prediction_data['hypertension'] = hypertension_prediction_mapping[patient_prediction_data['hypertension']]
    patient_prediction_data['diabetes'] = diabetes_prediction_mapping[patient_prediction_data['diabetes']]
    patient_prediction_data['anemia'] = anemia_prediction_mapping[patient_prediction_data['anemia']]
    patient_prediction_data['pedal_edema'] = pedal_edema_prediction_mapping[patient_prediction_data['pedal_edema']]

    patient_data_json = json.dumps(patient_prediction_data)
    # breakpoint()

    # convert to dictionary
    response = client.post("/predict", data=patient_data_json, headers = {'Content-Type': 'application/json'})
    print(response.get_data(as_text=True))
    assert response.status_code == 200

    # assert 'prediction' in response.json()

    assert response.text == 'Patient Has CKD' # model should return CKD for these variables





