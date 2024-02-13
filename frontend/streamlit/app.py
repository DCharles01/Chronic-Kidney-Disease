import streamlit as st
import secrets # generate random session id for each user session
import sqlite3
import datetime
import os
import logging
import requests
import json
# from utils.model_prediction import predict





log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format, datefmt='%m/%d/%Y %I:%M:%S %p', handlers=[
    logging.FileHandler(f'logs/logs_{datetime.datetime.now().strftime("%Y%m%d")}.log'),
    logging.StreamHandler()], encoding='utf-8', level=logging.INFO)
    



# MVP: add patient data one by one to get prediction
# Post-MVP: allow user to upload csv or excel with multiple patient data and return file with prediction

# generate random session id
session_id = secrets.token_hex(16) # streamlit refreshes and this will change everytime an input is changed
session_start_ts_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # timestamp
session_start_ts = datetime.datetime.now()
session_dt = datetime.date.today().strftime("%Y-%m-%d") # today's date


logging.info('Creating Database and Tables')
# run python script to create sqlite db and crete table
# if os.path.isfile('ml_streamlit_application_data.db'):
    # connect to database
conn = sqlite3.connect('ml_streamlit_application_data.db')
# else:
#     os.system('python setup_sqlite_db_schema.py')
logging.info('Done. Database and Table created.')



# create cursor
cursor = conn.cursor()

# insert data query
insert_data_query = '''
INSERT INTO ckd_patient_data (session_id, session_ts, sesstion_dt, session_duration, prediction_ts, prediction_dt, age, blood_pressure, red_blood_cell_count, white_blood_cell_count, packed_cell_volume, serum_creatinine, sodium, potassium, hemoglobin, red_blood_cells, coronary_artery_disease, appetite, hypertension, diabetes, anemia, pedal_edema, prediction, prediction_duration, is_correct)

VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
'''

# initialize variables to access outside of following if statement
prediction_start_ts_str = None
prediction_start_ts = None
prediction_end = None
prediction = None
prediction_dt = None
prediction_duration = None

