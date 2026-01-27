from fastapi import FastAPI

app = FastAPI(title="PredictaX", description="PredictaX")


@app.get("/")
async def root():
    return {"message": "Merhaba PredictaX"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
