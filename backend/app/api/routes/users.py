from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, require_role
from app.crud.crud_user import (
    create_user,
    get_user,
    get_user_by_email,
    get_user_by_username,
    get_users,
    update_password,
    update_user_status,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.user_schema import PasswordUpdate, UserCreate, UserOut, UserStatusUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/", response_model=dict)
def list_users(
    page: int = 1,
    limit: int = 50,
    role: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "manager")),
):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 50
    skip = (page - 1) * limit
    users, total = get_users(db=db, skip=skip, limit=limit, role=role)
    return {"data": users, "total": total}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user_account(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    if get_user_by_username(db, payload.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    user = create_user(db, payload)
    return {"message": "User created", "data": user}


@router.get("/{user_id}")
def get_user_detail(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if current_user.role == "staff" and current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    if current_user.role == "manager" and user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return user


@router.patch("/{user_id}/status")
def update_status(user_id: int, payload: UserStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    update_user_status(db, user, payload.is_active)
    return {"message": "Status updated"}


@router.put("/me/password")
def update_my_password(payload: PasswordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        update_password(db, current_user, payload.old_password, payload.new_password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return {"message": "Password updated"}
