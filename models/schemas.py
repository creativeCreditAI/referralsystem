from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    position: str = Field(min_length=2, max_length=100)


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    position: str
    referral_token: str
    referral_link: str
    timestamp: datetime


class SignupResponse(BaseModel):
    user_id: int
    referral_token: str
    referral_link: str
