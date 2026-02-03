from pydantic import BaseModel, EmailStr
from typing import Literal

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    role: Literal["User", "Admin"] = "User"
    firstName: str | None = None
    lastName: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    accessToken: str
    refreshToken: str
    tokenType: str = "Bearer"

class VerifyUser(BaseModel):
    email: str
    code: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    firstName: str | None
    lastName: str | None
    role: str
    isVerified: bool

class UserUpdate(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
    role: Literal["User", "Admin"] | None = None