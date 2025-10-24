from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    city: Optional[str] = None
    bio: Optional[str] = None
    verified_flag: bool
    vouches_count: int = 0
    activities_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class VouchResponse(BaseModel):
    id: str
    giver_user_id: str
    giver_name: str
    giver_avatar_url: Optional[str] = None
    short_text: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class VouchCreate(BaseModel):
    to_user_id: str
    text: Optional[str] = None