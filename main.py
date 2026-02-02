from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.cors import setup_cors
from app.core.exception_handlers import app_exception_handler, generic_exception_handler
from app.core.exceptions import BaseAppException
from app.db.database import Base, engine
from app.routers import auth

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS
setup_cors(app, settings)

# Exception handlers
app.add_exception_handler(BaseAppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/")
async def root():
    return {"message": "Merhaba PredictaX"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


app.include_router(auth.router)
