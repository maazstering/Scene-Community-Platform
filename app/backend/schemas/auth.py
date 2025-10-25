from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    phone_or_email: str
    name: Optional[str] = None
    password: Optional[str] = None


class OTPRequest(BaseModel):
    phone_or_email: str


class OTPVerifyRequest(BaseModel):
    phone_or_email: str
    otp_code: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str