# data_preprocessing.py
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

def load_and_preprocess_data():
    kidney_disease_medical_data = pd.read_csv('../data/kidney_disease.csv')
    kidney_disease_medical_data.replace('ckd\t', 'ckd', inplace=True)

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

    kidney_disease_medical_data = kidney_disease_medical_data.replace(r'\t', '', regex=True)
    kidney_disease_medical_data = kidney_disease_medical_data.replace('?', '0')
    kidney_disease_medical_data['dm'] = kidney_disease_medical_data['dm'].str.strip()
    kidney_disease_medical_data[['pcv', 'wc', 'rc']] = kidney_disease_medical_data[['pcv', 'wc', 'rc']].astype(float)

    X_features = ['bp', 'rbc', 'rc', 'wc', 'pcv', 'cad', 'appet', 'sc', 'sod', 'pot', 'hemo', 'htn', 'dm', 'ane', 'age', 'pe']
    X = kidney_disease_medical_data[X_features]
    y = kidney_disease_medical_data['classification']

    X = pd.get_dummies(X, drop_first=True, columns=['rbc', 'cad', 'appet', 'htn', 'dm', 'ane', 'pe'])
    y = pd.factorize(kidney_disease_medical_data['classification'])[0]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
    smote = SMOTE()
    X_train, y_train = smote.fit_resample(X_train, y_train)

    return X_train, X_test, y_train, y_test
