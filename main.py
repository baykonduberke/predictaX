from contextlib import asynccontextmanager

import requests
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


@app.get("/apitest")
async def apitest():
    url = "https://v3.football.api-sports.io/players/league=203"

    payload = {}
    headers = {
        "x-apisports-key": "c8c106cd827858adfbd000e6d049b3e6",
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


@app.get("/besiktas-fikstur")
async def get_besiktas_fixtures():
    url = "https://v3.football.api-sports.io/fixtures"

    params = {"team": "549", "season": "2024"}

    headers = {
        "x-apisports-key": "c8c106cd827858adfbd000e6d049b3e6",
        "x-rapidapi-host": "v3.football.api-sports.io",
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data


@app.get("/mac-istatistik/{fixture_id}")
async def get_match_statistics(fixture_id: int):
    url = "https://v3.football.api-sports.io/fixtures/statistics"
    params = {"fixture": fixture_id}
    headers = {
        "x-apisports-key": "c8c106cd827858adfbd000e6d049b3e6",
        "x-rapidapi-host": "v3.football.api-sports.io",
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()


app.include_router(auth.router)
