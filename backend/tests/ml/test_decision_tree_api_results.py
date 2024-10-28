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

    
    prediction_columns = ['age', 'bloodPressure', 'redBloodCellCount', 'whiteBloodCellCount',
                        'packedCellVolume', 'serumCreatinine', 'sodium', 'potassium', 'hemoglobin',
                        'redBloodCells', 'coronaryArteryDisease', 'appetite', 'hypertension', 
                        'diabetes', 'anemia', 'pedalEdema']

    
    attribute_mapping = {
        'age': 'age',
        'blood_pressure': 'bloodPressure',
        'red_blood_cell_count': 'redBloodCellCount',
        'white_blood_cell_count': 'whiteBloodCellCount',
        'packed_cell_volume': 'packedCellVolume',
        'serum_creatinine': 'serumCreatinine',
        'sodium': 'sodium',
        'potassium': 'potassium',
        'hemoglobin': 'hemoglobin',
        'red_blood_cells': 'redBloodCells',
        'coronary_artery_disease': 'coronaryArteryDisease',
        'appetite': 'appetite',
        'hypertension': 'hypertension',
        'diabetes': 'diabetes',
        'anemia': 'anemia',
        'pedal_edema': 'pedalEdema'
    }

    
    patient_data_dict = patient_data.to_dict()

    
    patient_prediction_data = {attribute_mapping[k]: v for k, v in patient_data_dict.items() if attribute_mapping.get(k) in prediction_columns}


    patient_data_json = json.dumps(patient_prediction_data)
    # breakpoint()

    # convert to dictionary
    response = client.post("/predict", data=patient_data_json, headers = {'Content-Type': 'application/json'})
    print(response.get_data(as_text=True))
    assert response.status_code == 200

    # assert 'prediction' in response.json()

    assert response.text == 'Patient Has CKD' # model should return CKD for these variables





