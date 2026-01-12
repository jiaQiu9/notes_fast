from pydantic import BaseModel, Field
from typing import Optional

# Shared base fields
class NoteBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Title of the note"
    )
    content: Optional[str] = Field(
        None, 
        max_length=5000, # max length enforced
        description="Optional note content"
    )

# used when creating a note
class NoteCreate(NoteBase):
    user_id: Optional[int] = Field(
        default=1,
        ge=1,
        description="Owner user ID (default user for now)"
    )

# Used when updating a note
class NoteUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
    )
    content: Optional[str]=None

# Used when returning a note
class NoteResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    user_id: int

    class Config:
        from_attributes = True # SQLAlchemy compatibility