import os
import pickle
import numpy as np
from pathlib import Path
from typing import Any, Dict

from .Forest import RandomForest

# 2. Trỏ đường dẫn tới file pkl THẬT (không dùng random_forest_churn giả nữa)
MODEL_DIR = Path(__file__).resolve().parent.parent.parent / "ml_models"
MODEL_PATH = MODEL_DIR / "rf_churn_model.pkl"

def load_model() -> Any:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy file mô hình tại {MODEL_PATH}")
    
    with open(MODEL_PATH, "rb") as handle:
        saved_package = pickle.load(handle)
        # Trích xuất đúng mô hình từ trong dictionary package
        return saved_package['model'] 

MODEL = load_model()

def predict_churn(data: Dict[str, Any]) -> float:
    # 3. Kéo đúng 24 features đầu ra từ preprocessing.py 
    # Frontend gửi API về phải map đúng tên biến này
    features = [
        data.get("Tenure_Months", 0),
        data.get("Monthly_Charges", 0.0),
        data.get("Total_Charges", 0.0),
        data.get("CLTV", 0.0),
        data.get("Gender_Male", 0),
        data.get("Senior_Citizen_Yes", 0),
        data.get("Partner_Yes", 0),
        data.get("Dependents_Yes", 0),
        data.get("Phone_Service_Yes", 0),
        data.get("Multiple_Lines_Yes", 0),
        data.get("Internet_Service_Fiber_optic", 0),
        data.get("Internet_Service_No", 0),
        data.get("Online_Security_Yes", 0),
        data.get("Online_Backup_Yes", 0),
        data.get("Device_Protection_Yes", 0),
        data.get("Tech_Support_Yes", 0),
        data.get("Streaming_TV_Yes", 0),
        data.get("Streaming_Movies_Yes", 0),
        data.get("Contract_One_year", 0),
        data.get("Contract_Two_year", 0),
        data.get("Paperless_Billing_Yes", 0),
        data.get("Payment_Method_Credit_card_automatic", 0),
        data.get("Payment_Method_Electronic_check", 0),
        data.get("Payment_Method_Mailed_check", 0)
    ]
    
    # 4. Chuyển list thành numpy array 2D cho hàm dự đoán
    X_new = np.array([features])
    
    # 5. Gọi predict_proba từ class custom của bạn
    proba = MODEL.predict_proba(X_new)
    
    # Lấy xác suất của class 1 (nguy cơ rời mạng)
    probability = float(proba[0][1])
    
    return round(probability * 100, 2)