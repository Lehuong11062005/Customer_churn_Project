import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.crud.crud_user import create_user, get_user_by_username
from app.db.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, UserOut
from app.api.dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_username(db, payload.username)
    if not user or not verify_password(payload.password, user.hashed_password):
        logger.warning(f"Failed login attempt for username: {payload.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        logger.warning(f"Login attempt with inactive account: {payload.username}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")
    logger.info(f"User logged in: {payload.username} (role: {user.role})")
    token = create_access_token(user.username, user.role)
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "username": user.username, "role": user.role, "full_name": user.full_name}}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "role": current_user.role, "full_name": current_user.full_name, "email": current_user.email, "is_active": current_user.is_active}
