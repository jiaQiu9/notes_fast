from sqlalchemy.orm import Session
from app.models import Note, User
from app.schemas.schemas import NoteCreate, NoteUpdate
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

def get_all_notes(db: Session):
    return db.query(Note).all()

def get_note_by_id(db:Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()

def create_note(db: Session, note: NoteCreate):
    # validate user exists
    user = db.query(User).filter(User.id == note.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail=f"User with id {note.user_id} not found")

    try:
        db_note = Note(title=note.title, content=note.content, user_id=note.user_id)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
def update_note(db: Session, note_id: int, note_update: NoteUpdate):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        return None
    update_data = note_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note  # <- return the Note instance




def delete_note(db:Session, note_id: int):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        return None
    db.delete(db_note)
    db.commit()
    return db_note