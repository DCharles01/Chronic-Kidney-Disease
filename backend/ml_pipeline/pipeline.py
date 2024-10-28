# predictions_pipeline.py
from prefect import flow, task
from data_preprocessing import load_and_preprocess_new_data
from model_loading import load_models
from predictions import make_predictions
from database import store_prediction_in_db

@task
def load_new_data_task(filepath):
    return load_and_preprocess_new_data(filepath)

@task
def load_models_task(model_names):
    return load_models(model_names)

@task
def make_predictions_task(models, X_new):
    return make_predictions(models, X_new)

@task
def store_predictions_task(predictions):
    for model_name, prediction_values in predictions.items():
        for prediction in prediction_values:
            store_prediction_in_db(model_name, prediction)

@flow(name="Prediction Pipeline")
def prediction_pipeline(filepath, model_names):
    # Load and preprocess new data
    X_new = load_new_data_task(filepath)

    # Load models
    models = load_models_task(model_names)

    # Make predictions
    predictions = make_predictions_task(models, X_new)

    # Store predictions in database
    store_predictions_task(predictions)

if __name__ == "__main__":
    # Run the prediction pipeline
    prediction_pipeline(filepath="../data/new_kidney_data.csv", model_names=["DecisionTree", "RandomForest", "GradientBoosting", "LogisticRegression", "NaiveBayes"])
