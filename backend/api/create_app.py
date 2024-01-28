from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from db.postgres_connector import database_url, test_database_url, dev_database_url
from db.models.models import db
import pickle
from sqlalchemy import create_engine

# load ML model
model = pickle.load(open('api/ml/decisiontreeV1_0801.pkl', 'rb'))

# TODO: make function modular so that user can pass in their login details as well as which environment they need to use
def create_app(environ: str):
    assert environ in ['prod', 'test', 'dev'], f"{environ} not in {['prod', 'test', 'dev']}"
    app = Flask(__name__)

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



        user_inputs = [data['age'], data['blood_pressure'], data['red_blood_cell_count'], data['white_blood_cell_count'],
                data['packed_cell_volume'], data['serum_creatinine'], data['sodium'], data['potassium'], data['hemoglobin'],
                data['red_blood_cells'], data['coronary_artery_disease'], data['appetite'], data['hypertension'], data['diabetes'],
                data['anemia'], data['pedal_edema']]

        prediction = model.predict([user_inputs])[0]
        prediction_mapping = {0: 'Patient Has CKD', 1: 'Patient Does Not Have CKD'}
        return prediction_mapping[prediction]

    return app



