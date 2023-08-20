from flask import Flask, request, jsonify
import pickle
import json

app = Flask(__name__)

# Load the machine learning model

model = pickle.load(open('model_api/model_decisiontree_0801.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    user_inputs = [data['age'], data['blood_pressure'], data['red_blood_cell_count'], data['white_blood_cell_count'], 
                data['packed_cell_volume'], data['serum_creatinine'], data['sodium'], data['potassium'], data['hemoglobin'], 
                data['red_blood_cells'], data['coronary_artery_disease'], data['appetite'], data['hypertension'], data['diabetes'], 
                data['anemia'], data['pedal_edema']]
    
    prediction = model.predict([user_inputs])[0]
    prediction_mapping = {0: 'Patient Has CKD', 1:'Patient Does Not Have CKD'}
    return prediction_mapping[prediction]



if __name__ == '__main__':
    app.run()



