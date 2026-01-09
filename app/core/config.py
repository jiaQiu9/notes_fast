import os

class Settings:
    APP_NAME: str = "Knowledge Base API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:mysecretpassword@db:5432/kb_db")

settings = Settings()

