from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class Note(Base):
    __tablename__ ="notes"

    id = Column(Integer, primary_key=True, index= True)
    title = Column(String, index=True, nullable = False)
    content = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", backref="notes")