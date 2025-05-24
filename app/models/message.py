from ..db.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.chat_id"), nullable=False, index=True)
    sender_id = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    attachment_url = Column(String)
    timestamp = Column(DateTime, default=datetime.now)
