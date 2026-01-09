from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes import notes
from app.models.base import Base
from app.db.session import engine

app = FastAPI(title="Knowledge Base API")

Base.metadata.create_all(bind=engine)
app.include_router(notes.router)
