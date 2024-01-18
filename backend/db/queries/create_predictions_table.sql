drop table if exists ckd_patient_data;

CREATE TABLE ckd_patient_data (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    session_ts TIMESTAMP NOT NULL,
    session_dt DATE NOT NULL,
    session_duration INTEGER NOT NULL,
    prediction_ts TIMESTAMP NOT NULL,
    prediction_dt DATE NOT NULL, -- yyyy-mm-dd
    age INTEGER,
    blood_pressure INTEGER,
    red_blood_cell_count INTEGER,
    white_blood_cell_count INTEGER,
    packed_cell_volume INTEGER,
    serum_creatinine INTEGER,
    sodium INTEGER,
    potassium INTEGER,
    hemoglobin INTEGER,
    red_blood_cells VARCHAR(255),
    coronary_artery_disease VARCHAR(255),
    appetite VARCHAR(255),
    hypertension VARCHAR(255),
    diabetes VARCHAR(255),
    anemia VARCHAR(255),
    pedal_edema VARCHAR(255),
    prediction VARCHAR(255) NOT NULL,
    prediction_duration INTEGER NOT NULL,
    is_correct VARCHAR(255) NOT NULL
);

