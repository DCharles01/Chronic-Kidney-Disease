from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the machine learning model

model = joblib.load('model_api/decision_tree_model_0429.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Assuming the input data is sent as JSON
    user_inputs = [data['age'], data['blood_pressure'], data['red_blood_cell_count'], data['white_blood_cell_count'], 
                   data['packed_cell_volume'], data['serum_creatinine'], data['sodium'], data['potassium'], data['hemoglobin'], 
                   data['red_blood_cells'], data['coronary_artery_disease'], data['appetite'], data['hypertension'], data['diabetes'], 
                   data['anemia'], data['pedal_edema']]
    prediction = model.predict([user_inputs])
    return jsonify({'prediction': prediction[0]})
