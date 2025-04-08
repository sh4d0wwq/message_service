from ..db.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from datetime import datetime
from pydantic import BaseModel

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, index=True, nullable=False)
    receiver_id = Column(Integer, index=True, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now())

class MessageCreate(BaseModel):
    receiver_id: int
    content: str

class MessageRead(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    timestamp: datetime
