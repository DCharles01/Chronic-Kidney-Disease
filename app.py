import streamlit as st
import joblib

# Load the pre-trained logistic regression model
model = joblib.load('decision_tree_model_0429.pkl')


# Define the function to make predictions
def predict(bp, rc, wc, pcv, sc, sod, pot, hemo, age, rbc, cad, appet, htn, dm, ane, pe):
    # Create a list with the user inputs
    user_inputs = [bp, rc, wc, pcv, sc, sod, pot, hemo, age, rbc, cad, appet, htn, dm, ane, pe]
    # Make a prediction using the loaded model
    prediction = model.predict([user_inputs])
    # Return the prediction
    return prediction[0]

# def replaceNAWithMean(df, column):
#     df[column] = df[column].fillna(df[column].mean())

# def replaceNAWithMode(df, column):
#     df[column] = df[column].fillna(df[column].mode()[0])

# def pre_processing(df):


#     X = pd.get_dummies(kidney_training_data, columns=['rbc', 'cad', 'appet', 'htn', 'dm', 'ane', 'pe'])


# Define the streamlit app
def app():
    # Set the title of the app
    st.title('Patient CKD Prediction')
    # Ask the user for the inputs
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

    rbc_prediction_mapping = {'normal':1, 'abnormal':0}
    cad_prediction_mapping = {'yes': 1, 'no':0}
    appetite_prediction_mapping = {'good':1, 'poor':0}
    hypertension_prediction_mapping = {'yes':1, 'no':0}
    diabetes_prediction_mapping = {'yes':1, 'no':0}
    anemia_prediction_mapping = {'yes':1, 'no':0}
    pedal_edema_prediction_mapping = {'yes':1, 'no':0}
    prediction_mapping = {'ckd': 'Patient Has CKD', 'notckd':'Patient Does Not Have CKD'}

    # feature engineer columns
    red_blood_cells = rbc_prediction_mapping[red_blood_cells]
    coronary_artery_disease = cad_prediction_mapping[coronary_artery_disease]
    appetite = appetite_prediction_mapping[appetite]
    hypertension = hypertension_prediction_mapping[hypertension]
    diabetes = diabetes_prediction_mapping[diabetes]
    anemia = anemia_prediction_mapping[anemia]
    pedal_edema = pedal_edema_prediction_mapping[pedal_edema]

    

    # Make a prediction based on the inputs
    if st.button('Predict'):
        prediction = predict(blood_pressure, red_blood_cell_count, white_blood_cell_count, packed_cell_volume, serum_creatinine, sodium, potassium, hemoglobin, age, red_blood_cells, coronary_artery_disease, appetite, hypertension, diabetes, anemia, pedal_edema)
        # Show the prediction to the user

        Prediction = prediction_mapping[prediction]
        st.write(Prediction)

# Run the streamlit app
if __name__ == '__main__':
    app()