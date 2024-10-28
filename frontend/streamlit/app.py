import streamlit as st
import secrets
import sqlite3
import datetime
import os
import logging
import requests
import json

# Setup logging
os.makedirs('logs', exist_ok=True)
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format, datefmt='%m/%d/%Y %I:%M:%S %p', handlers=[
    logging.FileHandler(f'logs/logs_{datetime.datetime.now().strftime("%Y%m%d")}.log'),
    logging.StreamHandler()], encoding='utf-8', level=logging.INFO)

# Generate random session id
session_id = secrets.token_hex(16)
session_start_ts_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
session_start_ts = datetime.datetime.now()
session_dt = datetime.date.today().strftime("%Y-%m-%d")

# Page 1: CKD Prediction Form
def ckd_form():
    st.title(f'Patient CKD Prediction\nSession ID: {session_id}')
    
    # Collect inputs
    age = st.number_input('age', min_value=0.0)
    blood_pressure = st.number_input('Blood Pressure (mm/HG)', min_value=0.0)
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

    # Convert inputs to a dictionary for prediction
    cols = ['age','bloodPressure','redBloodCellCount','whiteBloodCellCount','packedCellVolume','serumCreatinine','sodium','potassium','hemoglobin','redBloodCells','coronaryArteryDisease','appetite','hypertension','diabetes','anemia','pedalEdema']
    vals = [age, blood_pressure, red_blood_cell_count, white_blood_cell_count, packed_cell_volume, serum_creatinine, sodium, potassium, hemoglobin, red_blood_cells, coronary_artery_disease, appetite, hypertension, diabetes, anemia, pedal_edema]
    data_vals = dict(zip(cols, vals))

    # Prediction and submission logic
    if st.button('Predict'):
        prediction_start_ts_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prediction_start_ts = datetime.datetime.now()
        logging.info('Making Prediction')
        
        # Create json object
        data_json = json.dumps(data_vals)
        headers = {'Content-Type': 'application/json'}

        # Send POST request to prediction API
        response = requests.post(f'decision-tree-api-alb-300377183.us-east-2.elb.amazonaws.com/predict', data=data_json, headers=headers)
        prediction = response.text
        st.write(f'Prediction: {prediction}')
        
        prediction_end = datetime.datetime.now()
        prediction_duration = (prediction_end - prediction_start_ts).total_seconds()

        # Collect feedback on prediction
        is_correct = st.radio('Is this prediction correct?', ('Yes', 'No'))
        if st.button('Submit'):
            session_end = datetime.datetime.now()
            session_duration = (session_end - session_start_ts).total_seconds()
            
            # Insert data into database
            values_to_insert = (session_id, session_start_ts_str, session_dt, session_duration, prediction_start_ts_str, datetime.date.today().strftime("%Y-%m-%d"), age, blood_pressure, red_blood_cell_count, white_blood_cell_count, packed_cell_volume, serum_creatinine, sodium, potassium, hemoglobin, red_blood_cells, coronary_artery_disease, appetite, hypertension, diabetes, anemia, pedal_edema, prediction, prediction_duration, is_correct)
            cursor.execute(insert_data_query, values_to_insert)
            conn.commit()
            st.write('Thank you for your feedback!')

# Page 2: Portfolio
def portfolio():
    st.title('My Portfolio')
    st.write('Welcome to my portfolio! Here are some of the projects I have worked on.')

    # Add your portfolio content here
    st.markdown(
        """
        ### Projects:
        - [GitHub](https://github.com/your-github-username)
        - [LinkedIn](https://www.linkedin.com/in/your-linkedin-username)
        """
    )

