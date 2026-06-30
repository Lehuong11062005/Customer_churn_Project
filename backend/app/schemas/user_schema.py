from typing import Optional,List

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "staff"


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str


class UserStatusUpdate(BaseModel):
    is_active: bool

class UserListResponse(BaseModel):
    data: List[UserOut]
    total: int

class UserCreateResponse(BaseModel):
    message: str
    data: UserOut