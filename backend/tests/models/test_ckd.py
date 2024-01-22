from .create_data import insert_data



def test_user_has_session_id(insert_data):
    user = insert_data
    assert user.session_id == '123'

def test_patient_has_prediction(insert_data):
    patient = insert_data
    assert patient.prediction == 'CKD'