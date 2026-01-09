from sqlalchemy.orm import Session
from app.models import Note
from app.schemas.schemas import NoteCreate, NoteUpdate


def get_all_notes(db: Session):
    return db.query(Note).all()

def get_note_by_id(db:Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()

def create_note(db:Session, note: NoteCreate):
    db_note = Note(title=note.title, content=note.content, user_id=note.user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db:Session, note_id: int, note: NoteUpdate):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        return None
    for field, value in note.dict(exclude_unset=True).items():
        setattr(db_note, field, value)

    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db:Session, note_id: int):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        return None
    db.delete(db_note)
    db.commit()
    return db_note