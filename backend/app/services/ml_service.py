import pickle
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd

from .Forest import RandomForest

MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "ml_models"
MODEL_PATH = MODEL_DIR / "rf_churn_model.pkl"

COLUMN_MAP = {
    "customer_id": "CustomerID",
    "gender": "Gender",
    "senior_citizen": "Senior Citizen",
    "partner": "Partner",
    "dependents": "Dependents",
    "tenure_months": "Tenure Months",
    "phone_service": "Phone Service",
    "multiple_lines": "Multiple Lines",
    "internet_service": "Internet Service",
    "online_security": "Online Security",
    "online_backup": "Online Backup",
    "device_protection": "Device Protection",
    "tech_support": "Tech Support",
    "streaming_tv": "Streaming TV",
    "streaming_movies": "Streaming Movies",
    "contract": "Contract",
    "paperless_billing": "Paperless Billing",
    "payment_method": "Payment Method",
    "monthly_charges": "Monthly Charges",
    "total_charges": "Total Charges",
    "cltv": "CLTV",
    "city": "City",
    "state": "State",
    "zip_code": "Zip Code",
    "country": "Country",
    "churn_label": "Churn Label",
    "churn_reason": "Churn Reason",
}

LEAKAGE_COLUMNS = [
    "Churn Value",
    "Churn Score",
    "Churn Reason",
    "CustomerID",
    "City",
    "Zip Code",
    "Latitude",
    "Longitude",
    "Lat Long",
    "Count",
    "Country",
    "State",
    "Churn Label",
]


def load_model() -> Dict[str, Any]:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy file mô hình tại {MODEL_PATH}")

    with open(MODEL_PATH, "rb") as handle:
        saved_package = pickle.load(handle)

    if "feature_names" not in saved_package:
        raise ValueError("Saved model package must include feature_names. Retrain model with updated train_model.py.")

    return saved_package

SAVED_PACKAGE = load_model()
MODEL = SAVED_PACKAGE["model"]
FEATURE_NAMES = SAVED_PACKAGE["feature_names"]
TRAINING_COLUMNS = SAVED_PACKAGE.get("training_columns", [])


def preprocess_payload_to_features(data: Dict[str, Any]) -> np.ndarray:
    payload_df = pd.DataFrame([data])
    payload_df = payload_df.rename(columns=COLUMN_MAP)

    if TRAINING_COLUMNS:
        payload_df = payload_df.reindex(columns=TRAINING_COLUMNS, fill_value=pd.NA)

    numeric_columns = [
        "Tenure Months",
        "Monthly Charges",
        "Total Charges",
        "CLTV",
        "Senior Citizen",
    ]
    for column in numeric_columns:
        if column in payload_df.columns:
            payload_df[column] = pd.to_numeric(payload_df[column], errors="coerce").fillna(0)

    payload_df = payload_df.drop(columns=[c for c in LEAKAGE_COLUMNS if c in payload_df.columns], errors="ignore")

    X = pd.get_dummies(payload_df, drop_first=True, dtype=int)

    useless_dummies = [
        c for c in X.columns
        if "No internet service" in c
        or "No phone service" in c
    ]
    if useless_dummies:
        X = X.drop(columns=useless_dummies, errors="ignore")

    X = X.reindex(columns=FEATURE_NAMES, fill_value=0)

    print(f"Prediction feature count: {X.shape[1]}")
    print(f"Prediction feature names: {list(X.columns)}")

    return X.to_numpy()

def predict_churn(data):
    features = preprocess_payload_to_features(data)

    print(features.shape)

    proba = MODEL.predict_proba(features)

    probability = float(proba[0][1])

    return round(probability * 100, 2)