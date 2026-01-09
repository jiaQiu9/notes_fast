from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas  import NoteCreate, NoteUpdate, NoteOut
from app.services import notes_service
from app.db.session import get_db

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("/", response_model=list[NoteOut])
def read_note(db: Session= Depends(get_db)):
    return notes_service.get_all_notes(db)

@router.get("/{note_id}", response_model=NoteOut)
def read_note(note_id:int, db:Session=Depends(get_db)):
    note = notes_service.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code = 404, detail="Note not found")
    return note

@router.post("/", response_model=NoteOut)
def create_note(note: NoteCreate, db:Session =Depends(get_db)):
    return notes_service.create_note(db, note)

@router.put("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note: NoteUpdate, db:Session=Depends(get_db)):
    updated = notes_service.update_note(db, note_id, note)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated

@router.delete("/{note_id}", response_model = NoteOut)
def delete_note(note_id: int, db:Session= Depends(get_db)):
    delete = notes_service.delete_note(db, note_id)
    if not delete:
        raise HTTPException(status_code=404, detail="Note not found")
    return delete