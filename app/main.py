from fastapi import FastAPI
from sqlalchemy import text
from app.api.routes.health import router as health_router
from app.api.routes import notes
from app.models.base import Base
from app.models import User, Note, Link, Media  # Import all models so they register with Base.metadata
from app.db.session import engine, SessionLocal

app = FastAPI(title="Knowledge Base API")

# Import models before create_all() so they register with Base.metadata
Base.metadata.create_all(bind=engine)

# Create a default user with id=1 at startup (first time only)
def create_default_user():
    db = SessionLocal()
    try:
        # Check if user with id=1 already exists
        existing_user = db.query(User).filter(User.id == 1).first()
        if not existing_user:
            # Use raw SQL to insert user with id=1, bypassing the sequence
            with engine.connect() as conn:
                # Insert the user directly with id=1 using raw SQL
                conn.execute(text("""
                    INSERT INTO users (id, username, email) 
                    VALUES (1, 'default', 'default@example.com')
                    ON CONFLICT (id) DO NOTHING
                """))
                conn.commit()
            
            # After inserting id=1, set sequence to 1 so next auto-increment gets 2
            with engine.connect() as conn:
                # Set sequence to 1 (the last inserted value)
                # The 'false' parameter means the next call to nextval will return 2
                conn.execute(text("SELECT setval('users_id_seq', 1, false)"))
                conn.commit()
            
            print("Created default user with id: 1")
        else:
            print("Default user with id=1 already exists")
    except Exception as e:
        db.rollback()
        print(f"Error creating default user: {e}")
    finally:
        db.close()

create_default_user()

app.include_router(notes.router)
