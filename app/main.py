from fastapi import FastAPI
from app.api.routes.health import router as health_router

app = FastAPI(title="Knowledge Base API")

app.include_router(health_router)

@app.get("/")
def root():
    return {"status": "ok"}
