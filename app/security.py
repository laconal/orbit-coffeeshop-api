from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

pwdContext = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash_pwd(password: str) -> str:
    return pwdContext.hash(password[:72])

def verify_pwd(password: str, hashed: str) -> bool:
    return pwdContext.verify(password, hashed)

def create_token(data: dict, expiresDelta: timedelta):
    toEncode = data.copy()
    toEncode["exp"] = datetime.now() + expiresDelta
    return jwt.encode(toEncode, settings.secret_key, algorithm = settings.algorithm)

def create_access_token(userID: int):
    return create_token(
        {"userID": str(userID), "type": "access"},
        timedelta(minutes = settings.access_token_expiration)
    )

def create_refresh_token(userID: int):
    return create_token(
        {"userID": str(userID), "type": "refresh"},
        timedelta(days = settings.refresh_token_expiration)
    )