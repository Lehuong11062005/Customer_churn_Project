from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.customer import Customer


def get_customer(db: Session, customer_id: str) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 50, search: Optional[str] = None, risk: Optional[str] = None):
    query = db.query(Customer)
    if search:
        like_term = f"%{search}%"
        query = query.filter((Customer.customer_id.like(like_term)) | (Customer.city.like(like_term)))
    if risk:
        if risk == "high":
            query = query.filter(Customer.churn_score != None).filter(Customer.churn_score >= 70.0)
        elif risk == "low":
            query = query.filter(Customer.churn_score != None).filter(Customer.churn_score < 70.0)
    return query.order_by(Customer.id).offset(skip).limit(limit).all(), query.count()

def create_customer(db: Session, customer_data: dict) -> Customer:
    customer = Customer(**customer_data)
    customer.created_at = datetime.utcnow().isoformat()
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer: Customer, customer_data: dict) -> Customer:
    for key, value in customer_data.items():
        if hasattr(customer, key) and value is not None:
            setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer


def update_churn_status(db: Session, customer: Customer, churn_label: str, churn_reason: str) -> Customer:
    customer.churn_label = churn_label
    customer.churn_reason = churn_reason
    db.commit()
    db.refresh(customer)
    return customer


def get_dashboard_summary(db: Session):
    total_customers = db.query(Customer).count()
    current_churn_rate = 0.0
    high_risk_count = db.query(Customer).filter(Customer.churn_score != None).filter(Customer.churn_score >= 0.7).count()
    total_revenue = db.query(Customer).with_entities(Customer.monthly_charges).all()
    total_revenue_value = sum(item[0] or 0 for item in total_revenue)
    churned = db.query(Customer).filter(Customer.churn_label == "Yes").count()
    if total_customers:
        current_churn_rate = round(churned / total_customers, 4)
    return {
        "total_customers": total_customers,
        "current_churn_rate": current_churn_rate,
        "high_risk_count": high_risk_count,
        "total_revenue": round(total_revenue_value, 2),
    }


def get_churn_by_contract(db: Session):
    result = db.query(Customer.contract, Customer.churn_label).all()
    chart = {}
    for contract, label in result:
        if not contract:
            continue
        contract_name = contract
        chart.setdefault(contract_name, {"name": contract_name, "churned": 0, "retained": 0})
        if label == "Yes":
            chart[contract_name]["churned"] += 1
        else:
            chart[contract_name]["retained"] += 1
    return list(chart.values())
