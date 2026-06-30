from fastapi import APIRouter, Depends
import logging

from app.api.dependencies import get_current_user
from app.crud.crud_customer import get_churn_by_contract, get_dashboard_summary
from app.db.database import get_db
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/summary")
def dashboard_summary(db=Depends(get_db), current_user: User = Depends(get_current_user)):
    # Có thể thêm log để debug nếu dữ liệu dashboard bị lỗi
    logger.debug(f"Dashboard summary requested by {current_user.username}")
    return get_dashboard_summary(db)

@router.get("/charts/churn-by-contract")
def churn_by_contract(db=Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.debug(f"Churn by contract chart requested by {current_user.username}")
    return get_churn_by_contract(db)