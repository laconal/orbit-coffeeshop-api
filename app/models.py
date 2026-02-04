from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from datetime import datetime, timezone
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    email = Column(String, unique = True, index = True, nullable = False)
    hashedPWD = Column(String, nullable = False)

    firstName = Column(String, nullable = True)
    lastName = Column(String, nullable = True)

    role = Column(String, nullable = False, default = "User")

    isVerified = Column(Boolean, default = False)

    verificationCode = Column(String, nullable = True)
    createdAt = Column(DateTime, default = lambda: datetime.now(timezone.utc), nullable = False, server_default = func.now())