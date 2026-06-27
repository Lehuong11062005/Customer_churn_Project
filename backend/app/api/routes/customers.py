import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.crud.crud_customer import (
    create_customer,
    get_customer,
    get_customers,
    update_churn_status,
    update_customer,
)
from app.db.database import get_db
from app.models.customer import Customer
from app.models.user import User
from app.schemas.customer_schema import CustomerCreate, CustomerOut, CustomerUpdate
from app.services.ml_service import predict_churn

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.get("/")
def list_customers(
    page: int = 1,
    limit: int = 50,
    search: Optional[str] = None,
    risk: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 50
    skip = (page - 1) * limit
    data, total = get_customers(db=db, skip=skip, limit=limit, search=search, risk=risk)
    logger.debug(f"Customer list retrieved by {current_user.username} (search: {search}, risk: {risk})")
    return {
        "total": total,
        "page": page,
        "total_pages": (total + limit - 1) // limit if total else 1,
        "data": data,
    }


@router.get("/{customer_id}")
def get_customer_detail(customer_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    customer = get_customer(db, customer_id)
    if not customer:
        logger.warning(f"Attempted to access non-existent customer: {customer_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_customer_record(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = get_customer(db, payload.customer_id)
    if existing:
        logger.warning(f"Attempted to create customer with duplicate ID: {payload.customer_id}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CustomerID already exists")
    payload_dict = payload.model_dump()
    payload_dict["churn_score"] = predict_churn(payload_dict)
    customer = create_customer(db, payload_dict)
    logger.info(f"Customer created: {payload.customer_id} with churn_score: {customer.churn_score} by {current_user.username}")
    return {"message": "Created", "data": customer, "predicted_churn_score": customer.churn_score}


@router.put("/{customer_id}")
def update_customer_record(
    customer_id: str,
    payload: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = get_customer(db, customer_id)
    if not customer:
        logger.warning(f"Attempted to update non-existent customer: {customer_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    payload_dict = payload.model_dump(exclude_unset=True)
    if payload_dict:
        payload_dict["churn_score"] = predict_churn(payload_dict)
    customer = update_customer(db, customer, payload_dict)
    logger.info(f"Customer updated: {customer_id} with new churn_score: {customer.churn_score} by {current_user.username}")
    return {"message": "Updated", "data": customer}


@router.patch("/{customer_id}/churn")
def update_churn(customer_id: str, payload: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    customer = get_customer(db, customer_id)
    if not customer:
        logger.warning(f"Attempted to update churn for non-existent customer: {customer_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    if payload.get("churn_label") == "Yes" and not payload.get("churn_reason"):
        logger.warning(f"Churn update missing reason for customer: {customer_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Churn reason is required")
    update_churn_status(db, customer, payload.get("churn_label", "No"), payload.get("churn_reason", ""))
    logger.info(f"Customer churn status updated: {customer_id} -> {payload.get('churn_label')} by {current_user.username}")
    return {"message": "Status Updated"}
