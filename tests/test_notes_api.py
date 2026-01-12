# tests/test_notes_api.py
import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
# Import all models to ensure Base.metadata has all table definitions
from app.models import Base, Note, User, Link, Media
from app.db.session import get_db


# ----------------------
# Test database setup
# ----------------------
# Create a temporary file for the test database
# This ensures all connections see the same database
_test_db_file = None

def get_test_db_url():
    global _test_db_file
    if _test_db_file is None:
        # Create a temporary file that will be cleaned up
        fd, _test_db_file = tempfile.mkstemp(suffix='.db')
        os.close(fd)  # Close the file descriptor, SQLAlchemy will open it
    return f"sqlite:///{_test_db_file}"

# Use a module-scoped engine that persists across tests
# We'll recreate it for each test function in the fixture
engine = None
TestingSessionLocal = None

# ------------------------
# Dependency override
# ------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# ------------------------
# Fixtures
# ------------------------
@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """
    Create tables and seed initial data before each test.
    This fixture runs automatically for every test function.
    """
    global engine, TestingSessionLocal
    
    # Create a fresh database file for each test
    test_db_url = get_test_db_url()
    
    # Remove the file if it exists to start fresh
    if os.path.exists(test_db_url.replace("sqlite:///", "")):
        os.remove(test_db_url.replace("sqlite:///", ""))
    
    # Create new engine and session for this test
    engine = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False}
    )
    
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    # Create all tables - this must happen before any database operations
    # Importing all models above ensures Base.metadata has all table definitions
    Base.metadata.create_all(bind=engine)
    
    # Create a session to seed initial data
    db = TestingSessionLocal()
    try:
        # Create test user with id=1 explicitly to match test expectations
        user = User(id=1, username="testuser", email="test@test.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        # Verify the user was created with id=1
        assert user.id == 1, f"Expected user id=1, got {user.id}"
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
    
    # Yield control to the test
    yield
    
    # Cleanup after test
    db_cleanup = TestingSessionLocal()
    try:
        # Delete all data first (in reverse order of foreign key dependencies)
        db_cleanup.query(Note).delete()
        db_cleanup.query(User).delete()
        db_cleanup.commit()
    except Exception:
        db_cleanup.rollback()
    finally:
        db_cleanup.close()
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    
    # Clean up the database file
    db_file = test_db_url.replace("sqlite:///", "")
    if os.path.exists(db_file):
        os.remove(db_file)

# ------------------------
# Tests
# ------------------------
def test_create_note_success(setup_db):
    response = client.post(
        "/notes/",
        json={"title": "API Note", "content": "Created via API", "user_id": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "API Note"
    assert data["content"] == "Created via API"
    assert data["user_id"] == 1
    assert "id" in data

def test_create_note_invalid_user(setup_db):
    response = client.post(
        "/notes/",
        json={"title": "Bad Note", "content": "Should fail", "user_id": 999}
    )
    assert response.status_code == 400
    assert "not found" in response.json()["detail"]

def test_get_all_notes(setup_db):
    client.post("/notes/", json={"title": "Note 1", "content": "A", "user_id": 1})
    response = client.get("/notes/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_note_by_id_success(setup_db):
    create = client.post("/notes/", json={"title": "Single Note", "content": "Test", "user_id": 1})
    note_id = create.json()["id"]
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["id"] == note_id

def test_get_note_by_id_not_found(setup_db):
    response = client.get("/notes/999")
    assert response.status_code == 404

def test_update_note_success(setup_db):
    create = client.post("/notes/", json={"title": "Old", "content": "Old content", "user_id": 1})
    note_id = create.json()["id"]
    response = client.put(f"/notes/{note_id}", json={"title": "Updated", "content": "New content"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["content"] == "New content"

def test_delete_note_success(setup_db):
    create = client.post("/notes/", json={"title": "To delete", "content": "Bye", "user_id": 1})
    note_id = create.json()["id"]
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200  # or 204 if your API uses No Content
    get_response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404