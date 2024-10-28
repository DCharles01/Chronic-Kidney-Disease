import kfp
from kfp import dsl
from kfp.components import func_to_container_op
import mlflow
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

# Component to load and preprocess the data
@func_to_container_op
def load_and_preprocess_data():
    kidney_disease_medical_data = pd.read_csv('../data/kidney_disease.csv')
    kidney_disease_medical_data.replace('ckd\t', 'ckd', inplace=True)

    # Fill missing values and clean data
    def replaceNAWithMean(df, column):
        df[column] = df[column].fillna(df[column].mean())

    def replaceNAWithMode(df, column):
        df[column] = df[column].fillna(df[column].mode()[0])

    numeric_cols = kidney_disease_medical_data.select_dtypes(exclude='object').columns
    object_cols = kidney_disease_medical_data.select_dtypes(include='object').columns

    for col in numeric_cols:
        replaceNAWithMean(kidney_disease_medical_data, col)

    for col in object_cols:
        replaceNAWithMode(kidney_disease_medical_data, col)

    # Further clean and preprocess data
    kidney_disease_medical_data = kidney_disease_medical_data.replace(r'\t', '', regex=True)
    kidney_disease_medical_data = kidney_disease_medical_data.replace('?', '0')
    kidney_disease_medical_data['dm'] = kidney_disease_medical_data['dm'].str.strip()
    kidney_disease_medical_data[['pcv', 'wc', 'rc']] = kidney_disease_medical_data[['pcv', 'wc', 'rc']].astype(float)

    # Feature engineering
    X_features = ['bp', 'rbc', 'rc', 'wc', 'pcv', 'cad', 'appet', 'sc', 'sod', 'pot', 'hemo', 'htn', 'dm', 'ane', 'age', 'pe']
    X = kidney_disease_medical_data[X_features]
    y = kidney_disease_medical_data['classification']

    # Encode categorical variables and target variable
    X = pd.get_dummies(X, drop_first=True, columns=['rbc', 'cad', 'appet', 'htn', 'dm', 'ane', 'pe'])
    y = pd.factorize(kidney_disease_medical_data['classification'])[0]

    return X, y

# Component to train and log models
@func_to_container_op
# def train_and_log_model(self, X_train: pd.DataFrame, y_train: pd.Series, X_test: pd.DataFrame, y_test: pd.Series):
def train_and_log_model():
    mlflow.set_experiment("model_comparison_experiment")

    def train_and_log_model(model, model_name, params):
        with mlflow.start_run(run_name=model_name):
            mlflow.log_params(params)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)
            precision = precision_score(y_test, predictions, average="macro")
            recall = recall_score(y_test, predictions, average="macro")
            f1 = f1_score(y_test, predictions, average="macro")

            # Log metrics
            mlflow.log_metrics({"accuracy": accuracy, "precision": precision, "recall": recall, "f1_score": f1})
            mlflow.sklearn.log_model(model, model_name)
            print(f"{model_name} accuracy: {accuracy:.4f}")

    # Define models and hyperparameters
    models = {
        "DecisionTree": (DecisionTreeClassifier(max_depth=5), {"max_depth": 5}),
        "RandomForest": (RandomForestClassifier(n_estimators=100, max_depth=5), {"n_estimators": 100, "max_depth": 5}),
        "GradientBoosting": (GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3),
                             {"n_estimators": 100, "learning_rate": 0.1, "max_depth": 3}),
        "LogisticRegression": (LogisticRegression(solver="liblinear", penalty="l2", C=1.0), {"solver": "liblinear", "penalty": "l2", "C": 1.0}),
        "NaiveBayes": (GaussianNB(), {})
    }

    for model_name, (model, params) in models.items():
        train_and_log_model(model, model_name, params)

# Define the pipeline
@dsl.pipeline(
    name='Kidney Disease Prediction Pipeline',
    description='A pipeline for kidney disease prediction with data preprocessing and model comparison'
)
def kidney_disease_pipeline():
    # Load and preprocess data
    data_op = load_and_preprocess_data()

    # Split data for training and testing
    X_train, X_test, y_train, y_test = train_test_split(data_op.X, data_op.y, test_size=0.30, random_state=42)
    smote = SMOTE()
    X_train, y_train = smote.fit_resample(X_train, y_train)  # Apply SMOTE to balance classes

    # Train and evaluate models
    train_and_log_op = train_and_log_model(X_train, y_train, X_test, y_test)

# Compile and run the pipeline
kfp.Client().create_run_from_pipeline_func(
    kidney_disease_pipeline,
    namespace="default",
    arguments={},
)
