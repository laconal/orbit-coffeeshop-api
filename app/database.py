from sqlalchemy.orm import declarative_base
from app.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(
    settings.database_url, future = True
)

async_session = async_sessionmaker(engine, class_ = AsyncSession)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session