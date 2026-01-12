# tests/test_notes_service.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Note, User
from app.schemas.notes import NoteCreate, NoteUpdate
from app.services.notes_service import (
    create_note,
    get_all_notes,
    get_note_by_id,
    update_note,
    delete_note
)
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    # Add a test user with all required fields
    user = User(username="testuser", email="testuser@example.com")
    session.add(user)
    session.commit()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_note(db):
    note_data = NoteCreate(title="Test Note", content="This is a test note", user_id=1)
    note = create_note(db, note_data)
    return note


def test_create_note_success(db):
    note_data = NoteCreate(title="New Note", content="Content", user_id=1)
    note = create_note(db, note_data)
    assert note.id is not None
    assert note.title == "New Note"
    assert note.user_id == 1


def test_create_note_invalid_user(db):
    note_data = NoteCreate(title="Invalid Note", content="Content", user_id=999)
    with pytest.raises(HTTPException) as exc_info:
        create_note(db, note_data)
    assert exc_info.value.status_code == 400


def test_get_all_notes(db, test_note):
    notes = get_all_notes(db)
    assert len(notes) >= 1
    assert any(n.id == test_note.id for n in notes)


def test_get_note_by_id_success(db, test_note):
    note = get_note_by_id(db, test_note.id)
    assert note is not None
    assert note.id == test_note.id


def test_get_note_by_id_not_found(db):
    note = get_note_by_id(db, 999)
    assert note is None


def test_update_note_success(db, test_note):
    update_data = NoteUpdate(title="Updated Title", content="Updated content")
    updated_note = update_note(db, test_note.id, update_data)
    assert updated_note.title == "Updated Title"
    assert updated_note.content == "Updated content"


def test_update_note_not_found(db):
    update_data = NoteUpdate(title="Does Not Exist", content="...")
    updated_note = update_note(db, 999, update_data)
    assert updated_note is None


def test_delete_note_success(db, test_note):
    deleted_note = delete_note(db, test_note.id)
    assert deleted_note.id == test_note.id

    # Ensure it is gone
    note = get_note_by_id(db, test_note.id)
    assert note is None


def test_delete_note_not_found(db):
    deleted_note = delete_note(db, 999)
    assert deleted_note is None
