from ..db.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from datetime import datetime
from pydantic import BaseModel

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, nullable=False, index=True)
    sender_id = Column(Integer, nullable=False, unique=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())

class MessageCreate(BaseModel):
    chat_id: int
    content: str

