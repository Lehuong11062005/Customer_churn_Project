import os
import pickle
import numpy as np
from pathlib import Path
from typing import Any, Dict

from .Forest import RandomForest

MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "ml_models"
MODEL_PATH = MODEL_DIR / "rf_churn_model.pkl"

def load_model() -> Any:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy file mô hình tại {MODEL_PATH}")
    
    with open(MODEL_PATH, "rb") as handle:
        saved_package = pickle.load(handle)
        return saved_package['model'] 

MODEL = load_model()

def preprocess_payload_to_features(data: Dict[str, Any]) -> list:
    """
    Hàm này chuyển đổi dữ liệu Pydantic Schema (snake_case, raw string)
    sang danh sách 24 features (One-hot encoded) khớp 100% với lúc train.
    """
    # 1. Lấy các giá trị số cơ bản (chú ý key phải giống hệt trong Schema)
    tenure = data.get("tenure_months") or 0
    monthly_charges = data.get("monthly_charges") or 0.0
    total_charges = data.get("total_charges") or 0.0
    cltv = data.get("cltv", 0.0) # Nếu trong schema không có cltv, mặc định là 0.0

    # 2. Xử lý One-Hot Encoding cho các biến phân loại (Categorical)
    gender_male = 1 if data.get("gender") == "Male" else 0
    senior_citizen = 1 if data.get("senior_citizen") == 1 else 0
    partner_yes = 1 if data.get("partner") == "Yes" else 0
    dependents_yes = 1 if data.get("dependents") == "Yes" else 0
    phone_yes = 1 if data.get("phone_service") == "Yes" else 0
    multiple_lines_yes = 1 if data.get("multiple_lines") == "Yes" else 0
    
    internet_fiber = 1 if data.get("internet_service") == "Fiber optic" else 0
    internet_no = 1 if data.get("internet_service") == "No" else 0
    
    security_yes = 1 if data.get("online_security") == "Yes" else 0
    backup_yes = 1 if data.get("online_backup") == "Yes" else 0
    protection_yes = 1 if data.get("device_protection") == "Yes" else 0
    tech_yes = 1 if data.get("tech_support") == "Yes" else 0
    stream_tv_yes = 1 if data.get("streaming_tv") == "Yes" else 0
    stream_movies_yes = 1 if data.get("streaming_movies") == "Yes" else 0
    
    contract_one = 1 if data.get("contract") == "One year" else 0
    contract_two = 1 if data.get("contract") == "Two year" else 0
    
    paperless_yes = 1 if data.get("paperless_billing") == "Yes" else 0
    
    pay_credit = 1 if data.get("payment_method") == "Credit card (automatic)" else 0
    pay_electronic = 1 if data.get("payment_method") == "Electronic check" else 0
    pay_mailed = 1 if data.get("payment_method") == "Mailed check" else 0

    # 3. Trả về đúng thứ tự 24 features
    return [
        tenure, monthly_charges, total_charges, cltv,
        gender_male, senior_citizen, partner_yes, dependents_yes,
        phone_yes, multiple_lines_yes, internet_fiber, internet_no,
        security_yes, backup_yes, protection_yes, tech_yes,
        stream_tv_yes, stream_movies_yes, contract_one, contract_two,
        paperless_yes, pay_credit, pay_electronic, pay_mailed
    ]

def predict_churn(data: Dict[str, Any]) -> float:
    # Lấy features đã được chuẩn hóa từ payload
    features = preprocess_payload_to_features(data)
    
    # Debug: In ra để kiểm tra mảng đã có số thực sự chưa
    print("=== MẢNG FEATURES ĐƯA VÀO MODEL SAU KHI FIX ===")
    print(features)
    
    X_new = np.array([features])
    
    proba = MODEL.predict_proba(X_new)
    probability = float(proba[0][1])
    
    return round(probability * 100, 2)