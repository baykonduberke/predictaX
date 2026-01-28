from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)


@app.get("/")
async def root():
    return {"message": "Merhaba PredictaX"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
