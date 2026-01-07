```markdown
# Customer Churn Prediction System (End-to-End) — Telco Dataset

A complete **end-to-end machine learning project** that predicts whether a telecom customer will churn, using the Kaggle *Telco Customer Churn* dataset and a deployed Flask API + UI for real-time predictions. 

This repo demonstrates the full workflow: data cleaning → preprocessing pipeline → model training → threshold tuning → model persistence → REST API → web UI. 

---

## Demo (Local)

- Home UI: `GET /` (paste JSON payload and get prediction)
- Health check: `GET /health`
- Prediction API: `POST /predict` (JSON → JSON)

Your API response includes:
- `churn_probability` (model probability)
- `churn_label` (0/1 based on a tuned threshold)
- `threshold` (stored threshold used for classification) 

---

## What was built (skills shown)

### Data & Preprocessing
- Loaded and validated dataset shape + target distribution (7,043 rows, 21 columns). 
- Fixed a real-world issue: `TotalCharges` type conversion (`object` → numeric) with blank values converted to missing (`NaN`).
- Built a robust preprocessing pipeline using:
  - `ColumnTransformer` for mixed numeric/categorical columns
  - `OneHotEncoder(handle_unknown="ignore")` for safe inference on unseen categories
  - `StandardScaler` for numeric features 

### Modeling
- Trained a baseline churn classifier using scikit-learn `Pipeline` so preprocessing + model stay consistent in training and inference.
- Tuned a custom classification threshold using Precision-Recall trade-offs to hit a target churn recall rather than relying on default 0.5 threshold.

### Deployment
- Persisted model artifacts using `joblib` (re-loadable pipeline for inference). 
- Built a Flask REST API that accepts JSON using `request.get_json()` and returns JSON using `jsonify`.
- Added a simple Flask UI (templates + static JS) to test predictions in the browser. 

---

## Model Behavior (Current)

- Uses **Logistic Regression** with a tuned threshold stored in `models/threshold.json`. 
- Output is **probability + label**, where:
  - `churn_label = 1` if `churn_probability >= threshold`
  - else `0`

---

## Project Structure

```text
Customer-Churn-Prediction-System/
├── app/
│   ├── app.py
│   ├── app.js
│   ├── static/
│   └── templates/
│       └── index.html
├── data/
│   ├── processed/
│   └── raw/
├── models/
│   ├── churn_pipeline.joblib
│   ├── schema.json
│   └── threshold.json
├── notebooks/
│   └── Customer Churn EDA.ipynb
├── src/
│   ├── client_test.py
│   └── predict.py
└── README.md
```

---

## Setup (Windows / VS Code)

### 1) Create & activate virtual environment
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```powershell
pip install -r requirements.txt
```

> If you don’t have a `requirements.txt` yet, generate it after installing packages:
```powershell
pip freeze > requirements.txt
```

---

## Run the Flask App

From the project root:
```powershell
python -m app.app
```

Then open:
- `http://127.0.0.1:5000/` (UI)
- `http://127.0.0.1:5000/health` (health check)

Flask’s built-in server is fine for local testing; for production deployment you should use a WSGI server.

---

## API Documentation

### `GET /health`
**Response**
```json
{ "status": "ok" }
```

### `POST /predict`
**Request**
- Content-Type: `application/json` (required for `request.get_json()` to work reliably)

Example payload (one customer):
```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "Yes",
  "tenure": 24,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "No",
  "OnlineSecurity": "No internet service",
  "OnlineBackup": "No internet service",
  "DeviceProtection": "No internet service",
  "TechSupport": "No internet service",
  "StreamingTV": "No internet service",
  "StreamingMovies": "No internet service",
  "Contract": "One year",
  "PaperlessBilling": "No",
  "PaymentMethod": "Mailed check",
  "MonthlyCharges": 20.0,
  "TotalCharges": 480.0
}
```

**Response**
```json
{
  "churn_probability": 0.0310,
  "churn_label": 0,
  "threshold": 0.4021
}
```

---

## Quick Testing

### Option A: Using the provided client
```powershell
python src/client_test.py
```

### Option B: curl
```bash
curl -X POST http://127.0.0.1:5000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"gender\":\"Male\", ... }"
```

---

## Notes on Reproducibility

- `models/churn_pipeline.joblib` contains the full scikit-learn pipeline (preprocessing + classifier), preventing training/inference mismatches. [web:347][web:153]
- `models/schema.json` stores expected input columns to enforce correct field ordering and prevent silent errors.
- `models/threshold.json` stores the tuned threshold used at inference time. 

---

## Next Improvements (Planned)

- Add `src/train.py` to reproduce training + threshold selection from raw data end-to-end.
- Add input validation + better error messages for missing/invalid fields.
- Add `/predict_batch` for predicting multiple customers in one request.
- Add model interpretation (feature importance / SHAP) and a short “business insights” section.

---

## License
MIT (or update as needed).
```
