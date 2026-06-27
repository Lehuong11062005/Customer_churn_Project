from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.crud.crud_customer import get_churn_by_contract, get_dashboard_summary
from app.db.database import get_db
from app.models.user import User

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(db=Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_dashboard_summary(db)


@router.get("/charts/churn-by-contract")
def churn_by_contract(db=Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_churn_by_contract(db)