# Define the streamlit app
def app():

    # define global variable to make accessible outside of if statement
    global prediction_start_ts_str
    global prediction_start_ts
    global prediction_end
    global prediction
    global prediction_dt
    global prediction_duration
    global prediction_start_ts_str
    global prediction_start_ts


    # Set the title of the app
    st.title(f'Patient CKD Prediction\nSession ID: {session_id}')
    # Ask the user for the inputs
    age = st.number_input('age', min_value=0.0)
    blood_pressure = st.number_input('Blood Pressure (mm/HG)', min_value=0.0, help='Please only enter HG. Data used to create the model uses HG instead of MM - https://archive.ics.uci.edu/dataset/336/chronic+kidney+disease')
    red_blood_cell_count = st.number_input('Red Blood Cell Count', min_value=0.0)
    white_blood_cell_count = st.number_input('White Blood Cell Count', min_value=0.0)
    packed_cell_volume = st.number_input('Packed Cell Volume', min_value=0.0)
    serum_creatinine = st.number_input('Serum Creatinine (mgs/dl)', min_value=0.0)
    sodium = st.number_input('Sodium (mEq/L)', min_value=0.0)
    potassium = st.number_input('Potassium (mEq/L)', min_value=0.0)
    hemoglobin = st.number_input('Hemoglobin (gms)', min_value=0.0)
    red_blood_cells = st.selectbox('Red Blood Cells', ['normal', 'abnormal'])
    coronary_artery_disease = st.selectbox('Coronary Heart Disease?', ['yes', 'no'])
    appetite = st.selectbox('Is the patient\'s appetite good or poor?', ['good', 'poor'])
    hypertension = st.selectbox('Hypertension?', ['yes', 'no'])
    diabetes = st.selectbox('Diabetes?', ['yes', 'no'])
    anemia = st.selectbox('Anemic?', ['yes', 'no'])
    pedal_edema = st.selectbox('Pedal Edema?', ['yes', 'no'])

    # map binary options to 1 and 0
    rbc_prediction_mapping = {'normal':1, 'abnormal':0}
    cad_prediction_mapping = {'yes': 1, 'no':0}
    appetite_prediction_mapping = {'good':1, 'poor':0}
    hypertension_prediction_mapping = {'yes':1, 'no':0}
    diabetes_prediction_mapping = {'yes':1, 'no':0}
    anemia_prediction_mapping = {'yes':1, 'no':0}
    pedal_edema_prediction_mapping = {'yes':1, 'no':0}
    

    # feature engineer columns
    red_blood_cells = rbc_prediction_mapping[red_blood_cells]
    coronary_artery_disease = cad_prediction_mapping[coronary_artery_disease]
    appetite = appetite_prediction_mapping[appetite]
    hypertension = hypertension_prediction_mapping[hypertension]
    diabetes = diabetes_prediction_mapping[diabetes]
    anemia = anemia_prediction_mapping[anemia]
    pedal_edema = pedal_edema_prediction_mapping[pedal_edema]


    # convert to json format for model api
    cols = ['age','bloodPressure','redBloodCellCount','whiteBloodCellCount','packedCellVolume','serumCreatinine','sodium','potassium','hemoglobin','redBloodCells','coronaryArteryDisease','appetite','hypertension','diabetes','anemia','pedalEdema']
    vals = [age,blood_pressure,red_blood_cell_count,white_blood_cell_count,packed_cell_volume,serum_creatinine,sodium,potassium,hemoglobin,red_blood_cells,coronary_artery_disease,appetite,hypertension,diabetes,anemia,pedal_edema]
    data_vals = dict(zip(cols,vals))
    

    
    
    logging.info(data_vals)
    # # Make a prediction based on the inputs
    if st.button('Predict'):
        # define global variable to make accessible outside of if statement
        # global prediction_start_ts_str
        # global prediction_start_ts
        # global prediction_end
        # global prediction
        # global prediction_dt
        # global prediction_duration
        # global prediction_start_ts_str
        # global prediction_start_ts

        prediction_start_ts_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # prediction timestamp
        prediction_start_ts = datetime.datetime.now() # prediction timestamp

        # try:
        logging.info('Making Prediction')
        # create json object from data dictionary
        data_json = json.dumps(data_vals)
        logging.info(data_json)

        # headers
        headers = {'Content-Type': 'application/json'}

        # Fetch the public IP address of the EC2 instance
        # ip_response = requests.get('http://api.ipify.org?format=json')
        # ip_data = ip_response.json()
        # public_ip = ip_data['ip']

        # Make a POST request to the Flask API
        response = requests.post(f'http://localhost:80/predict', data=data_json, headers=headers)
        prediction = response.text
        #prediction = predict(model, blood_pressure, red_blood_cell_count, white_blood_cell_count, packed_cell_volume, serum_creatinine, sodium, potassium, hemoglobin, age, red_blood_cells, coronary_artery_disease, appetite, hypertension, diabetes, anemia, pedal_edema)
        logging.info(f'Prediction Successful: {prediction}')
        # except:
        #     logging.critical('Prediction Not Made.')
        #     st.experimental_rerun() # refresh page if prediction is not returned
        
        prediction_end = datetime.datetime.now() # prediction timestamp
        # prediction duration to track if prediction is taking a long time
        prediction_duration = (prediction_end - prediction_start_ts).total_seconds()

        # Show the prediction to the user
        # prediction = prediction_mapping[prediction]

        st.write(prediction)
        prediction_dt = datetime.date.today().strftime("%Y-%m-%d") # prediction date
        
        
    # add checkbox for user to confirm if prediction is correct    
    is_correct = st.radio('Is this prediction correct?', ('Yes', 'No'))

    # not_correct = st.checkbox('This prediction is not correct!')
    logging.info(f'True Prediction Duration:{prediction_duration}')
    logging.info(f'True Prediction:{prediction}')

    # add submit button for user to officially send predictions to database
    if st.button('Submit'):
        
        if is_correct == 'Yes':
        

            session_end = datetime.datetime.now()
    
            # calculate session duration
            session_duration = (session_end - session_start_ts).total_seconds()
            logging.info(f'Prediction Duration:{prediction_duration}')
            logging.info(f'Prediction:{prediction}')
            # values to insert into sqlite database
            values_to_insert = (session_id, session_start_ts_str, session_dt, session_duration, prediction_start_ts_str, prediction_dt, age, blood_pressure, 
                                red_blood_cell_count, white_blood_cell_count, packed_cell_volume, serum_creatinine, sodium, potassium, hemoglobin, red_blood_cells,
                                coronary_artery_disease, appetite, hypertension, diabetes, anemia, pedal_edema, prediction, prediction_duration, is_correct)
            
            # insert data into database
            cursor.execute(insert_data_query, values_to_insert)

            conn.commit()
            conn.close()

            
            st.write('Thank you for confirming Prediction! We will use this to improve the model')
            logging.debug('Session Finished. Predictions inserted into database')
    
        else:
                
            logging.info(f'Prediction Duration:{prediction_duration}')
            logging.info(f'Prediction:{prediction}')
            session_end = datetime.datetime.now()
    
            # calculate session duration
            session_duration = (session_end - session_start_ts).total_seconds()

            # values to insert into sqlite database
            values_to_insert = (session_id, session_start_ts_str, session_dt, session_duration, prediction_start_ts_str, prediction_dt, age, blood_pressure, 
                                red_blood_cell_count, white_blood_cell_count, packed_cell_volume, serum_creatinine, sodium, potassium, hemoglobin, red_blood_cells,
                                coronary_artery_disease, appetite, hypertension, diabetes, anemia, pedal_edema, prediction, prediction_duration, is_correct)
            
            # insert data into database
            cursor.execute(insert_data_query, values_to_insert)

            conn.commit()
            conn.close()

            st.write("It is very important that we get these predictions correct to reduce false positives as CKD can go undetected for years. Thank you for your feedback. We will use this data to improve our model!")
            logging.debug('Session Finished. Predictions inserted into database')

    

   

# Run the streamlit app
if __name__ == '__main__':
    app()
    # st.experimental_rerun()