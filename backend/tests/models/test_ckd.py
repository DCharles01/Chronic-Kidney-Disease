from .create_data import insert_data



def test_user_has_age(insert_data):
    user = insert_data
    assert user.age == 25

def test_patient_has_prediction(insert_data):
    patient = insert_data
    assert patient.prediction == 'CKD'