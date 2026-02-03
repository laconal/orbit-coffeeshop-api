from fastapi import FastAPI
from app.database import Base, engine
from app.auth import router as r_auth
from app.endpoints import router as r_endpoints
from app.config import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.environment == "dev":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(title = "Coffee shop API", lifespan = lifespan)

app.include_router(r_auth)
app.include_router(r_endpoints)