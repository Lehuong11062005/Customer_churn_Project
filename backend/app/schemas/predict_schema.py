from typing import Any, Dict, Optional

from pydantic import BaseModel


class PredictRequest(BaseModel):
    data: Dict[str, Any]


class PredictResponse(BaseModel):
    churn_prediction: int
    churn_probability: float
    risk_level: str
