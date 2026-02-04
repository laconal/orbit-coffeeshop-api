from datetime import datetime, timedelta
from sqlalchemy.future import select
from app.database import async_session
from app.models import User
from app.celery import celeryApp

@celeryApp.task
async def delete_unverified_users():
    cutoff = datetime.now() - timedelta(days = 2)

    async with async_session() as db:
        result = await db.execute(select(User).filter(
            User.isVerified == False,
            User.createdAt < cutoff
        ))

        usersToDelete = result.scalars().all()

        counter = 0
        for user in usersToDelete:
            await db.delete(user)
            coutner += 1

        await db.commit()

        print(f"Deleted: {counter} unverified users")