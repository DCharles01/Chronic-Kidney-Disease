drop table if exists ckd_patient_data;

CREATE TABLE ckd_patient_data (
    session_id TEXT,
    session_ts TEXT,
    sesstion_dt TEXT,
    session_duration INTEGER,
    prediction_ts TEXT,
    prediction_dt TEXT, -- yyyy-mm-dd 
    age INTEGER,
    blood_pressure INTEGER,
    red_blood_cell_count INTEGER,
    white_blood_cell_count INTEGER,
    packed_cell_volume INTEGER,
    serum_creatinine INTEGER,
    sodium INTEGER,
    potassium INTEGER,
    hemoglobin INTEGER,
    red_blood_cells TEXT,
    coronary_artery_disease TEXT,
    appetite TEXT,
    hypertension TEXT,
    diabetes TEXT,
    anemia TEXT,
    pedal_edema TEXT,
    prediction TEXT,
    prediction_duration INTEGER,
    is_correct TEXT
);
