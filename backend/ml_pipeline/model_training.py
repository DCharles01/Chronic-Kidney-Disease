# model_training.py
import mlflow
import mlflow.sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_and_log_model(X_train, y_train, X_test, y_test):
    mlflow.set_experiment("model_comparison_experiment")

    def train_and_log_model_instance(model, model_name, params):
        with mlflow.start_run(run_name=model_name):
            mlflow.log_params(params)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)
            precision = precision_score(y_test, predictions, average="macro")
            recall = recall_score(y_test, predictions, average="macro")
            f1 = f1_score(y_test, predictions, average="macro")

            mlflow.log_metrics({"accuracy": accuracy, "precision": precision, "recall": recall, "f1_score": f1})
            mlflow.sklearn.log_model(model, model_name)

    models = {
        "DecisionTree": (DecisionTreeClassifier(max_depth=5), {"max_depth": 5}),
        "RandomForest": (RandomForestClassifier(n_estimators=100, max_depth=5), {"n_estimators": 100, "max_depth": 5}),
        "GradientBoosting": (GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3),
                             {"n_estimators": 100, "learning_rate": 0.1, "max_depth": 3}),
        "LogisticRegression": (LogisticRegression(solver="liblinear", penalty="l2", C=1.0), {"solver": "liblinear", "penalty": "l2", "C": 1.0}),
        "NaiveBayes": (GaussianNB(), {})
    }

    for model_name, (model, params) in models.items():
        train_and_log_model_instance(model, model_name, params)
