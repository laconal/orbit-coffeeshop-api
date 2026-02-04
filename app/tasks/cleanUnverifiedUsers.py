import asyncio
from datetime import datetime, timedelta
from sqlalchemy.future import select
from app.database import async_session
from app.models import User
from app.celery import celeryApp


async def _delete_unverified_users():
    cutoff = datetime.now() - timedelta(seconds=60)

    async with async_session() as db:
        result = await db.execute(
            select(User).where(
                User.isVerified == False,
                User.createdAt < cutoff
            )
        )

        users_to_delete = result.scalars().all()

        counter = 0
        for user in users_to_delete:
            await db.delete(user)
            counter += 1

        await db.commit()

        print(f"Deleted: {counter} unverified users")


@celeryApp.task
def delete_unverified_users():
    asyncio.run(_delete_unverified_users())
