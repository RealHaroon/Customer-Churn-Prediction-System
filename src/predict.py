import json
import joblib
import pandas as pd

PIPELINE_PATH='D:\\Github\\Customer-Churn-Prediction-System\\models\\churn_pipeline.joblib'
THRESH_PATH='D:\\Github\\Customer-Churn-Prediction-System\\models\\threshold.json'
SCHEMA_PATH='D:\\Github\\Customer-Churn-Prediction-System\\models\\schema.json'

pipeline=joblib.load(PIPELINE_PATH)
threshold=json.load(open(THRESH_PATH))['threshold']
schema=json.load(open(SCHEMA_PATH))['columns']

def predict_one(payload:dict) -> dict:
    X=pd.DataFrame([payload])

    missing=set(schema) - set(X.columns)
    extra = set(X.columns) - set(schema)

    if missing:
        raise ValueError(f'Missing fields : {sorted(missing)}')
    if extra :
        X=X[schema]
    
    X=X[schema]
    proba=float(pipeline.predict_proba(X)[:,1][0])
    label=int(proba >= threshold)
    return {'churn_probability':proba, 'churn_label':label,'threshold':threshold}
