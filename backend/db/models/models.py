from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CKDPatientData(db.Model):
    __tablename__ = 'patient_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(255))
    session_ts = db.Column(db.String(255))
    session_dt = db.Column(db.String(255))
    session_duration = db.Column(db.Integer)
    prediction_ts = db.Column(db.String(255))
    prediction_dt = db.Column(db.String(10))  # Assuming 'yyyy-mm-dd' format
    age = db.Column(db.Integer)
    blood_pressure = db.Column(db.Integer)
    red_blood_cell_count = db.Column(db.Integer)
    white_blood_cell_count = db.Column(db.Integer)
    packed_cell_volume = db.Column(db.Integer)
    serum_creatinine = db.Column(db.Integer)
    sodium = db.Column(db.Integer)
    potassium = db.Column(db.Integer)
    hemoglobin = db.Column(db.Integer)
    red_blood_cells = db.Column(db.String(255))
    coronary_artery_disease = db.Column(db.String(255))
    appetite = db.Column(db.String(255))
    hypertension = db.Column(db.String(255))
    diabetes = db.Column(db.String(255))
    anemia = db.Column(db.String(255))
    pedal_edema = db.Column(db.String(255))
    prediction = db.Column(db.String(255))
    prediction_duration = db.Column(db.Integer)
    is_correct = db.Column(db.String(255))
