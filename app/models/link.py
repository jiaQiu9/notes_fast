from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    url  = Column(String, nullable=False)
    note_id = Column(Integer, ForeignKey("notes.id"))

    note = relationship("Note", backref="links")

    