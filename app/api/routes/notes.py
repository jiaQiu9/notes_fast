from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# from app.schemas.schemas  import NoteCreate, NoteUpdate, NoteOut
from app.services import notes_service
from app.db.session import get_db

from app.schemas.notes import (
    NoteCreate, 
    NoteUpdate,
    NoteResponse
)

router = APIRouter(
    prefix="/notes", 
    tags=["Notes"],
)

@router.get("/", response_model=list[NoteResponse])
def read_notes(db: Session= Depends(get_db)):
    return notes_service.get_all_notes(db)

@router.get("/{note_id}", response_model=NoteResponse)
def read_note(note_id:int, db:Session=Depends(get_db)):
    note = notes_service.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code = 404, detail="Note not found")
    return note

@router.post("/", response_model=NoteResponse)
def create_note(note: NoteCreate, db:Session =Depends(get_db)):
    
    return notes_service.create_note(db, note)
    

@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note: NoteUpdate, db:Session=Depends(get_db)):
    try:
        updated,_ = notes_service.update_note(db, note_id, note)
        if not updated:
            raise HTTPException(status_code=404, detail="Note not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{note_id}", response_model = NoteResponse)
def delete_note(note_id: int, db:Session= Depends(get_db)):
    deleted = notes_service.delete_note(db, note_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return deleted