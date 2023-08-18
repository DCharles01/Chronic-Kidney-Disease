# Define the function to make predictions
def predict(model, bp, rc, wc, pcv, sc, sod, pot, hemo, age, rbc, cad, appet, htn, dm, ane, pe):
    # Create a list with the user inputs
    user_inputs = [bp, rc, wc, pcv, sc, sod, pot, hemo, age, rbc, cad, appet, htn, dm, ane, pe]
    # Make a prediction using the loaded model
    prediction = model.predict([user_inputs])
    # Return the prediction
    return prediction[0]