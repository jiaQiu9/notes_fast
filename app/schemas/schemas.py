from pydantic import BaseModel
from typing import Optional

class NoteBase(BaseModel):
    title: str
    content: Optional[str]=None
    user_id: int

class NoteCreate(NoteBase):
    pass 

class NoteUpdate(BaseModel):
    title:Optional[str] = None
    content: Optional[str] = None

class NoteOut(NoteBase):
    id: int
    model_config={
        "from_attributes":True
    }