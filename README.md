

# Customer Churn Prediction System (End-to-End)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-green)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A complete **end-to-end machine learning project** that predicts whether a telecom customer will churn. This project utilizes the [Telco Customer Churn dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) to build a training pipeline, exposes the model via a Flask REST API, and provides a user-friendly web interface.

This repository demonstrates the full MLOps workflow: Data Cleaning → Preprocessing Pipeline → Model Training → Threshold Tuning → Model Persistence → REST API → Web UI.

---

## 📸 Demo

*(Optional: Add a screenshot of your Web UI here)*

- **Home UI:** `GET /` (Paste JSON payload and view prediction)
- **Health Check:** `GET /health`
- **Prediction API:** `POST /predict` (JSON input → JSON output)

The API response includes:
- `churn_probability`: The raw probability score from the model.
- `churn_label`: `1` (Churn) or `0` (No Churn) based on a custom tuned threshold.
- `threshold`: The specific threshold value used for the decision.

---

## 🏗️ What Was Built (Key Features)

### 1. Data & Preprocessing
- **Data Validation:** Loaded and validated dataset shape (7,043 rows, 21 columns).
- **Data Cleaning:** Handled real-world dirty data, specifically converting `TotalCharges` from `object` to numeric and handling resulting `NaN` values.
- ** robust Pipeline:**
    - `ColumnTransformer` for handling mixed data types.
    - `OneHotEncoder(handle_unknown="ignore")` to ensure the API doesn't crash on unseen categories.
    - `StandardScaler` for normalizing numeric features.

### 2. Modeling
- **Algorithm:** Logistic Regression (Baseline).
- **Pipeline Integration:** Used scikit-learn `Pipeline` to bundle preprocessing and modeling, preventing data leakage and ensuring consistency between training and inference.
- **Threshold Tuning:** Instead of the default `0.5`, the classification threshold was tuned using the **Precision-Recall curve** to prioritize specific business metrics (e.g., Target Recall).

### 3. Deployment
- **Persistence:** Model artifacts saved using `joblib`.
- **API:** Flask REST API handling JSON requests.
- **Frontend:** A clean HTML/JS/CSS dashboard for testing predictions manually.

---

## 📂 Project Structure

```markdown
Customer-Churn-Prediction-System/
├── app/
│   ├── app.py              # Main Flask application
│   ├── static/             # CSS/JS files
│   │   └── app.js
│   └── templates/          # HTML templates
│       └── index.html
├── data/
│   ├── processed/          # Cleaned data for training
│   └── raw/                # Original dataset
├── models/
│   ├── churn_pipeline.joblib  # Trained model pipeline
│   ├── schema.json            # Expected input schema
│   └── threshold.json         # Tuned threshold value
├── notebooks/
│   └── Customer Churn EDA.ipynb  # Jupyter notebook for analysis
├── src/
│   ├── client_test.py      # Script to test the API programmatically
│   └── predict.py          # Prediction logic
├── requirements.txt
└── README.md

```

---

## 🚀 Setup & Installation (Windows)

### 1. Create & Activate Virtual Environment

```powershell
python -m venv .venv
# Activate in PowerShell:
.venv\Scripts\Activate.ps1
# Or in Command Prompt (cmd):
# .venv\Scripts\activate.bat

```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt

```

*> Note: If `requirements.txt` is missing, install necessary packages (flask, scikit-learn, pandas, numpy) and generate it: `pip freeze > requirements.txt*`

---

## 🏃‍♂️ Running the Application

From the project root directory:

```powershell
python -m app.app

```

Once the server starts, open your browser:

* **UI:** [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
* **Health Check:** [http://127.0.0.1:5000/health](http://127.0.0.1:5000/health)

---

## 🔌 API Documentation

### `POST /predict`

Send a JSON object containing customer data to get a churn prediction.

**Headers:**

* `Content-Type: application/json`

**Example Payload:**

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

**Example Response:**

```json
{
  "churn_probability": 0.0310,
  "churn_label": 0,
  "threshold": 0.4021
}

```

---

## 🧪 Testing

### Option A: Python Client

Run the included test script to simulate a client request:

```powershell
python src/client_test.py

```

### Option B: cURL (Windows CMD)

```cmd
curl -X POST [http://127.0.0.1:5000/predict](http://127.0.0.1:5000/predict) ^
  -H "Content-Type: application/json" ^
  -d "{\"gender\":\"Male\", \"SeniorCitizen\": 0, \"Partner\": \"No\", \"Dependents\": \"No\", \"tenure\": 1, \"PhoneService\": \"No\", \"MultipleLines\": \"No phone service\", \"InternetService\": \"DSL\", \"OnlineSecurity\": \"No\", \"OnlineBackup\": \"Yes\", \"DeviceProtection\": \"No\", \"TechSupport\": \"No\", \"StreamingTV\": \"No\", \"StreamingMovies\": \"No\", \"Contract\": \"Month-to-month\", \"PaperlessBilling\": \"Yes\", \"PaymentMethod\": \"Electronic check\", \"MonthlyCharges\": 29.85, \"TotalCharges\": 29.85}"

```

---

## 📝 Reproducibility Notes

1. **`models/churn_pipeline.joblib`**: Contains the full pipeline (Preprocessing + Classifier). This ensures that the exact same transformations applied during training are applied during inference.
2. **`models/schema.json`**: Stores the list of expected input columns. This is used to align the JSON input with the model's expected dataframe structure.
3. **`models/threshold.json`**: Stores the optimal probability threshold derived during the EDA/Training phase.

---

## 🔮 Roadmap (Future Improvements)

* [ ] Add `src/train.py` to automate the training and threshold selection process.
* [ ] Implement Pydantic for stricter input validation and error handling.
* [ ] Add a `/predict_batch` endpoint for bulk processing.
* [ ] integrate SHAP values to explain *why* a customer is at risk of churning.

---

## License

MIT

```

```