def add_ckd_info():
    st.image("https://static.wixstatic.com/media/002708_7b02c77ce56d440ebbef36bf23bc39f0~mv2.png/v1/fill/w_1000,h_504,al_c,q_90,usm_0.66_1.00_0.01/002708_7b02c77ce56d440ebbef36bf23bc39f0~mv2.png")
    st.markdown("""
    ## Chronic Kidney Disease: The Silent Killer

    Chronic Kidney Disease (CKD) is often referred to as a 'silent killer' because it can progress without showing any noticeable symptoms until significant damage has already occurred. The kidneys are responsible for filtering waste from the blood and regulating fluid balance. When they fail, harmful waste accumulates in the body, leading to serious health issues.

    ### CKD Risk Factors:
    - **Hypertension (High blood pressure)**
    - **Diabetes**
    - **Cardiovascular diseases**
    - **Age over 60**
    - **Family history of kidney disease**

    Early detection is crucial because CKD can often be managed with lifestyle changes and treatment if caught in time.

    ### Understanding the Input Fields

    - **Age:** Age of the patient.
    - **BP (Blood Pressure):** Measured in mmHg, indicates the force of blood against artery walls. High BP can damage the kidneys.
    - **SG (Specific Gravity):** A test to measure the concentration of urine, which can help detect kidney function issues.
    - **AL (Albumin):** Presence of albumin in urine can indicate kidney damage.
    - **SU (Sugar):** High levels of sugar in urine can indicate diabetes, a major risk factor for CKD.
    - **RBC (Red Blood Cells):** Red blood cells in urine can suggest damage to the kidneys or urinary tract.
    - **PC (Pus Cell):** Indicates infection in the kidneys or urinary tract.
    - **PCC (Pus Cell Clumps):** Can indicate a severe infection or inflammation in the kidneys.
    - **BA (Bacteria):** Presence of bacteria in urine may indicate a urinary tract infection.
    - **BGR (Blood Glucose Random):** Blood glucose levels can help identify diabetes, which affects kidney function.
    - **BU (Blood Urea):** Elevated levels of urea can indicate impaired kidney function.
    - **SC (Serum Creatinine):** A key indicator of kidney function. High levels indicate poor kidney filtration.
    - **SOD (Sodium):** Essential for maintaining fluid balance; abnormal levels can affect kidney function.
    - **POT (Potassium):** High potassium levels can indicate poor kidney function.
    - **Hemo (Hemoglobin):** Low hemoglobin can indicate anemia, a common complication of CKD.
    - **PCV (Packed Cell Volume):** Also known as hematocrit, low PCV levels can indicate anemia.
    - **WC (White Blood Cell Count):** High WBC count may indicate infection or inflammation.
    - **RC (Red Blood Cell Count):** Low red blood cell count can indicate anemia, which is often associated with CKD.
    - **HTN (Hypertension):** High blood pressure is both a cause and a result of CKD.
    - **DM (Diabetes Mellitus):** A major risk factor for CKD, as high blood sugar levels can damage the kidneys.
    - **CAD (Coronary Artery Disease):** Heart disease can be related to poor kidney health.
    - **Appet (Appetite):** Loss of appetite can be a symptom of CKD.
    - **PE (Pedal Edema):** Swelling in the legs, which can indicate fluid retention due to kidney failure.
    - **Ane (Anemia):** Anemia is common in CKD because the kidneys help produce red blood cells.
    - **Classification:** Whether the patient has CKD or not.


    ### References
    - https://archive.ics.uci.edu/ml/datasets/chronic_kidney_disease#
    - https://pubmed.ncbi.nlm.nih.gov/28592280/
    - https://www.kidney.org/atoz/content/what_anemia_ckd#:~:text=When%20you%20have%20kidney%20disease,can%20no%20longer%20make%20EPO.
    - https://www.seminarsinnephrology.org/article/S0270-9295(08)00166-6/pdf
    - https://www.cdc.gov/kidneydisease/publications-resources/ckd-national-facts.html#:~:text=CKD%20by%20Age%2C%20Sex%2C%20and,According%20to%20current%20estimates%3A&text=CKD%20is%20more%20common%20in,%25)%20than%20men%20(12%25).
    - https://www.cdc.gov/kidney-disease/php/data-research/?CDC_AAref_Val=https://www.cdc.gov/kidneydisease/publications-resources/ckd-national-facts.html
    - https://www.mayoclinic.org/diseases-conditions/anemia/diagnosis-treatment/drc-20351366
    - https://pubmed.ncbi.nlm.nih.gov/32635265/
    - https://www.kidneyfund.org/living-kidney-disease/health-problems-caused-kidney-disease/high-potassium-hyperkalemia-causes-prevention-and-treatment
    - https://www.jahjournal.org/article.asp?issn=1658-5127;year=2019;volume=10;issue=2;spage=61;epage=66;aulast=Shastry


    ### Educational Resources:
    - [National Kidney Foundation](https://www.kidney.org/)
    - [Mayo Clinic on CKD](https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521)
    - [World Health Organization (WHO)](https://www.who.int/news-room/fact-sheets/detail/kidney-disease)
    """)

# Main function to handle page navigation
def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ["CKD Prediction", "Chronic Kidney Disease Information","Portfolio"])

    if page == "CKD Prediction":
        ckd_form()
    elif page == "Chronic Kidney Disease Information":
        add_ckd_info()
    elif page == "Portfolio":
        portfolio()

# Run the app
if __name__ == '__main__':
    main()
