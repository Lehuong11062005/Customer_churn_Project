import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.predict_schema import PredictRequest, PredictResponse
from app.services.ml_service import predict_churn

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/predict", tags=["predict"])

@router.post("/evaluate", response_model=PredictResponse)
def evaluate_prediction(payload: PredictRequest, current_user: User = Depends(get_current_user)):
    if not payload.data:
        logger.warning(f"Prediction requested with empty data by {current_user.username}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Prediction data is required"
        )
    
    # Lấy điểm số xác suất từ mô hình (0.0 -> 100.0)
    score = predict_churn(payload.data)
    
    # Phân loại risk_level đồng bộ với kết quả dự đoán rời mạng (ngưỡng 50)
    if score >= 75:
        risk_level = "High"
    elif score >= 50:
        risk_level = "Medium"
    else:
        risk_level = "Low"
        
    logger.debug(f"Prediction made by {current_user.username}: score={score}, risk_level={risk_level}")
    
    return {
        "churn_prediction": "Yes" if score >= 50 else "No", 
        "churn_probability": round(score / 100, 4), 
        "risk_level": risk_level
    }