from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from db.postgres_connector import database_url, test_database_url, dev_database_url
from db.models.models import db
import pickle
from flask_cors import CORS
from sqlalchemy import create_engine

# load ML model
model = pickle.load(open('api/ml/decisiontreeV1_0801.pkl', 'rb'))

# TODO: make function modular so that user can pass in their login details as well as which environment they need to use
def create_app(environ: str):
    assert environ in ['prod', 'test', 'dev'], f"{environ} not in {['prod', 'test', 'dev']}"
    app = Flask(__name__)

    CORS(app)

    if environ == 'prod':
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    elif environ == 'test':
        app.config['SQLALCHEMY_DATABASE_URI'] = test_database_url
    elif environ == 'dev':
        app.config['SQLALCHEMY_DATABASE_URI'] = dev_database_url

    else:
        print(f'Invalid environment: {environ}')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    db.init_app(app)

    @app.route('/')
    def home():
        return 'Endpoint to predict CKD'

    @app.route('/predict', methods=['POST'])
    def predict():
        data = request.get_json()

        rbc_prediction_mapping = {'normal': 1, 'abnormal': 0}
        cad_prediction_mapping = {'yes': 1, 'no': 0}
        appetite_prediction_mapping = {'good': 1, 'poor': 0}
        hypertension_prediction_mapping = {'yes': 1, 'no': 0}
        diabetes_prediction_mapping = {'yes': 1, 'no': 0}
        anemia_prediction_mapping = {'yes': 1, 'no': 0}
        pedal_edema_prediction_mapping = {'yes': 1, 'no': 0}
        
        # print(data['coronaryArteryDisease'])
        # print(cad_prediction_mapping)
        # # feature engineer columns
        data['coronaryArteryDisease'] = cad_prediction_mapping[
            data['coronaryArteryDisease']]
        data['redBloodCells'] = rbc_prediction_mapping[data['redBloodCells']]
        data['appetite'] = appetite_prediction_mapping[data['appetite']]
        data['hypertension'] = hypertension_prediction_mapping[data['hypertension']]
        data['diabetes'] = diabetes_prediction_mapping[data['diabetes']]
        data['anemia'] = anemia_prediction_mapping[data['anemia']]
        data['pedalEdema'] = pedal_edema_prediction_mapping[data['pedalEdema']]


        # breakpoint()
        user_inputs = [data['age'], data['bloodPressure'], data['redBloodCellCount'], data['whiteBloodCellCount'],
                data['packedCellVolume'], data['serumCreatinine'], data['sodium'], data['potassium'], data['hemoglobin'],
                data['redBloodCells'], data['coronaryArteryDisease'], data['appetite'], data['hypertension'], data['diabetes'],
                data['anemia'], data['pedalEdema']]



        prediction = model.predict([user_inputs])[0]
        prediction_mapping = {0: 'Patient Has CKD', 1: 'Patient Does Not Have CKD'}
        return prediction_mapping[prediction]

    return app



