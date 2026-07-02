from sqlalchemy import Boolean, Column, Float, Integer, String, Text

from app.db.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), unique=True, nullable=False, index=True)
    gender = Column(String(20), nullable=True)
    senior_citizen = Column(Integer, nullable=True)
    partner = Column(String(20), nullable=True)
    dependents = Column(String(20), nullable=True)
    tenure_months = Column(Integer, nullable=True)
    phone_service = Column(String(20), nullable=True)
    multiple_lines = Column(String(20), nullable=True)
    internet_service = Column(String(50), nullable=True)
    online_security = Column(String(20), nullable=True)
    online_backup = Column(String(20), nullable=True)
    device_protection = Column(String(20), nullable=True)
    tech_support = Column(String(20), nullable=True)
    streaming_tv = Column(String(20), nullable=True)
    streaming_movies = Column(String(20), nullable=True)
    contract = Column(String(50), nullable=True)
    paperless_billing = Column(String(20), nullable=True)
    payment_method = Column(String(50), nullable=True)
    monthly_charges = Column(Float, nullable=True)
    total_charges = Column(Float, nullable=True)
    cltv = Column(Float, nullable=True)
    churn_label = Column(String(10), nullable=True)
    churn_reason = Column(Text, nullable=True)
    churn_score = Column(Float, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    created_at = Column(String(50), nullable=True)
