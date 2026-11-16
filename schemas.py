from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ---------- Users ----------
class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Projects ----------
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Tasks ----------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: str = "medium"
    user_id: Optional[int] = None
    project_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

from pydantic import BaseModel

# סכמת קלט: מגדירה מה המשתמש חייב לשלוח בעת ההרשמה
class UserRegister(BaseModel):
    username: str
    password: str

# סכמת פלט: מגדירה מה השרת מחזיר למשתמש לאחר ההרשמה (ללא סיסמה!)
class UserRegisterResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True