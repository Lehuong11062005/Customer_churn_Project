import os
import pickle
from pathlib import Path
from typing import Any, Dict

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

from app.core.config import settings

MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "ml_models"
MODEL_PATH = MODEL_DIR / "random_forest_churn.pkl"


def ensure_model_exists() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    if MODEL_PATH.exists():
        return
    X, y = make_classification(n_samples=200, n_features=8, n_informative=5, n_redundant=0, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    with open(MODEL_PATH, "wb") as handle:
        pickle.dump(model, handle)


def load_model() -> Any:
    ensure_model_exists()
    with open(MODEL_PATH, "rb") as handle:
        return pickle.load(handle)


MODEL = load_model()


def predict_churn(data: Dict[str, Any]) -> float:
    features = [
        data.get("tenure_months", 0),
        data.get("monthly_charges", 0),
        data.get("total_charges", 0),
        1 if data.get("partner") == "Yes" else 0,
        1 if data.get("dependents") == "Yes" else 0,
        1 if data.get("contract") == "Month-to-month" else 0,
        1 if data.get("internet_service") == "Fiber optic" else 0,
        1 if data.get("paperless_billing") == "Yes" else 0,
    ]
    frame = pd.DataFrame([features], columns=["tenure_months", "monthly_charges", "total_charges", "partner", "dependents", "contract", "internet_service", "paperless_billing"])
    probability = float(MODEL.predict_proba(frame)[0][1])
    return round(probability * 100, 2)
