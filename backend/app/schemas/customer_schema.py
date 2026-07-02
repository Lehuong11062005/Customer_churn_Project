from typing import Optional

from pydantic import BaseModel, Field


class CustomerBase(BaseModel):
    customer_id: str
    gender: Optional[str] = None
    senior_citizen: Optional[int] = None
    partner: Optional[str] = None
    dependents: Optional[str] = None
    tenure_months: Optional[int] = None
    phone_service: Optional[str] = None
    multiple_lines: Optional[str] = None
    internet_service: Optional[str] = None
    online_security: Optional[str] = None
    online_backup: Optional[str] = None
    device_protection: Optional[str] = None
    tech_support: Optional[str] = None
    streaming_tv: Optional[str] = None
    streaming_movies: Optional[str] = None
    contract: Optional[str] = None
    paperless_billing: Optional[str] = None
    payment_method: Optional[str] = None
    monthly_charges: Optional[float] = None
    total_charges: Optional[float] = None
    cltv: Optional[float] = None
    churn_label: Optional[str] = None
    churn_reason: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerOut(CustomerBase):
    id: int
    churn_score: Optional[float] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
