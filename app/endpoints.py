from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import APIKeyHeader
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User
from app.database import get_db
from app.config import settings
from app.schemas import UserRead, UserUpdate

router = APIRouter(tags = ["users"])

bearerScheme = APIKeyHeader(name = "x-key")

async def get_current_user(token: str = Depends(bearerScheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms = [settings.algorithm])
        userID = payload.get("userID")
        if userID is None: raise HTTPException(status_code = 401, detail = "Invalid token")
    except Exception: raise HTTPException(status_code = 401, detail = "Invalid token")
    
    result = await db.execute(select(User).filter(User.id == userID))
    user = result.scalars().first()

    if not user: raise HTTPException(status_code = 404, detail = "User not found")

    return user

def admin_require(currentUser: User = Depends(get_current_user)):
    if currentUser.role != "Admin":
        raise HTTPException(status_code = 403, detail = "Admin privileges required")
    return currentUser

@router.get("/me", response_model = UserRead,
            summary = "Get user info",
            description = "Returns requesting user info: id, email, firstname, lastname, ,role, isVerified")
def get_me(currentUser: User = Depends(get_current_user)):
    return currentUser

@router.get("/users", response_model = list[UserRead],
            summary = "Get all users (Only for admins)",
            description = "Returns list of all users: [{user1}, {user2}, ...]")
async def users_all(db: AsyncSession = Depends(get_db), _: User = Depends(admin_require)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get("/users/{userID}", response_model = UserRead,
            summary = "Get specific user (Only for admins)",
            description = '''Returns user info: id, email, firstname, lastname, role, isVerified
            
            If requesting user's role is Admin, can get info of any user, 
            if user's role is User, can get only itself info''')
async def get_user(userID: int, db: AsyncSession = Depends(get_db), _: User = Depends(admin_require)):
    result = await db.execute(select(User).filter(User.id == userID))
    user = result.scalars().first()

    if not user: raise HTTPException(status_code = 404, detail = "User not found")

    return user

@router.patch("/users/{userID}", response_model = UserUpdate,
              summary = "Partially update user (Ony for admins)",
              description = "Partially updates user values with provided userID")
async def update_user(userID: int, data: UserUpdate, db: AsyncSession = Depends(get_db),
                currentUser: User = Depends(get_current_user)):
    result = await db.execute(select(User).filter(User.id == userID))
    user = result.scalars().first()

    if not user: raise HTTPException(status_code = 404, detail = "User not found")
    
    if currentUser.role != "Admin" and currentUser.id != user.id:
        raise HTTPException(status_code = 403, detail = "Cannot edit other users")

    updateData = data.model_dump(exclude_unset = True)

    if currentUser.role != "Admin": updateData.pop("role", None)

    for field, value in data.model_dump(exclude_unset = True).items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/users/{userID}", status_code = 204,
               summary = "Delete user (Only for admins)",
               description = "Deletes user with provided userID")
async def delete_user(userID: int, db: AsyncSession = Depends(get_db), _: User = Depends(admin_require)):
    result = await db.execute(select(User).filter(User.id == userID))
    user = result.scalars().first()
    
    if not user: raise HTTPException(status_code = 404, detail = "User not found")
    
    await db.delete(user)
    await db.commit()

    return {"message": f"Successfully deleted user {user.email}"}