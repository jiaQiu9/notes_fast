from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    note_id = Column(Integer, ForeignKey("notes.id"))

    note = relationship("Notes", backref="media")
    