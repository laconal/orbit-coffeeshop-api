from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
import random

from app.database import get_db
from app.models import User
from app.schemas import UserSignup, UserLogin, Token, VerifyUser
from app.config import settings
import app.security as security

def generate_verification_code(length: int = 6) -> str:
    return "".join([str(random.randint(0, 9)) for _ in range(length)])

router = APIRouter(prefix = "/auth", tags = ["Authentication"])

@router.post("/signup", status_code = 201,
             summary = "Register new user",
             description = "Creates new user and generates verification code")
async def signup(data: UserSignup, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == data.email))
    emailExists = result.scalars().first()
    if emailExists:
        raise HTTPException(status_code = 400, detail = "Email already registered")
    
    vCode = generate_verification_code()

    user = User(
        email=data.email,
        hashedPWD=security.hash_pwd(data.password),
        firstName=data.firstName,
        lastName=data.lastName,
        verificationCode=vCode,
        role=data.role
    )

    db.add(user)
    await db.commit()

    print(f"Verification code for user {data.email}: {vCode}")

    return {"message": "User successfully registered"}

@router.post("/verify", 
             summary = "User verificaiton",
             description = "Verfiy user if code is equal to verification code created in singup step, if yes - user is verified")
async def verify_user(data: VerifyUser, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == data.email))
    user = result.scalars().first()

    if not user: raise HTTPException(status_code = 404, detail = "User not found")
    if user.isVerified: return {"message": "User is alerady verified"}
    if user.verificationCode != data.code: raise HTTPException(status_code = 400, detail = "Invalid verification code")

    user.isVerified = True
    user.verificationCode = None

    await db.commit()

    return {"message": "User successfully verified"}

@router.post("/login", response_model = Token,
             summary = "Getting JWT tokens",
             description = "If credentials (email and password) is correct, returns jwt acces, refress tokens and token type")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == data.email))
    user = result.scalars().first()

    if not user or not security.verify_pwd(data.password, user.hashedPWD):
        raise HTTPException(status_code = 401, detail = "Invalid credentials")
    
    return Token(
        accessToken = security.create_access_token(user.id),
        refreshToken = security.create_refresh_token(user.id)
    )
    

@router.post("/refresh", response_model = Token,
             summary = "Refresh access token",
             description = "Refreshes the access token using a valid refresh token")
async def refresh_token(refreshToken: str):
    try:
        payload = jwt.decode(refreshToken, settings.secret_key, algorithms = [settings.algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code = 401, detail = "Invalid token type")
        
        userID = int(payload.get("userID"))

    except JWTError: raise HTTPException(status_code = 401, detail = "Invalid refresh token")

    return Token(
        accessToken = security.create_access_token(userID),
        refreshToken = security.create_refresh_token(userID)
    )